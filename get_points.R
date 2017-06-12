setwd('~/Desktop/rentalrealty/sd_rental_yeild')
library(shiny)
library(leaflet)
library(rgdal)
library(jsonlite)
ca_neighbors<-readOGR(dsn="./Data/ZillowNeighborhoods-CA.shp")
sd<-ca_neighbors[ca_neighbors$County == "San Diego",]
dat<-fromJSON("./Data/craigslist_rental_data.json",flatten=TRUE)
sd$PlaceName<-as.character(sd$Name)

find_place<-function(idx,dt,shp) {
	for (i in 1:nrow(shp))
	{
		isit<-point.in.polygon(dt$longitue[idx],dt$latitude[idx],shp@polygons[[i]]@Polygons[[1]]@coords[,1],shp@polygons[[i]]@Polygons[[1]]@coords[,2]) 
		if (isit)
		{
			return(shp$PlaceName[i])
		}
	}
	return("NA")
}

dat$Place<-lapply(seq(1:nrow(dat)),FUN=find_place,dat,sd)
dat$Place<-unlist(dat$Place)
t<-aggregate(dat$Rent_price~ dat$Place, FUN=length)
nrow(t[t$"dat$Rent_price">=10,])
house_type<- function(x) { if ('apartment'%in% x) {return('apartment')} else if ('condo' %in% x) {return('condo')} else if ('house' %in% x) {return('house')} else if ('townhouse' %in% x) {return('townhouse')} else if ('loft' %in% x) {return ('loft')} else if ('duplex' %in% x) {return('duplex')} else {return('NA')} }
dat$home_type<-lapply(dat$attributes,FUN=house_type)
dat$home_type<-unlist(dat$home_type)
dat_filt<-dat[(dat$Rent_price>300) & (!(dat$Place== "NA")) & (!is.na(dat$Rent_price)) & (!is.na(dat$map_accuracy)) &(dat$map_accuracy<22) &(dat$Rent_price<10000) & (dat$Square_feet<10000),]

#point.in.polygon(sd@polygons[[1]]@labpt[1],sd@polygons[[1]]@labpt[2],sd@polygons[[1]]@Polygons[[1]]@coords[,1],sd@polygons[[1]]@Polygons[[1]]@coords[,2])
