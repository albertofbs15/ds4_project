import numpy as np
import pandas as pd
import math
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.formula.api import glm
import collections
from statsmodels.sandbox.stats.multicomp import multipletests
import time
from folium import plugins
import folium
from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime
import os
from calendar import month_name
import datetime

df=pd.read_csv('Final_poisson.csv').iloc[:,1:]
semaforos=pd.read_csv('lights_clean.csv')[['LATITUD','LONGITUD']]
def conteo_perf(newdf=df):
    df_drop=newdf.drop_duplicates(subset='LAT_LON').reset_index(drop=True)
    conteos=newdf[['LAT_LON','SITIO_EXACTO_ACCIDENTE']].groupby(['LAT_LON','SITIO_EXACTO_ACCIDENTE']).size().reset_index(name='count')
    grp_conteos = conteos.groupby('LAT_LON')['count'].agg(['sum','max'])
    grp_conteos['sum_rate'] = grp_conteos['max'] / grp_conteos['sum']
    filtered_conteos = grp_conteos[grp_conteos['sum_rate'] > 0.3]
    return_df = filtered_conteos.drop(['max', 'sum_rate'], axis=1)
    return_df.rename(columns = {'sum':'NACCIDENTS'}, inplace = True) 
    fusion=pd.merge(return_df,df_drop,on='LAT_LON',how='inner')[['NACCIDENTS','AÑO_ACCIDENTE','MES_ACCIDENTE',
                                                     'CLASE_ACCIDENTE','LONGITUD', 'LATITUD',
                                                     'POT', 'PIEZA_URBANA', 'BUS_SUBIDA','BUS_BAJADA', 
                                                     'TRAFICO','ES_FESTIVO','SOLO_HORA','DIA_ACCIDENTE','JUNIOR_JUGO']].reset_index().iloc[:,1:]
    return(fusion)


def distancia_semaforos_mas_rapido(final_df,lights=semaforos):
    closest=np.zeros(final_df.shape[0])
    numclose=np.zeros(final_df.shape[0])
    numclose2=np.zeros(final_df.shape[0])
    numclose3=np.zeros(final_df.shape[0])
    for i in range(final_df.shape[0]):
        corner_lat=final_df['LATITUD'][i]
        corner_lon=final_df['LONGITUD'][i]
        light_lat=np.array(lights['LATITUD'])
        light_lon=np.array(lights['LONGITUD'])
        dx = (light_lon-corner_lon)*40000*np.cos((light_lat+corner_lat)*math.pi/360)/360
        dy = (light_lat-corner_lat)*40000/360
        distance=np.sqrt(dx**2+dy**2)
        closest[i]=distance[distance.argmin()]
        numclose[i]=np.sum(distance<0.1)
        numclose2[i]=np.sum(((distance>=0.1) & (distance<0.5)))
        numclose3[i]=np.sum(((distance>=0.5) & (distance<2)))
    final_df['NLIGHTS']=list(numclose)
    final_df['NLIGHTS2']=list(numclose2)
    final_df['NLIGHTS3']=list(numclose3)
    final_df['CLOSEST_LIGHT']=list(closest)
    return(final_df)

def modelo_poisson(dia=False,mes=False,hora=25, df=df,lights=semaforos,lights_aux=semaforos): #Ojo dia, festivo, mes, año tienen que ser excluyente, si uno es verdadero automaticamente los otros son falsos
        if(mes!=False):
            aux=df[df.MES_ACCIDENTE!=mes].copy()
            df=df[df.MES_ACCIDENTE==mes].reset_index(drop=True)
            conteo_cero=conteo_perf(newdf=aux)
            conteo_cero['NACCIDENTS']=0
            data=conteo_perf(newdf=df)
            data=pd.concat([data,conteo_cero]).reset_index(drop=True)
        if(dia!=False):
            aux=df[df.DIA_ACCIDENTE!=dia].copy()
            df=df[df.DIA_ACCIDENTE==dia].reset_index(drop=True)
            conteo_cero=conteo_perf(newdf=aux)
            conteo_cero['NACCIDENTS']=0
            data=conteo_perf(newdf=df)
            data=pd.concat([data,conteo_cero]).reset_index(drop=True)
        if(hora!=25):
            aux=df[df.SOLO_HORA!=hora].copy()
            df=df[df.SOLO_HORA==hora].reset_index(drop=True)
            conteo_cero=conteo_perf(newdf=aux)
            conteo_cero['NACCIDENTS']=0
            data=conteo_perf(newdf=df)
            data=pd.concat([data,conteo_cero]).reset_index(drop=True)
        if((mes==False)&(dia==False)&(hora==25)):
            data=conteo_perf(newdf=df)            
        data_aux=data.copy()
        data=distancia_semaforos_mas_rapido(final_df=data,lights=lights)
        data_aux=distancia_semaforos_mas_rapido(final_df=data_aux,lights=lights_aux)
        formula='NACCIDENTS~BUS_SUBIDA+BUS_BAJADA+POT+PIEZA_URBANA+NLIGHTS+NLIGHTS2+TRAFICO+CLOSEST_LIGHT'
        model = glm(formula=formula, data=data, family=sm.families.Poisson()).fit()
        data_aux['PREDICHOS']=model.predict(data_aux)   
        data['PREDICHOS']=model.predict()
        return([data[['LATITUD','LONGITUD','PREDICHOS']],data_aux[['LATITUD','LONGITUD','PREDICHOS']]])
        
