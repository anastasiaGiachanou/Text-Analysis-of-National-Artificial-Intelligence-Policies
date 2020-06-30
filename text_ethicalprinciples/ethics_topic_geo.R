library(dplyr)
library(ggplot2)
library(tidyverse)


######################

# Section 4.2 - Discussion of Ethical Principles
reverseSearchFrequency <- read.csv("reverseSearchFrequency.csv", check.names=FALSE)
str(reverseSearchFrequency)
long_reverseSearchFrequency <- reverseSearchFrequency %>%
  gather(Principle, Frequency, Transparency:Solidarity)

str(long_reverseSearchFrequency)
long_reverseSearchFrequency$Principle <- as.factor(long_reverseSearchFrequency$Principle)

levels(long_reverseSearchFrequency$Principle)
long_reverseSearchFrequency$Principle = reorder(long_reverseSearchFrequency$Principle, desc(long_reverseSearchFrequency$Frequency), median)

long_reverseSearchFrequency$Ratio = long_reverseSearchFrequency$Frequency / long_reverseSearchFrequency$TotalLength

ggplot(long_reverseSearchFrequency, aes(x = Ratio, y = Principle, fill = Principle)) +
  scale_x_continuous(labels = scales::percent_format(accuracy = 0.5),
                     limits = c(0, NA),
                     expand = expansion(mult = c(0, 0.1))) +
  ylab("") +
  xlab("Occurence in corpus") +
  geom_boxplot(width = 0.5) +
  geom_point(alpha = 0.45) +
  ggthemes::theme_clean(base_size = 17) +
  theme(
    legend.position = "none",
    legend.key = element_blank(), strip.background = element_blank(),
    plot.title = element_text(size = 14, hjust = 0.5),
    axis.ticks = element_blank(),
    panel.grid = element_blank(),
    panel.grid.major.y = element_blank(),
    panel.background = element_blank(),
    legend.background = element_rect(color = NA),
    legend.title = element_blank(),
    legend.spacing.x = unit(0.15, 'cm'),
    plot.background = element_rect(color = NA))

#ggsave("plots/principles.pdf", height = 11, width = 25, units = "cm")



library(data.table)
library(ggthemes)

ethicsGeoclusters <- read.csv("ethicsGeoclusters.csv", check.names=FALSE)
ethicsGeoclusters <- reshape2::melt(ethicsGeoclusters)

str(ethicsGeoclusters)

ethicsGeoclusters$geocluster_label <- ethicsGeoclusters$geocluster

ethicsGeoclustersMean <- ethicsGeoclusters %>% 
  group_by(variable) %>%
  summarise(mean = mean(value))

ethicsGeoclusters <- merge(ethicsGeoclusters, 
                           ethicsGeoclustersMean, by = "variable")

ggplot(ethicsGeoclusters, 
       aes (x = reorder(variable, desc(variable)), 
            y = value, group = geocluster), shape = 16) +
  geom_point(aes(y = mean, color = "red"), shape = 1) +
  geom_point(aes(color = "black")) +
  facet_wrap(geocluster ~ ., scales = "free_x") +
  scale_y_continuous(labels = scales::percent) +
  scale_color_manual(name = "Frequency",
                     labels = c("Cluster average", "Corpus average"),
                     values = c("#000000", "#ff0000"),
                     guide = guide_legend(override.aes = list(shape = c(16, 1)))) +
  xlab("") +
  ylab("") +
  theme_clean(base_size = 13) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5),
        plot.background = element_rect(color = NA),
        legend.position = "bottom",
        legend.title = element_blank(),
        legend.background = element_blank())

#ggsave("plots/ethics-regions.pdf", width = 27, height = 18, units = "cm")
#ggsave("plots/ethics-regions.png", width = 27, height = 18, units = "cm")
