#!/usr/bin/env python
# coding: utf-8

# In[5]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

#%%
accidents=pd.read_csv("Accidentalidad_en_Barranquilla.csv",sep=";")


# In[6]:


import googlemaps
KEY = 'AIzaSyAYJejbUTC_tatmkH61AF_9-h3b-p0-Pvs'
gmaps = googlemaps.Client(key=KEY)


# In[9]:


def get_coordinates(address):
    city = 'Barranquilla, Colombia'
    geocode_result = gmaps.geocode(str(address) +' '+ city)
    if len(geocode_result) > 0:
        return list(geocode_result[0]['geometry']['location'].values())
    else:
        return [np.NaN, np.NaN]


# In[ ]:


geo_lat=[]
geo_lon=[]
naccidents=accidents.shape[0]
i=0
for address in accidents['SITIO_EXACTO_ACCIDENTE']:
    if i<=23000 or i>=23523:
        i=i+1
        continue
    print(f'{i} out of {naccidents}')
    geocoordinates=get_coordinates(address)
    geo_lat.append(geocoordinates[0])
    geo_lon.append(geocoordinates[1])
    if i%1000==0 :
        coordinates_dict = {'longitude': geo_lon, 'latitude': geo_lat}
        coordinates=pd.DataFrame(data=coordinates_dict)
        coordinates.to_csv('temp_coordinates.csv')
    i=i+1;

coordinates.to_csv('temp_coordinates_522.csv')

accidents['longitude']=geo_lon
accidents['latitude']=geo_lat

accidents.to_csv('accidents_geo.csv')


# In[26]:
part1=pd.read_csv('temp_coordinates - copia.csv')
part2=pd.read_csv('temp_coordinates_522.csv')
part3=pd.read_csv('temp_coordinates_4762.csv')
allparts=pd.concat([part1,part2,part3]).reset_index()
allparts=allparts.drop(['index','Unnamed: 0'],axis=1)
accidents_full=accidents.join(allparts)
accidents_full.to_csv('accidents_geo.csv')

# In[ ]:


#11.051455, -74.924250
#10.910911, -74.751215

def get_color_pot(geox,geoy,image):
    imx=image.shape[0]-1
    imy=image.shape[1]-1
    
    topleft=[11.051455, -74.924250]
    botright=[10.910911, -74.751215]
    
    mx=imx/(botright[0]-topleft[0])
    x=mx*(geox-topleft[0])
    
    my=imy/(botright[1]-topleft[1])
    y=my*(geoy-topleft[1])
    print(x)
    if math.isnan(x) or math.isnan(y):
        return(np.NaN)
        
    if int(x)>imx or int(y)>imy or int(x)<0 or int(y)<0:
        return(np.NaN)

    rgb=image[int(x)][int(y)]


        
        
    if rgb[0]>0.9 and rgb[1]>0.9 and rgb[2]<0.1:
        return('residencial')
    elif rgb[0]>0.9 and rgb[1]<0.1 and rgb[2]<0.1:
        return('comercial')
    elif rgb[0]>0.5 and rgb[1]<0.1 and rgb[2]>0.9:
        return('central')
    elif rgb[0]>0.9 and rgb[1]>0.55 and rgb[2]<0.1:
        return('portuaria')
    elif rgb[0]>0.9 and rgb[1]<0.6 and rgb[2]<0.6:
        return('industrial')
    elif rgb[0]>0.7 and rgb[1]>0.9 and rgb[2]>0.7:
        return('protegida')
    else:
        return('ninguna')
        
#%%
        
def get_color_loc(geox,geoy,image):
    imx=image.shape[0]-1
    imy=image.shape[1]-1
    
    topleft=[11.056087, -74.923477]
    botright=[10.915462, -74.751687]
    
    mx=imx/(botright[0]-topleft[0])
    x=mx*(geox-topleft[0])
    
    my=imy/(botright[1]-topleft[1])
    y=my*(geoy-topleft[1])
    print(x)
    if math.isnan(x) or math.isnan(y):
        return(np.NaN)
        
    if int(x)>imx or int(y)>imy or int(x)<0 or int(y)<0:
        return(np.NaN)

    rgb=image[int(x)][int(y)]


        
        
    if rgb[0]>0.9 and rgb[1]<0.1 and rgb[2]<0.1:
        return('riomar')
        
    elif rgb[0]<0.15 and rgb[1]<0.1 and rgb[2]>0.9:
        return('prado norte')
        
        
    elif rgb[0]<0.1 and rgb[1]>0.9 and rgb[2]>0.9:
        return('centro carrera 38')
        
    elif rgb[0]>0.9 and rgb[1]>0.9 and rgb[2]<0.1:
        return('suroccidental 2')
        
    elif rgb[0]<0.1 and rgb[1]>0.9 and rgb[2]<0.3:
        return('centro metropolitana')
        
    elif rgb[0]>0.9 and rgb[1]<0.1 and rgb[2]>0.9:
        return('ribera occidental')
        
    elif rgb[0]>0.9 and rgb[1]<0.8 and rgb[2]<0.1:
        return('suroriental')
        
    elif rgb[0]<0.4 and rgb[1]<0.1 and rgb[2]>0.5:
        return('suroccidental 1')
        
    else:
        return('ninguna')
        
        

#%%
        
def get_color_bus(geox,geoy,image,t):
    imx=image.shape[0]-1
    imy=image.shape[1]-1
    
    topleft=[11.083463, -74.910173]
    botright=[10.856376, -74.741860]
    
    mx=imx/(botright[0]-topleft[0])
    x=mx*(geox-topleft[0])
    
    my=imy/(botright[1]-topleft[1])
    y=my*(geoy-topleft[1])
    print(x)
    
    if math.isnan(x) or math.isnan(y):
        return(np.NaN)
        
    if int(x)>imx or int(y)>imy or int(x)<0 or int(y)<0:
        return(np.NaN)

    img=image[int(x)][int(y)]

    if t==1:
        thresh=[0.9,0.8,0.7,0.4,0.2]
    elif t==2:
        thresh=[0.9,0.7,0.5,0.4,0.25]
  
        
    if img>thresh[0]:
        return(0)
    elif img>thresh[1]:
        return(1)
    elif img>thresh[2]:
        return(2)
    elif img>thresh[3]:
        return(3)
    elif img>thresh[4]:
        return(4)
    else:
        return('ninguna')
        
#%%
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

accidents2=pd.read_csv("accidents_geo.csv")
imagepot=plt.imread('pot.png')
imageloc=plt.imread('barrios.png')
imagebus_b=rgb2gray(plt.imread('bus_bajadas.png'))
imagebus_s=rgb2gray(plt.imread('bus_subidas.png'))



#%%

accidents2['pot']=[get_color_pot(accidents2['latitude'][i],accidents2['longitude'][i],imagepot) for i in range(accidents2.shape[0])]
accidents2['pieza urbana']=[get_color_loc(accidents2['latitude'][i],accidents2['longitude'][i],imageloc) for i in range(accidents2.shape[0])]
accidents2['bus_subidas']=[get_color_bus(accidents2['latitude'][i],accidents2['longitude'][i],imagebus_s,1) for i in range(accidents2.shape[0])]
accidents2['bus_bajadas']=[get_color_bus(accidents2['latitude'][i],accidents2['longitude'][i],imagebus_b,2) for i in range(accidents2.shape[0])]

accidents2.to_csv('accidents_geo.csv')


    