def mapa_calor_año(lights_aux=semaforos):
    id=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    modelo=modelo_poisson(lights_aux=lights_aux)
    mapa_barranquilla_observados = folium.Map(location=[10.980706, -74.807636],zoom_start=15,tiles="OpenStreetMap")
    mapa_barranquilla_predichos = folium.Map(location=[10.980706, -74.807636],zoom_start=15,tiles="OpenStreetMap")
    mapa_barranquilla_resta = folium.Map(location=[10.980706, -74.807636],zoom_start=15,tiles="OpenStreetMap")
    capa_calor_observados=HeatMap(modelo[0][['LATITUD','LONGITUD','PREDICHOS']],radius=15)
    capa_calor_predichos=HeatMap(modelo[1][['LATITUD','LONGITUD','PREDICHOS']],radius=15)
    mapa_barranquilla_predichos.add_child(capa_calor_predichos)
    mapa_barranquilla_observados.add_child(capa_calor_observados)
    mapa_barranquilla_observados.save('anho_asIs_'+id+'.html')
    mapa_barranquilla_predichos.save('anho_toBe_'+id+'.html')
    anho={}
    anho['conteo_toBe']=round(np.sum(modelo[1]['PREDICHOS']),0)
    anho['conteo_asIs']=round(np.sum(modelo[0]['PREDICHOS']),0)
    anho['id']=id
    anho['key']='Year'
    anho['asIs']='anho_asIs_'+id+'.html'
    anho['toBe']='anho_toBe_'+id+'.html'
    resta=modelo[1][['LATITUD','LONGITUD','PREDICHOS']].copy()
    resta['PREDICHOS']=modelo[1]['PREDICHOS']-modelo[0]['PREDICHOS']
    negativos=resta[resta['PREDICHOS']<0][['LATITUD','LONGITUD']].reset_index(drop=True)
    negativos['PREDICHOS']=1
    positivos=resta[resta['PREDICHOS']>0][['LATITUD','LONGITUD']].reset_index(drop=True)
    positivos['PREDICHOS']=1
    capa_calor_positiva=HeatMap(positivos[['LATITUD','LONGITUD','PREDICHOS']],gradient={0.4: 'orange', 0.65: 'orange', 1: 'orange'},radius=10,min_opacity=0.8,blur=20)
    capa_calor_negativo=HeatMap(negativos[['LATITUD','LONGITUD','PREDICHOS']],gradient={0.4: 'blue', 0.65: 'blue', 1: 'blue'},radius=10,min_opacity=0.8,blur=20)
    mapa_barranquilla_resta.add_child(capa_calor_positiva)
    mapa_barranquilla_resta.add_child(capa_calor_negativo)
    mapa_barranquilla_resta.save('anho_resta_'+id+'.html')
    anho['resta']='anho_resta_'+id+'.html'
    lista=[anho]
    return(lista)

