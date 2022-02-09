# GIRA - Extrair disponibilidade bicicletas 

## EMEL OPEN DATA

#### Manuel Banza - February, 2022


import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd
import datetime
import time

# Obter dados do emel open data: https://emel.city-platform.com/opendata/

url = "https://emel.city-platform.com/opendata/gira/station/list"

headers = CaseInsensitiveDict()
headers["accept"] = "application/json"
headers["api_key"] = "f90859a793cda8a701dd7c25adf5ae2c"


resp = requests.get(url, headers=headers)

#print(resp.status_code)

json = resp.json()
results = json['features']

df = pd.DataFrame(results)
df = df[['properties']]


df = pd.json_normalize(df['properties'])

# Passar para date e criar coluna datetime
df['update_date'] = df['update_date'].astype(str).str[:-1]
df['update_date'] = pd.to_datetime(df['update_date'], format='%Y-%m-%dT%H:%M:%S')
df['update_date_hour'] = df['update_date'].dt.hour
df['update_date_only'] = df['update_date'].dt.date

# cirar latitude e longitude
df['bbox'] = df['bbox'].astype(str).str.replace(']', '')
df['bbox'] = df['bbox'].astype(str).str.replace('[', '')
df[['longitude', 'latitude', 'lon2', 'lat2']] = df['bbox'].str.split(', ', expand=True)

# Eliminar coluna position
df = df.drop(columns=['lon2', 'lat2'])

df.head()


# Exportar
from datetime import datetime
df.to_csv(datetime.now().strftime('data_sources/data_transformed/gira_disponibilidade_emel_opendata-%Y-%m-%d-%H-%M-%S.csv'), encoding='utf8', index=False)