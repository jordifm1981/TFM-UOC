# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 09:40:41 2018

@author: Jordi
"""

import pandas as pd
import xml.etree.ElementTree as ET
tree = ET.parse('sau-2007-2018.xml')
root = tree.getroot()

dades = root.find('.//DATA_PROVIDER[@NAME="GRH"]')
data = []
for rows in dades.findall('ROW'):
    temp = []
    for cell in rows:
        temp.append(cell.text)
    data.append(temp)
    
df=pd.DataFrame(data,columns=['Dia', 'Variable', 'Mitjana', 'Descripcio_Variable', 'Unitat_Mesura', 'Estacio', 'UTM_X', 'UTM_Y', 'Dia_Format_Data', 'Mitjana_Dia', 'Conca'])

df = df.sort_values(by=['Dia'])

tree1986 = ET.parse('sau-1986-2006.xml')
root1986 = tree1986.getroot()

dades1986 = root1986.find('.//DATA_PROVIDER[@NAME="GRH"]')
data1986 = []
for rows in dades1986.findall('ROW'):
    temp = []
    for cell in rows:
        temp.append(cell.text)
    data1986.append(temp)

df1986=pd.DataFrame(data1986,columns=['Dia', 'Variable', 'Mitjana', 'Descripcio_Variable', 'Unitat_Mesura', 'Estacio', 'UTM_X', 'UTM_Y', 'Dia_Format_Data', 'Mitjana_Dia', 'Conca'])
df1986 = df1986.sort_values(by=['Dia'])
df1986 = df1986[df1986['Dia']>='1986-01-01']

variables =  df.Variable.unique()
d = {}

for var in variables:
    d['df' + str(var)] = df[df.Variable==var]
    

variables1986 =  df1986.Variable.unique()
d1986 = {}

for var in variables1986:
    d1986['df' + str(var)] = df1986[df1986.Variable==var]
    
grup12DF = pd.DataFrame(d['df3378678']['Dia'])
grup12DF['Grup12']=pd.DataFrame(d['df3378678']['Mitjana'])
grup12DF["Grup12"] = pd.to_numeric(grup12DF["Grup12"])
grup12DF['Dia'] = pd.to_datetime(grup12DF['Dia'], format='%Y/%m/%d')

volumDF = pd.DataFrame(d['df4159510']['Dia'])
volumDF['Volum']=pd.DataFrame(d['df4159510']['Mitjana'])
volumDF["Volum"] = pd.to_numeric(volumDF["Volum"])
volumDF['Dia'] = pd.to_datetime(volumDF['Dia'], format='%Y/%m/%d')

nivellDF = pd.DataFrame(d['df4159509']['Dia'])
nivellDF['Nivell']=pd.DataFrame(d['df4159509']['Mitjana'])
nivellDF["Nivell"] = pd.to_numeric(nivellDF["Nivell"])
nivellDF['Dia'] = pd.to_datetime(nivellDF['Dia'], format='%Y/%m/%d')

sau2007DF = pd.merge(volumDF, nivellDF, how='left', on=['Dia'])

percentDF = pd.DataFrame(d['df4159547']['Dia'])
percentDF['Percent']=pd.DataFrame(d['df4159547']['Mitjana'])
percentDF["Percent"] = pd.to_numeric(percentDF["Percent"])
percentDF['Dia'] = pd.to_datetime(percentDF['Dia'], format='%Y/%m/%d')

sau2007DF = pd.merge(sau2007DF, percentDF, how='left', on=['Dia'])

entradaDF = pd.DataFrame(d['df4165141']['Dia'])
entradaDF['Entrada']=pd.DataFrame(d['df4165141']['Mitjana'])
entradaDF["Entrada"] = pd.to_numeric(entradaDF["Entrada"])
entradaDF['Dia'] = pd.to_datetime(entradaDF['Dia'], format='%Y/%m/%d')

sau2007DF = pd.merge(sau2007DF, entradaDF, how='left', on=['Dia'])

sortidaDF = pd.DataFrame(d['df4165140']['Dia'])
sortidaDF['Sortida']=pd.DataFrame(d['df4165140']['Mitjana'])
sortidaDF["Sortida"] = pd.to_numeric(sortidaDF["Sortida"])
sortidaDF['Dia'] = pd.to_datetime(sortidaDF['Dia'], format='%Y/%m/%d')

sau2007DF = pd.merge(sau2007DF, sortidaDF, how='left', on=['Dia'])
sau2007DF = pd.merge(sau2007DF, grup12DF, how='left', on=['Dia'])

volum1986DF = pd.DataFrame(d1986['df4159510']['Dia'])
volum1986DF['Volum']=pd.DataFrame(d1986['df4159510']['Mitjana'])
volum1986DF["Volum"] = pd.to_numeric(volum1986DF["Volum"])
volum1986DF['Dia'] = pd.to_datetime(volum1986DF['Dia'], format='%Y/%m/%d')

nivell1986DF = pd.DataFrame(d1986['df4159509']['Dia'])
nivell1986DF['Nivell']=pd.DataFrame(d1986['df4159509']['Mitjana'])
nivell1986DF["Nivell"] = pd.to_numeric(nivell1986DF["Nivell"])
nivell1986DF['Dia'] = pd.to_datetime(nivell1986DF['Dia'], format='%Y/%m/%d')

sau1986DF = pd.merge(volum1986DF, nivell1986DF, how='left', on=['Dia'])


percent1986DF = pd.DataFrame(d1986['df4159547']['Dia'])
percent1986DF['Percent']=pd.DataFrame(d1986['df4159547']['Mitjana'])
percent1986DF["Percent"] = pd.to_numeric(percent1986DF["Percent"])
percent1986DF['Dia'] = pd.to_datetime(percent1986DF['Dia'], format='%Y/%m/%d')

sau1986DF = pd.merge(sau1986DF, percent1986DF, how='left', on=['Dia'])

entrada1986DF = pd.DataFrame(d1986['df4165141']['Dia'])
entrada1986DF['Entrada']=pd.DataFrame(d1986['df4165141']['Mitjana'])
entrada1986DF["Entrada"] = pd.to_numeric(entrada1986DF["Entrada"])
entrada1986DF['Dia'] = pd.to_datetime(entrada1986DF['Dia'], format='%Y/%m/%d')

sau1986DF = pd.merge(sau1986DF, entrada1986DF, how='left', on=['Dia'])

sortida1986DF = pd.DataFrame(d1986['df4165140']['Dia'])
sortida1986DF['Sortida']=pd.DataFrame(d1986['df4165140']['Mitjana'])
sortida1986DF["Sortida"] = pd.to_numeric(sortida1986DF["Sortida"])
sortida1986DF['Dia'] = pd.to_datetime(sortida1986DF['Dia'], format='%Y/%m/%d')

sau1986DF = pd.merge(sau1986DF, sortida1986DF, how='left', on=['Dia'])


sauTotDF = sau1986DF.append(sau2007DF)
sauTotDF = pd.concat([sau1986DF,sau2007DF])
sauTotDF = sauTotDF.sort_values(by=['Dia'])
sauTotDF = sauTotDF.reset_index(drop=True)
sauTotDF_CSV = sauTotDF
sauTotDF_CSV = sauTotDF_CSV.set_index(sauTotDF['Dia'])
sauTotDF_CSV = sauTotDF_CSV.drop('Dia', 1)

sauTotDF_CSV.to_csv('dadesSau.csv', sep=';', encoding='utf-8')

def grafica_series(dies, valors, titol, unitats):
    
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    plt.style.use('seaborn-whitegrid')
    
    fig, ax = plt.subplots(figsize=(15,7))
    
    ax.plot(dies, valors)
        
    #set ticks every week0
    ax.xaxis.set_major_locator(mdates.YearLocator())
    #set major ticks format
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        
    ax.set_ylabel(unitats, fontsize=20)
    ax.set_title(titol, fontsize=22)
    ttl = ax.title
    ttl.set_position([.5, 1.03])
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(14) 
    
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(14) 
    
    plt.xticks(rotation=90)
    plt.show()


def grafica_series_multi(graf):
    
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    plt.style.use('seaborn-whitegrid')
    
    mida = len(graf)
    fig, ax = plt.subplots(nrows=mida, ncols=1, sharex=True, figsize=(15,15))
    
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

