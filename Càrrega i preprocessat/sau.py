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

print(df[:10])


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
    
for var in variables:
    nom='df' + str(var)
    print(var)
    print (d[nom]['Descripcio_Variable'][:1])

variables1986 =  df1986.Variable.unique()
d1986 = {}

for var in variables1986:
    d1986['df' + str(var)] = df1986[df1986.Variable==var]
    
for var in variables1986:
    nom='df' + str(var)
    print(var)
    print (d1986[nom]['Descripcio_Variable'][:1])

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

grafica_series(grup12DF['Dia'], grup12DF["Grup12"], 'Grup 1 +2','$m^3/s$')

grafica_series(sauTotDF['Dia'], sauTotDF["Nivell"], 'Nivell aigua Sau','m.s.n.m.')
grafica_series(sauTotDF['Dia'], sauTotDF["Volum"], 'Volum aigua Sau','$hm^3$')
grafica_series(sauTotDF['Dia'], sauTotDF["Percent"], '% volum Sau','% volum')
grafica_series(sauTotDF['Dia'], sauTotDF["Entrada"], 'Cabal entrada Sau','$m^3/s$')
grafica_series(sauTotDF['Dia'], sauTotDF["Sortida"], 'Cabal sortida Sau','$m^3/s$')

v9=[entradaDF['Entrada'].count(), entradaDF['Entrada'].isna().sum(), sau2007DF['Entrada'].isna().sum(), entradaDF['Dia'].min().strftime('%Y-%m-%d'), entradaDF['Dia'].max().strftime('%Y-%m-%d')]
v10=[sortidaDF['Sortida'].count(), sortidaDF['Sortida'].isna().sum(), sau2007DF['Sortida'].isna().sum(),  sortidaDF['Dia'].min().strftime('%Y-%m-%d'), sortidaDF['Dia'].max().strftime('%Y-%m-%d')]
v6=[volumDF['Volum'].count(), volumDF['Volum'].isna().sum(), sau2007DF['Volum'].isna().sum(), volumDF['Dia'].min().strftime('%Y-%m-%d'), volumDF['Dia'].max().strftime('%Y-%m-%d')]
v7=[nivellDF['Nivell'].count(), nivellDF['Nivell'].isna().sum(), sau2007DF['Nivell'].isna().sum(), nivellDF['Dia'].min().strftime('%Y-%m-%d'), nivellDF['Dia'].max().strftime('%Y-%m-%d')]
v8=[percentDF['Percent'].count(), percentDF['Percent'].isna().sum(), sau2007DF['Percent'].isna().sum(), percentDF['Dia'].min().strftime('%Y-%m-%d'), percentDF['Dia'].max().strftime('%Y-%m-%d')]

v4=[entrada1986DF['Entrada'].count(), entrada1986DF['Entrada'].isna().sum(), sau1986DF['Entrada'].isna().sum(), entrada1986DF['Dia'].min().strftime('%Y-%m-%d'), entrada1986DF['Dia'].max().strftime('%Y-%m-%d')]
v5=[sortida1986DF['Sortida'].count(), sortida1986DF['Sortida'].isna().sum(), sau1986DF['Sortida'].isna().sum(), sortida1986DF['Dia'].min().strftime('%Y-%m-%d'), sortida1986DF['Dia'].max().strftime('%Y-%m-%d')]
v1=[volum1986DF['Volum'].count(), volum1986DF['Volum'].isna().sum(), sau1986DF['Volum'].isna().sum(), volum1986DF['Dia'].min().strftime('%Y-%m-%d'), volum1986DF['Dia'].max().strftime('%Y-%m-%d')]
v2=[nivell1986DF['Nivell'].count(), nivell1986DF['Nivell'].isna().sum(), sau1986DF['Nivell'].isna().sum(), nivell1986DF['Dia'].min().strftime('%Y-%m-%d'), nivell1986DF['Dia'].max().strftime('%Y-%m-%d')]
v3=[percent1986DF['Percent'].count(), percent1986DF['Percent'].isna().sum(), sau1986DF['Percent'].isna().sum(), percent1986DF['Dia'].min().strftime('%Y-%m-%d'), percent1986DF['Dia'].max().strftime('%Y-%m-%d')]

v11=[grup12DF['Grup12'].count(), grup12DF['Grup12'].isna().sum(), sau2007DF['Grup12'].isna().sum(), grup12DF['Dia'].min().strftime('%Y-%m-%d'), grup12DF['Dia'].max().strftime('%Y-%m-%d')]
varsauDF = pd.DataFrame(list(zip(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11)),
              columns=['Volum 1986', 'Nivell 1986', 'Percent 1986', 'Entrada 1986', 'Sortida 1986', 'Volum 2007', 'Nivell 2007', 'Percent 2007', 'Entrada 2007', 'Sortida 2007', 'Cabals grup 1+2'])

varsauDF = varsauDF.transpose()
varsauDF.columns = ['Num observacions', 'Valors nuls', 'Nuls interval','Dia inici', 'Dia fi']
display(varsauDF)
