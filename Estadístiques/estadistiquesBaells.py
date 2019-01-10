# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 23:41:26 2018

@author: Jordi
"""
import loadSau
import labaells
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.stattools import acf, pacf
import numpy as np


baellsDades = labaells.labaellsTotDF

# Descomposició sèrie temporal
descomp_serie = sm.tsa.seasonal_decompose(baellsDades['Volum'], model='additive', freq=365)  

var_graf = ((baellsDades['Dia'], descomp_serie.observed, 'Volum la Baells','$hm^3$'),(baellsDades['Dia'], descomp_serie.trend, 'Tendència','$hm^3$'),
               (baellsDades['Dia'], descomp_serie.seasonal, 'Component estacionària','$hm^3$'),(baellsDades['Dia'], descomp_serie.resid, 'Component residual','$hm^3$'))

loadSau.grafica_series_multi(var_graf)

# Descomposició sèrie temporal
descomp_serie2007 = sm.tsa.seasonal_decompose(baellsDades['Volum'][baellsDades['Dia']>='2007-10-01'], model='additive', freq=365)  

var_graf2007 = ((baellsDades['Dia'][baellsDades['Dia']>='2007-10-01'], descomp_serie2007.observed, 'Volum la Baells','$hm^3$'),(baellsDades['Dia'][baellsDades['Dia']>='2007-10-01'], descomp_serie2007.trend, 'Tendència','$hm^3$'),
               (baellsDades['Dia'][baellsDades['Dia']>='2007-10-01'], descomp_serie2007.seasonal, 'Component estacionària','$hm^3$'),(baellsDades['Dia'][baellsDades['Dia']>='2007-10-01'], descomp_serie2007.resid, 'Component residual','$hm^3$'))

loadSau.grafica_series_multi(var_graf2007)


# Test d'estacionalitat
from statsmodels.tsa.stattools import adfuller
def test_stationarity(timeseries):
    
    #Perform Dickey-Fuller test:
    print ('Resultats del test de Dickey-Fuller:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)
    
# Test d'estacionalitat del volum i dels residus
test_stationarity(baellsDades['Volum'])
descomp_serie.resid.dropna(inplace=True)
test_stationarity(descomp_serie.resid)

#Histogrma
plt.rcParams.update({'font.size': 15})
plt.figure(1, figsize=(15, 5))
plt.subplots_adjust(hspace=0.5)
plt.subplots_adjust(wspace=0.2)
plt.subplot(121)
plt.title('Histograma volum la Baells')
baellsDades['Volum'].hist(bins=20)
plt.xlabel('volum ($hm^3$)')
plt.subplot(122)
plt.title('Funció densitat de probabilitat')
baellsDades['Volum'].plot(kind='kde')
plt.xlabel('volum ($hm^3$)')
plt.show()


# Autocorrelació i autocorrelació parcial
lag_acf = acf(baellsDades['Volum'], nlags=50)
lag_pacf = pacf(baellsDades['Volum'], nlags=50)

plt.rcParams.update({'font.size': 15})
plt.figure(1, figsize=(15, 5))
plt.subplots_adjust(hspace=0.5)
plt.subplots_adjust(wspace=0.2)
fig, ax = plt.subplots(nrows=1, ncols=2,figsize=(15,5))
ax[0].plot(lag_acf)
ax[0].axhline(y=0,linestyle='--',color='gray')
ax[0].axhline(y=-1.96/np.sqrt(len(baellsDades['Volum'])),linestyle='--',color='gray')
ax[0].axhline(y=1.96/np.sqrt(len(baellsDades['Volum'])),linestyle='--',color='gray')
ax[0].set_title("Funció d'autocorrelació",fontsize=15)

for tick in ax[0].xaxis.get_major_ticks():
    tick.label.set_fontsize(15) 

#Plot PACF:
ax[1].plot(lag_pacf)
ax[1].axhline(y=0,linestyle='--',color='gray')
ax[1].axhline(y=-1.96/np.sqrt(len(baellsDades['Volum'])),linestyle='--',color='gray')
ax[1].axhline(y=1.96/np.sqrt(len(baellsDades['Volum'])),linestyle='--',color='gray')
ax[1].set_title("Funció d'autocorrelació parcial", fontsize=15)
ax[1].set_xticks(np.arange(0, 51, 5))

for tick in ax[1].xaxis.get_major_ticks():
    tick.label.set_fontsize(15)

plt.show()


# Agrupem per mitjanes mensuals
volumSau = pd.DataFrame(baellsDades['Volum'])
volumSau = volumSau.set_index(pd.DatetimeIndex(baellsDades['Dia']))
volumSauMonth = volumSau.resample('M', how='mean')

mesoshidro=[]

for x in range (1986,2018):
    inici=str(x)+'-10-01'
    fi=str(x+1)+'-09-30'
    a=volumSauMonth.loc[inici:fi]
    mesoshidro.append(a['Volum'].tolist())
    
mesosDF = pd.DataFrame(mesoshidro).T
mesosDF.columns=['1986','1987','1988','1989','1990','1991','1992','1993','1994','1995','1996',
                 '1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007',
                 '2008','2009','2010','2011','2012','2013','2014','2015','2016','2017']
mesosDF['mesos'] = ['octubre', 'novembre', 'desembre', 'gener', 'febrer', 'març', 'abril', 'maig', 'juny', 'juliol', 'agost', 'setembre']

mesosDF = mesosDF.set_index(mesosDF['mesos'])
mesosDF = mesosDF.drop('mesos', 1)

summaryAnys = mesosDF.describe()
#summary = summary.transpose()
display(summaryAnys)

# Taula de mitjanes per mesos, desviació estàndard i coeficients estacionals
mesosDF2=mesosDF
mesosDF['mean'] = mesosDF2.mean(axis=1)
mesosDF['std']=mesosDF2.std(axis=1)

mitjana = mesosDF['mean'].mean()
mesosDF['coef_estac']= mesosDF['mean'].map(lambda x: x-mitjana)
del mesosDF.index.name
display(mesosDF[0:6])
display(mesosDF.iloc[:,0:7])
display(mesosDF.iloc[:,7:14])
display(mesosDF.iloc[:,14:21])
display(mesosDF.iloc[:,21:28])
display(mesosDF.iloc[:,28:35])


mesosDFT=mesosDF.iloc[:,0:32]
mesosDFT=mesosDFT.T
fig, ax = plt.subplots(nrows=1, ncols=1,figsize=(15,15))
ax.plot(mesosDFT)
ax.set_title('Mitjanes volum per mesos',fontsize=15)
ax.legend()

for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(14) 
for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(14) 
    
plt.xticks(rotation=90)

plt.show()


# Agrupem per mitjanes trimestral
volumSauTri = pd.DataFrame(baellsDades['Volum'])
volumSauTri = volumSauTri.set_index(pd.DatetimeIndex(baellsDades['Dia']))
volumSauTri = volumSauTri.resample('Q', how='mean')

trimestrehidro=[]

for x in range (1986,2018):
    inici=str(x)+'-10-01'
    fi=str(x+1)+'-09-30'
    a=volumSauTri.loc[inici:fi]
    trimestrehidro.append(a['Volum'].tolist())
    
trimestresDF = pd.DataFrame(trimestrehidro).T
trimestresDF.columns=['1986','1987','1988','1989','1990','1991','1992','1993','1994','1995','1996',
                 '1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007',
                 '2008','2009','2010','2011','2012','2013','2014','2015','2016','2017']
trimestresDF['trimestre'] = ['oct-des', 'gen-mar', 'abr-jun', 'jul-set']

trimestresDF = trimestresDF.set_index(trimestresDF['trimestre'])
trimestresDF = trimestresDF.drop('trimestre', 1)

summaryTri = trimestresDF.describe()
#summary = summary.transpose()
display(summaryTri)

# Taula de mitjanes per mesos, desviació estàndard i coeficients estacionals
triDF2=trimestresDF
trimestresDF['mean'] = triDF2.mean(axis=1)
trimestresDF['std']= triDF2.std(axis=1)

mitjana = trimestresDF['mean'].mean()
trimestresDF['coef_estac']= trimestresDF['mean'].map(lambda x: x-mitjana)

del trimestresDF.index.name

display(trimestresDF[0:10])
display(trimestresDF.iloc[:,0:10])
display(trimestresDF.iloc[:,10:20])
display(trimestresDF.iloc[:,20:30])
display(trimestresDF.iloc[:,30:35])


trimestresDFT=trimestresDF.iloc[:,0:32]
trimestresDFT=trimestresDFT.T
fig, ax = plt.subplots(nrows=1, ncols=1,figsize=(15,15))
ax.plot(trimestresDFT)
ax.set_title('Mitjanes volum per trimestres',fontsize=15)

for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(14) 
for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(14) 
    
plt.xticks(rotation=90)
plt.legend(trimestresDFT.columns, loc=4)
plt.show()

summaryToT = baellsDades.describe()
#summary = summary.transpose()
display(summaryTri)

