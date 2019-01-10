# -*- coding: utf-8 -*-

import pandas as pd
from pandas import read_csv

xls = pd.ExcelFile("dadesmeteo.xlsx")

meteoBaells = xls.parse('CR la Quar') #2 is the sheet number
meteoSau = xls.parse('WS Viladrau') #2 is the sheet number
plujaSau = xls.parse('KE Pantà de Sau') #2 is the sheet number


meteoBaells['Dia'] = pd.to_datetime(meteoBaells['DATA_LECTURA'], format='%Y/%m/%d')


dadesSau = read_csv('dadesSau.csv', sep=';',header=0, index_col=0)
volumSau = pd.DataFrame(dadesSau.loc[dadesSau.index >= '2007-01-01']['Volum'])
dadesBaells = read_csv('dadesBaells.csv', sep=';',header=0, index_col=0)
volumBaells = pd.DataFrame(dadesBaells.loc[dadesBaells.index >= '2007-01-01']['Volum'])


meteoBaells = meteoBaells.loc[:,['DATA_LECTURA', 'TM','TX','TN','HRM','PPT24h','PM']]
meteoSau = meteoSau.loc[:,['DATA_LECTURA', 'TM','TX','TN','HRM','PPT24h','PM']]

meteoSau['Dia'] = pd.to_datetime(meteoSau['DATA_LECTURA'], format='%Y/%m/%d')
meteoSau = meteoSau.set_index(meteoSau['Dia'])
plujaSau['Dia'] = pd.to_datetime(plujaSau['DATA_LECTURA'], format='%Y/%m/%d')
plujaSau = plujaSau.set_index(plujaSau['Dia'])

plujaSau = plujaSau.loc[:,['PPT24h']]

plujaSau.columns = ['PPT']

sauConjunt = pd.concat([meteoSau, plujaSau], axis=1)

print(meteoBaells.isna().sum())

sauConjunt['PPT'] = sauConjunt['PPT'].fillna(sauConjunt['PPT24h'])

print(sauConjunt.isna().sum())

# Corregim dades
indexNul = meteoBaells[meteoBaells['PPT24h'].isnull()].index.tolist()
meteoBaells.at[indexNul, 'PPT24h'] = 0

indexNul = meteoBaells[meteoBaells['TM'].isnull()].index.tolist()
meteoBaells.at[indexNul, 'TM']=(meteoBaells.loc[indexNul[0]-1]['TM']+meteoBaells.loc[indexNul[1]+1]['TM'])/2

indexNul = meteoBaells[meteoBaells['TX'].isnull()].index.tolist()
meteoBaells.at[indexNul, 'TX']=(meteoBaells.loc[indexNul[0]-1]['TX']+meteoBaells.loc[indexNul[0]+1]['TX'])/2

indexNul = meteoBaells[meteoBaells['TN'].isnull()].index.tolist()
meteoBaells.at[indexNul, 'TN']=(meteoBaells.loc[indexNul[0]-1]['TN']+meteoBaells.loc[indexNul[0]+1]['TN'])/2

indexNul = meteoBaells[meteoBaells['HRM'].isnull()].index.tolist()
meteoBaells.at[indexNul, 'HRM']=(meteoBaells.loc[indexNul[0]-1]['HRM']+meteoBaells.loc[indexNul[1]+1]['HRM'])/2

indexNul = meteoBaells[meteoBaells['PM'].isnull()].index.tolist()
meteoBaells.at[indexNul, 'PM']=(meteoBaells.loc[indexNul[0]-1]['PM']+meteoBaells.loc[indexNul[1]+1]['PM'])/2

print(meteoBaells.isna().sum())

sauDades = sauConjunt.loc[:,['DATA_LECTURA', 'TM','TX','TN','HRM','PPT','PM']]
sauDades['Dia'] = pd.to_datetime(sauDades['DATA_LECTURA'], format='%Y/%m/%d')
sauDades = sauDades.set_index(meteoSau['Dia'])
sauDades = sauConjunt.loc[:,['Dia', 'TM','TX','TN','HRM','PPT','PM']]
sauDades['Volum']=volumSau['Volum']