def video_mapa_hora(horas=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],lights_aux=semaforos):
    lista=[]
    id=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    for i in horas:        
        modelo=modelo_poisson(hora=i,lights_aux=lights_aux)
        mapa_barranquilla_observados = folium.Map(location=[10.980706, -74.807636],zoom_start=15,tiles="OpenStreetMap")
        mapa_barranquilla_predichos = folium.Map(location=[10.980706, -74.807636],zoom_start=15,tiles="OpenStreetMap")
        capa_calor_observados=HeatMap(modelo[0][['LATITUD','LONGITUD','PREDICHOS']],radius=15)
        capa_calor_predichos=HeatMap(modelo[1][['LATITUD','LONGITUD','PREDICHOS']],radius=15)
        mapa_barranquilla_predichos.add_child(capa_calor_predichos)
        mapa_barranquilla_observados.add_child(capa_calor_observados)
        mapa_barranquilla_observados.save('hora_'+str(i)+'_asIs_'+id+'.html')
        mapa_barranquilla_predichos.save('hora_'+str(i)+'_toBe_'+id+'.html')
        aux={}
        aux['conteo_toBe']=round(np.sum(modelo[1]['PREDICHOS']),0)
        aux['conteo_asIs']=round(np.sum(modelo[0]['PREDICHOS']),0)
        aux['id']=id
        aux['key']=str(i)
        aux['asIs']='hora_'+str(i)+'_asIs_'+id+'.html'
        aux['toBe']='hora_'+str(i)+'_toBe_'+id+'.html'
        
        mapa_barranquilla_resta = folium.Map(location=[10.980706, -74.807636],zoom_start=15,tiles="OpenStreetMap")
        resta=modelo[1][['LATITUD','LONGITUD','PREDICHOS']].copy()
        resta['PREDICHOS']=modelo[1]['PREDICHOS']-modelo[0]['PREDICHOS']
        negativos=resta[resta['PREDICHOS']<0][['LATITUD','LONGITUD']].reset_index(drop=True)
        negativos['PREDICHOS']=1
        positivos=resta[resta['PREDICHOS']>0][['LATITUD','LONGITUD']].reset_index(drop=True)
        positivos['PREDICHOS']=1
        capa_calor_positiva=HeatMap(positivos[['LATITUD','LONGITUD','PREDICHOS']],gradient={0.4: 'orange', 0.65: 'orange', 1: 'orange'},radius=10,min_opacity=0.8,blur=20)
        capa_calor_negativo=HeatMap(negativos[['LATITUD','LONGITUD','PREDICHOS']],gradient={0.4: 'blue', 0.65: 'blue', 1: 'blue'},radius=10,min_opacity=0.8,blur=20)
        mapa_barranquilla_resta.add_child(capa_calor_positiva)
        mapa_barranquilla_resta.add_child(capa_calor_negativo)
        mapa_barranquilla_resta.save('hora_'+str(i)+'_resta_'+id+'.html')
        aux['resta']='hora_'+str(i)+'_resta_'+id+'.html'
        lista.append(aux)
    return(lista)

def video_mapa_mes(mes=[1,2,3,4,5,6,7,8,9,10,11,12],lights_aux=semaforos):
    lista=[]
    id=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    for i in mes:
        modelo=modelo_poisson(mes=int(i),lights_aux=lights_aux)
        mapa_barranquilla_observados = folium.Map(location=[10.980706, -74.807636],zoom_start=15,tiles="OpenStreetMap")
        mapa_barranquilla_predichos = folium.Map(location=[10.980706, -74.807636],zoom_start=15,tiles="OpenStreetMap",)
        capa_calor_observados=HeatMap(modelo[0][['LATITUD','LONGITUD','PREDICHOS']],radius=15)
        capa_calor_predichos=HeatMap(modelo[1][['LATITUD','LONGITUD','PREDICHOS']],radius=15)
        mapa_barranquilla_predichos.add_child(capa_calor_predichos)
        mapa_barranquilla_observados.add_child(capa_calor_observados)
        
        aux={}
        aux['conteo_toBe']=round(np.sum(modelo[1]['PREDICHOS']),0)
        aux['conteo_asIs']=round(np.sum(modelo[0]['PREDICHOS']),0)
        aux['key']=month_name[int(i)]
        aux['id']=id
        aux['asIs']='mes_'+month_name[int(i)]+'_asIs_'+id+'.html'
        aux['toBe']='mes_'+month_name[int(i)]+'_toBe_'+id+'.html'
        mapa_barranquilla_observados.save('mes_'+month_name[int(i)]+'_asIs_'+id+'.html')
        mapa_barranquilla_predichos.save('mes_'+month_name[int(i)]+'_toBe_'+id+'.html')
        
        mapa_barranquilla_resta = folium.Map(location=[10.980706, -74.807636],zoom_start=15,tiles="OpenStreetMap")
        resta=modelo[1][['LATITUD','LONGITUD','PREDICHOS']].copy()
        resta['PREDICHOS']=modelo[1]['PREDICHOS']-modelo[0]['PREDICHOS']
        negativos=resta[resta['PREDICHOS']<0][['LATITUD','LONGITUD']].reset_index(drop=True)
        negativos['PREDICHOS']=1
        positivos=resta[resta['PREDICHOS']>0][['LATITUD','LONGITUD']].reset_index(drop=True)
        positivos['PREDICHOS']=1
        capa_calor_positiva=HeatMap(positivos[['LATITUD','LONGITUD','PREDICHOS']],gradient={0.4: 'orange', 0.65: 'orange', 1: 'orange'},radius=10,min_opacity=0.8,blur=20)
        capa_calor_negativo=HeatMap(negativos[['LATITUD','LONGITUD','PREDICHOS']],gradient={0.4: 'blue', 0.65: 'blue', 1: 'blue'},radius=10,min_opacity=0.8,blur=20)
        mapa_barranquilla_resta.add_child(capa_calor_positiva)
        mapa_barranquilla_resta.add_child(capa_calor_negativo)
        mapa_barranquilla_resta.save('mes_'+month_name[int(i)]+'_resta'+id+'.html')
        aux['resta']='mes_'+month_name[int(i)]+'_resta'+id+'.html'
        lista.append(aux)
    return(lista)


