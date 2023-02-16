### 1a. SPATIAL JOIN - EUBUCCO AND OECD FUA BOUNDARIES

import psycopg2
import geopandas as gpd
from sshtunnel import SSHTunnelForwarder
import paramiko
import io

# Load private key
with open('C:/Users/charl/OneDrive/Bureau/PrivateKey3', 'r') as f:
    key = f.read()
    pkey = paramiko.RSAKey.from_private_key(io.StringIO(key))

with SSHTunnelForwarder(('194.163.151.34', 22), ssh_username='flo', remote_bind_address=('172.30.0.4', 5432), ssh_pkey= pkey) as server:
    
    server.start()
    print('Server connected.')

    params = {
        'database': 'eubucco',
        'user': 'NvWkXLveTsmzpuuhXdewHwavJFSsSoVa',
        'password': 'sUur5w7PHUufrRqWvcilJ5Gvxk5TbdAu3cLv9gWXWqd6P1GTTqKqZGgexwtpB6eQ',
        'host': 'localhost',
        'port': server.local_bind_port,
        'connect_timeout': 10,
        }

    conn = psycopg2.connect(**params)
    conn.set_session(readonly=True)
    curs = conn.cursor()
    print('Database connected.')

    sql = 'SELECT * FROM data_country;'
    data = gpd.GeoDataFrame.from_postgis(
        sql=sql,
        con=conn,
        geom_col='geometry', 
        index_col='id', 
        )
    print('Data retrieved.')

data