sauDadesDF_CSV = sauDades
sauDadesDF_CSV = sauDadesDF_CSV.set_index(sauDades['Dia'])
sauDadesDF_CSV.to_csv('dadesSauMultiDia.csv', sep=';', encoding='utf-8')
sauDadesDF_CSV_SD = sauDadesDF_CSV.drop('Dia', 1)

sauDadesDF_CSV_SD.to_csv('dadesSauMulti.csv', sep=';', encoding='utf-8')


meteoBaells['PPT'] = meteoBaells['PPT24h']
baellsDades = meteoBaells.loc[:,['DATA_LECTURA', 'TM','TX','TN','HRM','PPT','PM']]
baellsDades['Dia'] = pd.to_datetime(meteoBaells['DATA_LECTURA'], format='%Y/%m/%d')
baellsDades = baellsDades.set_index(baellsDades['Dia'])
baellsDades = baellsDades.loc[:,['Dia', 'TM','TX','TN','HRM','PPT','PM']]
baellsDades['Volum']=volumBaells['Volum']

baellsDadesDF_CSV = baellsDades
baellsDadesDF_CSV = baellsDadesDF_CSV.set_index(baellsDades['Dia'])
baellsDadesDF_CSV.to_csv('dadesBaellsMultiDia.csv', sep=';', encoding='utf-8')
baellsDadesDF_CSV_SD = baellsDadesDF_CSV.drop('Dia', 1)

baellsDadesDF_CSV_SD.to_csv('dadesBaellsMulti.csv', sep=';', encoding='utf-8')



def grafica_series(graf):
    
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    plt.style.use('seaborn-whitegrid')
    
    fig, ax = plt.subplots(nrows=7, ncols=1, sharex=True, figsize=(20,20))
    
    for row, dades_graf in zip(ax, graf):
        dies = dades_graf[0]
        valors = dades_graf[1]
        titol = dades_graf[2]
        unitats = dades_graf[3]
        row.plot(dies, valors)
              
        #set ticks every week0
        row.xaxis.set_major_locator(mdates.YearLocator())
        #set major ticks format
        row.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            
        row.set_ylabel(unitats, fontsize=15)
        row.set_title(titol, fontsize=15)
        ttl = row.title
        ttl.set_position([.5, 1.03])
        for tick in row.xaxis.get_major_ticks():
            tick.label.set_fontsize(14) 
        
        for tick in row.yaxis.get_major_ticks():
            tick.label.set_fontsize(14) 
        
        plt.xticks(rotation=90)
        
        
    plt.show()

var_graf = ((baellsDades['Dia'], baellsDades["PPT"], 'Precipitació 24h','$l/m^2$'),(baellsDades['Dia'], baellsDades["TM"], 'Temperatura mitjana','ºC'),
               (baellsDades['Dia'], baellsDades["TX"], 'Temperatura màxima diària','ºC'),(baellsDades['Dia'], baellsDades["TN"], 'Temperatura mínima diària','ºC'),
               (baellsDades['Dia'], baellsDades["HRM"], 'Humitat relativa mitjana diària','%'), (baellsDades['Dia'], baellsDades["PM"], 'Pressió atmosfèrica mitjana diària','hPa'),
               (baellsDades['Dia'], baellsDades["Volum"], 'Volum aigua','$hm^3$'))
grafica_series(var_graf)


var_graf = ((sauDades['Dia'], sauDades["PPT"], 'Precipitació 24h','$l/m^2$'),(sauDades['Dia'], sauDades["TM"], 'Temperatura mitjana','ºC'),
               (sauDades['Dia'], sauDades["TX"], 'Temperatura màxima diària','ºC'),(sauDades['Dia'], sauDades["TN"], 'Temperatura mínima diària','ºC'),
               (sauDades['Dia'], sauDades["HRM"], 'Humitat relativa mitjana diària','%'), (sauDades['Dia'], sauDades["PM"], 'Pressió atmosfèrica mitjana diària','hPa'),
               (sauDades['Dia'], sauDades["Volum"], 'Volum aigua','$hm^3$'))
grafica_series(var_graf)

