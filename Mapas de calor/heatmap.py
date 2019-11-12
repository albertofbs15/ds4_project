from folium import plugins
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from selenium import webdriver
import os
import time
import datetime
from selenium.webdriver import Firefox
df=pd.read_csv('Final_Final.csv').iloc[:,1:]
blanco=mpimg.imread('blanco.png')

def filtrar()