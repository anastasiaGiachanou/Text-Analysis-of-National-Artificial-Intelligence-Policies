#install.packages("ggplot2")
#install.packages("dplyr")
#install.packages("maps")
#install.packages("rworldmap")
#install.packages("rworldxtra")

countries <- read.csv("countries.csv")

library(ggplot2)
library(dplyr)
library(maps)
library(rworldmap) # get world map with iso codes

countries$include <- TRUE
str(countries)

world_map <- joinCountryData2Map(countries, 
                                 mapResolution = "low",
                                 joinCode = "NAME",
                                 nameJoinColumn = "Country")

world_map_poly <- fortify(world_map) #extract polygons 
world_map_poly <- merge(world_map_poly, world_map@data, by.x="id", by.y="ADMIN.1", all.x=T)
world_map_poly <- world_map_poly %>% arrange(id, order)

colnames(world_map@data) <- make.unique(names(world_map@data))

world_map_poly[is.na(world_map_poly$include),]$include <- FALSE

ggplot() + 
  coord_map(xlim = c(-180, 180), ylim = c(-55, 75))  +
  #coord_sf(ylim = c(-50, 90), datum = NA) +
  #coord_map() +
  geom_polygon(data = world_map_poly, aes(long, lat, group = group, fill = include),size = 0.3) + 
  scale_fill_manual(values= c("#dddddd", "#2c7fb8")) + 
  theme_bw() + xlab(NULL) + ylab(NULL) + 
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.text = element_blank(),
        axis.ticks = element_blank(),
        panel.border = element_blank(),
        legend.position = "none")

#ggsave("plots/worldmap.pdf", height = 5, width = 9, units = "cm")