# -*- coding: utf-8 -*-
"""Forecasting Export Product.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KUh7_9eVOfFG7wcfR8RSd1MQrpf1hS03

Masukkan data yang terdiri dari waktu, keuntungan, dan kurs pada waktu tersebut"""

from matplotlib import pyplot
import matplotlib.pyplot as plt
import matplotlib as plt
import pandas as pd
import numpy as np
import seaborn as sns

# Masukkan data
data = pd.read_csv('data mil.txt', sep=';', header=0, low_memory=False)
data.to_csv('data.csv')
dataset = pd.read_csv('data.csv')
dataset = pd.DataFrame(dataset)
df = dataset.drop(columns=['Unnamed: 0'])
df['waktu'] = pd.to_datetime(df.waktu)
df1 = pd.DataFrame(df, columns=['waktu', 'keuntungan'])
df

"""Menampilkan plot time series keuntungan vs kurs"""

import matplotlib as plt
import matplotlib.pyplot as plt
# Menampilkan plot time series data
plt.rcParams['figure.figsize'] = (35, 5)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(24,12))

axa = df['keuntungan'].plot(colormap='BrBG',figsize=(15,5),title='Plot Time Series Keuntungan Perusahaan Setiap Bulan', ax=ax1);
axa.set_xlabel("Periode")
axa.set_ylabel("Keuntungan")
axb = df['kurs'].plot(colormap='BrBG_r',figsize=(15,5),title='Plot Time Series Kurs Dollar Terhadap Rupiah', ax=ax2);
axb.set_xlabel("Periode")
axb.set_ylabel("Nilai Kurs")
fig.tight_layout()

"""Membuat data training (insample) sebagai pembentuk model dan data test (outsample) sebagai uji kinerja model"""

# Membuat data training dan test
train = df.keuntungan[:86]
test = df.keuntungan[84:]

"""Menampilkan plot time series data training"""

import matplotlib as plt
# Menampilkan plot time series data
ax = train.plot(colormap='BrBG',figsize=(15,5),title='Plot Time Series Keuntungan Perusahaan Setiap Bulan');
ax.set_xlabel("Waktu")
ax.set_ylabel("Jumlah")

"""Melakukan uji-uji untuk menentukan model terbaik"""

from statsmodels.tsa.stattools import adfuller
from numpy import log
# Uji stasioner dengan ADF Test
result = adfuller(train)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['figure.figsize'] = (35, 5)
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Membuat plot acf dan pacf
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(24,12))

# Plot the ACF of Data Train
acf=plot_acf(train, lags=36, zero=False, ax=ax1, title='Plot ACF Tanpa Differencing');


# Plot the PACF of Data Train
pacf=plot_pacf(train, lags=36, zero=False, ax=ax2, title='Plot PACF Tanpa Differencing');

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['figure.figsize'] = (35, 5)
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# difference data train
train1 = train.diff().dropna()

# Membuat plot acf dan pacf setelah di difference
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(24,12))

# Plot the ACF of Data Train1
acf1=plot_acf(train1, lags=36, zero=False, ax=ax1, title='Plot ACF 1st Order Differencing');


# Plot the PACF of Data Train1
pacf1=plot_pacf(train1, lags=36, zero=False, ax=ax2, title='Plot PACF 1st Order Differencing');

pip install pmdarima

import pmdarima as pm

# Seasonal - fit stepwise auto-ARIMA
smodel = pm.auto_arima(train1, start_p=2, start_q=2,
                         test='adf',
                         max_p=2, max_q=2, m=12,
                         start_P=2, seasonal=True,
                         d=None, D=1, trace=True,
                         error_action='ignore',  
                         suppress_warnings=True, 
                         stepwise=True)

smodel.summary()

"""Diperoleh model terbaik yaitu ARIMA(1,0,2)(1,1,1)[12].
Selanjutnya kita akan menguji kinerja model dengan melihat persentase errornya, semakin kecil errornya semakin baik pula kinerjanya
"""

from statsmodels.tsa.statespace.sarimax import SARIMAX
model = SARIMAX(train1, order=(1,0,2),seasonal_order=(1,1,1,12))
model_fit = model.fit(disp=-1)
print(model_fit.summary())

# Plot residual errors
model_fit.plot_diagnostics(figsize=(7,5))

# Forecast
forecast = model_fit.forecast(36)
actual = test

from statsmodels.tsa.stattools import acf

# Accuracy metrics
def forecast_accuracy(forecast, actual):
    mape = np.mean(np.abs(forecast - actual)/np.abs(actual))  # MAPE
    me = np.mean(forecast - actual)             # ME
    mae = np.mean(np.abs(forecast - actual))    # MAE
    mpe = np.mean((forecast - actual)/actual)   # MPE
    rmse = np.mean((forecast - actual)**2)**.5  # RMSE
    corr = np.corrcoef(forecast, actual)[0,1]   # corr
    mins = np.amin(np.hstack([forecast[:,None], 
                              actual[:,None]]), axis=1)
    maxs = np.amax(np.hstack([forecast[:,None], 
                              actual[:,None]]), axis=1)
    minmax = 1 - np.mean(mins/maxs)             # minmax
    acf1 = acf(fc-test)[1]                      # ACF1
    return({'mape':mape, 'me':me, 'mae': mae, 
            'mpe': mpe, 'rmse':rmse, 'acf1':acf1, 
            'corr':corr, 'minmax':minmax})

forecast_accuracy(fc, test.values)

"""Diperoleh error yang cukup kecil, dimana pada uji ini kita cukup melihat nilai MAPE nya saja sebagai ukuran ketepatan peramalan, dimana disitu nilai MAPE = 1,24% yang artinya kinerja model sangat baik dimana berada dibawah 10%.
Sehingga selanjutnya dilakukan peramalan dengan data asli.
"""

from statsmodels.tsa.statespace.sarimax import SARIMAX
mod = SARIMAX(df1['keuntungan'], order=(1,0,2),seasonal_order=(1,1,1,12))
results = mod.fit()

pred_uc = results.get_forecast(steps=36)
pred_ci = pred_uc.conf_int()
ax = df1['keuntungan'].plot(label='Data Aktual Selama 10 Tahun', figsize=(14, 7))
pred_uc.predicted_mean.plot(ax=ax, label='Prediksi 3 Tahun ke Depan')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Periode')
ax.set_ylabel('Keuntungan')
plt.title('Prediksi Keuntungan 3 Tahun Mendatang')
plt.legend()
plt.show()

"""Terlihat pada plot, keuntungan 3 tahun kedepan mengalami fluktuasi yang sama seperti periode sebelumnya, yaitu mencapai keuntungan max di akhir tahun kemudian kembali ke rata-rata, hal ini perlu diperhatikan untuk menstabilkan keuntungan max di masa mendatang."""
