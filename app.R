library(shiny)
library(leaflet)
library(rgdal)

ca_neighbors<-readOGR(dsn="./Data/ZillowNeighborhoods-CA.shp")
sd<-ca_neighbors[ca_neighbors$County == "San Diego",]
colors<-colorRampPalette(c("red","green"))(length(sd$Name))
neighborhood_names<-as.character(sd@data$Name)

ui <- fluidPage(
  leafletOutput("sd_rent_yeild_map",width="100%",height=500)
)

server <- function(input, output, session) {
  output$sd_rent_yeild_map <- renderLeaflet({
	leaflet(sd)%>% addProviderTiles(providers$Esri) %>%addPolygons(color = colors, weight = 1, smoothFactor = 0.5,opacity = 1.0, fillOpacity = 0.5,label= neighborhood_names,highlightOptions = highlightOptions(color = "white", weight = 2,bringToFront = TRUE))%>%setView(-117.161087,32.715736,zoom=12)
  })
}

shinyApp(ui, server)