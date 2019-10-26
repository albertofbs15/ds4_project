#################Limpieza NA SPECIALDATES##################

nas=which(is.na(SpecialDates$Type))
SpecialDates$Type[nas]="Común"

##################Limpieza NA accidentes HERIDOS y muertos###

nas=which(is.na(accidentes$`CANT_HERIDOS_EN _SITIO_ACCIDENTE`))
accidentes$`CANT_HERIDOS_EN _SITIO_ACCIDENTE`[nas]=0


nas=which(is.na(accidentes$`CANT_MUERTOS_EN _SITIO_ACCIDENTE`))
accidentes$`CANT_MUERTOS_EN _SITIO_ACCIDENTE`[nas]=0
################ Limpieza NA  latitud y Longitud y#####


nas=which(is.na(accidentes$latitude))
#accidentes=accidentes[-nas,]
#nas=which(is.na(accidentes$longitude)) #no hizo falta


nas=which(is.na(accidentes$SITIO_EXACTO_ACCIDENTE))
accidentes=accidentes[-nas,]


nas=which(is.na(accidentes$pot))
accidentes=accidentes[-nas,]

nas=which(is.na(accidentes$`pieza urbana`))
accidentes=accidentes[-nas,]

#Se elimina la hora de fecha accidente ya que no sirve porque todas están en 12.00.00am
accidentes$FECHA_ACCIDENTE

accidentes$FECHA_ACCIDENTE=sapply(accidentes$FECHA_ACCIDENTE,FUN = substr,start=1,stop=10,USE.NAMES = F)
accidentes$FECHA_ACCIDENTE=as.Date(accidentes$FECHA_ACCIDENTE,format = "%m/%d/%Y")
###################Aquí termina la limpieza de accidente#######

#transformamos la fecha de specialDate

SpecialDates$Date=sapply(SpecialDates$Date,FUN = substr,start=1,stop=10,USE.NAMES = F)
SpecialDates$Date=as.Date(SpecialDates$Date,format="%Y-%m-%d")
#############

library(tidyverse)

aux=left_join(accidentes, SpecialDates, by = c("FECHA_ACCIDENTE"="Date"), suffix = c(".x", ".y"))
View(aux)

aux=left_join(aux, junior, by = c("FECHA_ACCIDENTE"="date"), suffix = c(".x", ".y"))




write.csv(aux,"datos_joined.csv",row.names = F)
