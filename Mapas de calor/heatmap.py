import pandas as pd
import numpy as np
import folium
from folium import plugins
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from selenium import webdriver
import os
import time
from PIL import Image
#os.chdir("//home//usuario//Documentos//MinTIC//ds4_project//Mapas de calor//")
df=pd.read_csv('Final_Final.csv',low_memory=False).iloc[:,1:]
blanco=mpimg.imread('blanco.png')
# Imágenes para los días de la semana
def imagenes(variable='AÑO_ACCIDENTE',radio=5,blur=6,max_zoom=5):
    variable_agrupado=df.groupby(variable)
    browser = webdriver.Chrome()
    browser.set_window_position(0, 0)
    browser.set_window_size(1600, 900) # resolucion pc del trabajo
    #browser.set_window_size(1920, 1080) #resolución pc de la casa
    for aux in variable_agrupado:
        grupo=aux[1]
        mapa_barranquilla = folium.Map(
            location=[10.980706, -74.807636],
            zoom_start=13,tiles="OpenStreetMap")
        folium.raster_layers.ImageOverlay(
            image=blanco,
            bounds=[[11.047646, -74.881417],[10.887618, -74.755426]]).add_to(mapa_barranquilla)
        capa_calor=HeatMap(grupo[['LATITUD','LONGITUD']], min_opacity=0.1,radius=radio, blur=blur,max_zoom=max_zoom)
        mapa_barranquilla.add_child(capa_calor)
        tmpurl='file://{path}/{mapfile}.html'.format(path=os.getcwd(),mapfile=aux[0])
        mapa_barranquilla.save('{nombre}.html'.format(nombre=aux[0]))
        browser.get(tmpurl)
        browser.save_screenshot('{nombre}.png'.format(nombre=aux[0]))
        im = Image.open('{nombre}.png'.format(nombre=aux[0]))         
        im1 = im.crop((330, 0, 1062, 742)) 
        os.remove('{nombre}.png'.format(nombre=aux[0]))        
        os.remove('{nombre}.html'.format(nombre=aux[0]))
        im1.save('{nombre}.png'.format(nombre=aux[0]))
    browser.quit()

verdad=True
while(verdad):
    val=input('Escriba el nombre de la variable que quiere: ')
    imagenes(variable=val)
    print('Listo!')
    verdad=False
