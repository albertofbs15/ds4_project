#%%
import numpy as np
import pandas as pd
import folium
from folium import plugins
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from selenium import webdriver
from folium.plugins import HeatMap
import os
import time
import datetime
from selenium.webdriver import Firefox
os.chdir("//home//usuario//Documentos//MinTIC//ds4_project//Mapas de calor//")
df=pd.read_csv('Final_Final.csv').iloc[:,1:]
blanco=mpimg.imread('blanco.png')
año_agrupado=df.groupby('AÑO_ACCIDENTE')
#%%
browser = webdriver.Chrome()
for aux in año_agrupado:
    año=aux[1]
    mapa_barranquilla = folium.Map(
        location=[10.980706, -74.807636],
        zoom_start=13,tiles="Stamen Toner")
    folium.raster_layers.ImageOverlay(
        image=blanco,
        bounds=[[11.047646, -74.881417],[10.887618, -74.755426]]).add_to(mapa_barranquilla)
    capa_calor=HeatMap(año[['LATITUD','LONGITUD']], min_opacity=0.1,radius=5, blur=6,max_zoom=5)
    mapa_barranquilla.add_child(capa_calor)
    tmpurl='file://{path}/{mapfile}.html'.format(path=os.getcwd(),mapfile=aux[0])
    mapa_barranquilla.save('{nombre}.html'.format(nombre=aux[0]))
    browser.set_window_position(0, 0)
    browser.set_window_size(1600, 900)
    browser.get(tmpurl)
    browser.save_screenshot('{nombre}.png'.format(nombre=aux[0]),)
browser.quit()


# %%
