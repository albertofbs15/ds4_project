import os
import pandas as pd
import numpy as np


def clean_address1(x):
    xlist=x.split()
    xnew=list()
    for i in range(len(xlist)):
        curi=xlist[i]
        if curi in ['CL','CLL','CLLE','CCLLE','CALLE']:
            curi='C'
        elif curi in ['CR','CARRERA','CRA']:
            curi='K'
        elif curi in ['AVENIDA','AV']:
            curi='AV'
        elif curi=="VIA":
            curi="VIA"
        else:
            continue
        
        if i==len(xlist)-1:
            continue
        curx="".join([curi,xlist[i+1]])
        xnew.append(curx)
    
    return(" ".join(xnew))

def clean_address2(x):
    xlist=x.split()
    xnew=list()
    for i in range(len(xlist)):
        curi=xlist[i]
        if curi in ['CL','CLL','CLLE','CCLLE','CALLE']:
            curi='C'
        elif curi in ['CR','CARRERA','CRA']:
            curi='K'
        elif curi in ['AVENIDA','AV']:
            curi='AV'

        xnew.append(curi)
    
    return("".join(xnew))

def load_data():
    # Read CSV file
    if(os.path.isfile('src/data/filtered_data.csv')):
        df = pd.read_csv('src/data/Final_Final.csv', encoding = "utf-8")
        df.rename(columns={'Unnamed: 0':'ID'})
        df['year']=df['AÑO_ACCIDENTE']
        trafico=np.linspace(min(df['TRAFICO']),max(df['TRAFICO']),4)
        df['C_TRAFICO']=[0 if i<trafico[1] else (1 if i<trafico[2] else 2) for i in df['TRAFICO']]
        #df['energy']=df['TRAFICO']
        #df['vel']=df['bus_subidas']
        #df['alt']=df['bus_bajadas']
        df['ID']=df['Unnamed: 0']
        df['impact-e']=df['CANT_HERIDOS_EN _SITIO_ACCIDENTE']
        df['lat']=df['LATITUD']
        df['lon']=df['LONGITUD']
        df['legend']=df['FECHA_ACCIDENTE']
        df['date_time'] = df[['FECHA_ACCIDENTE', 'HORA_ACCIDENTE']].apply(lambda x: ' '.join(x), axis=1)
        df['date_time'] = pd.to_datetime(df['date_time'],format='%Y-%m-%d %I:%M:%S:%p')
        df['hour']=[i.hour for i in df['date_time']]
        df['month']=[i.month for i in df['date_time']]
        df['month_name']=[i.month_name() for i in df['date_time']]
        df['day of week']=[i.dayofweek for i in df['date_time']]
        df['day']=[i.day for i in df['date_time']]
        df['day_name']=[i.day_name() for i in df['date_time']]
        df['address']=[i.upper() for i in df['SITIO_EXACTO_ACCIDENTE']]
        df['address']=df['address'].apply(clean_address2)
        pieza_code={
            'riomar':0.1,
            'prado norte': 0.2,
            'suroccidental 2': 0.3,
            'centro carrera 38': 0.4,
            'centro metropolitana': 0.5,
            'suroriental': 0.6,
            'suroccidental 1': 0.7,
            'ribera occidental': 0.8
        }
        pieza_relative={
            'riomar':0.1723,
            'prado norte': 0.0906,
            'suroccidental 2': 0.1496,
            'centro carrera 38': 0.1034,
            'centro metropolitana': 0.0507,
            'suroriental': 0.1360,
            'suroccidental 1': 0.1236,
            'ribera occidental': 0.1737,
        },
        pot_code={
            'residencial': 0.2,
            'comercial':0.1,
            'protegida': 0.6,
            'portuaria': 0.4,
            'industrial': 0.7,
            'central': 0.5,
            'público': 0.8,
            'institucional':0.3
        }
        pot_relative={
            'residencial': 0.4392,
            'comercial':0.1081,
            'protegida': 0.1694,
            'portuaria': 0.0576,
            'industrial': 0.0870,
            'central': 0.0372,
            'público': 0.0457,
            'institucional':0.0557
        }
    else:
        df = pd.read_csv('src/data/fireballs.csv')
        df = process_df(df)
        df.to_csv('src/data/filtered_data.csv', index=False)
    
    return df

