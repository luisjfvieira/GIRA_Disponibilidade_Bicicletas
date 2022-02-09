# GIRA - Extrair disponibilidade bicicletas

#### Manuel Banza - February, 2022


import requests
import pandas as pd
import datetime
import time

url = 'http://coiapp.cm-lisboa.pt/api/opendata/public/download/53616c7465645f5f62a975d9194dd0ee7a0d7ffb4f36b0c0b5161a94daf4ed0e.csv?format=csv'
df = pd.read_csv(url, encoding='utf8')
print(len(df))

# Passar para date e criar coluna datetime
df['add_data'] = pd.to_datetime(df['add_data'], format='%Y-%m-%d')
df['datetime'] = df['add_data'].astype(str) + ' ' + df['add_hora'].astype(str)
df['datetime'] = pd.to_datetime(df['datetime'])

# Limpar coluna com coordenadas
df['position'] = df['position'].astype(str)
df['position'] = df['position'].str[17:]
df['position'] = df['position'].str[:20]
df['position'] = df['position'].str.replace('],', '')

# cirar latitude e longitude
df[['longitude', 'latitude']] = df['position'].str.split(', ', expand=True)

# Eliminar coluna position
df = df.drop(columns=['position'])


from datetime import datetime, timedelta

yesterday = datetime.now() - timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d')

df = df.loc[df['add_data']>=yesterday]


# Exportar
from datetime import datetime
df.to_csv(datetime.now().strftime('data_sources/data_transformed/gira_disponibilidade-%Y-%m-%d-%H-%M-%S.csv'), encoding='utf8', index=False)