def video_mapa_dia(dias=['Lun','Mar','Mié','Jue','Vie','Sáb','Dom'],lights_aux=semaforos):
    lista=[]
    id=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    for i in dias:
        modelo=modelo_poisson(dia=i,lights_aux=lights_aux)
        mapa_barranquilla_observados = folium.Map(location=[10.980706, -74.807636],zoom_start=15,tiles="OpenStreetMap")
        mapa_barranquilla_predichos = folium.Map(location=[10.980706, -74.807636],zoom_start=15,tiles="OpenStreetMap")
        capa_calor_observados=HeatMap(modelo[0][['LATITUD','LONGITUD','PREDICHOS']],radius=15)
        capa_calor_predichos=HeatMap(modelo[1][['LATITUD','LONGITUD','PREDICHOS']],radius=15)
        mapa_barranquilla_predichos.add_child(capa_calor_predichos)
        mapa_barranquilla_observados.add_child(capa_calor_observados)
        mapa_barranquilla_observados.save('dia_'+i+'asIs'+id+'.html')
        mapa_barranquilla_predichos.save('dia_'+i+'toBe'+id+'.html')
        mapa_barranquilla_resta = folium.Map(location=[10.980706, -74.807636],zoom_start=13,tiles="OpenStreetMap")
        aux={}
        aux['conteo_toBe']=round(np.sum(modelo[1]['PREDICHOS']),0)
        aux['conteo_asIs']=round(np.sum(modelo[0]['PREDICHOS']),0)
        aux['id']=id
        aux['key']=i
        aux['asIs']='dia_'+i+'asIs'+id+'.html'
        aux['toBe']='dia_'+i+'toBe'+id+'.html'
        
        mapa_barranquilla_resta = folium.Map(location=[10.980706, -74.807636],zoom_start=15,tiles="OpenStreetMap")
        resta=modelo[1][['LATITUD','LONGITUD','PREDICHOS']].copy()
        resta['PREDICHOS']=modelo[1]['PREDICHOS']-modelo[0]['PREDICHOS']
        negativos=resta[resta['PREDICHOS']<0][['LATITUD','LONGITUD']].reset_index(drop=True)
        negativos['PREDICHOS']=1
        positivos=resta[resta['PREDICHOS']>0][['LATITUD','LONGITUD']].reset_index(drop=True)
        positivos['PREDICHOS']=1
        capa_calor_positiva=HeatMap(positivos[['LATITUD','LONGITUD','PREDICHOS']],gradient={0.4: 'orange', 0.65: 'orange', 1: 'orange'},radius=10,min_opacity=0.8,blur=20)
        capa_calor_negativo=HeatMap(negativos[['LATITUD','LONGITUD','PREDICHOS']],gradient={0.4: 'blue', 0.65: 'blue', 1: 'blue'},radius=10,min_opacity=0.8,blur=20)
        mapa_barranquilla_resta.add_child(capa_calor_positiva)
        mapa_barranquilla_resta.add_child(capa_calor_negativo)
        mapa_barranquilla_resta.save('dia_'+i+'resta'+id+'.html')
        aux['resta']='dia_'+i+'resta'+id+'.html'        
        lista.append(aux) 
        print(lista)       

    return(lista)


def funcion_final(dia=False, mes=False, hora=25, df=df, lights=semaforos, lights_aux=semaforos):
    if (mes != False):
        return (video_mapa_mes(mes=mes, lights_aux=semaforos))
    if (dia != False):
        return (video_mapa_dia(dias=dia, lights_aux=semaforos))
    if (hora != 25):
        return (video_mapa_hora(horas=hora, lights_aux=semaforos))
    return (mapa_calor_año(lights_aux=semaforos))
mapa_calor_año(lights_aux=semaforos.iloc[1:,:])