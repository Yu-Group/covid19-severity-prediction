# Create scatterplot figures for COVID-19 presentation
# Author: Rebecca Barter
# Date: 3/31/2020

library(tidyverse)
library(lubridate)
library(scales)

## Load data ##----------------------------------------------------------------

source("01_clean_data.R")


## Plot 3-day prediction performance ## ---------------------------------------------------------------

data_clean %>%
  filter(date == ymd("2020-03-30")) %>%
  ggplot() +
  geom_point(aes(x = deaths_predicted_3day, y = actual_deaths), size = 5, 
             col = "#445E93") +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed") +
  geom_text(aes(x = deaths_predicted_3day + 5, 
                y = actual_deaths, label = county_state), 
            hjust = 0, check_overlap = TRUE, size = 6, 
            family = "Avenir") +
  theme_classic(base_size = 22) +
  labs(x = "Predicted deaths by 3/30\n(predicted on 3/27)",
       y = "Actual deaths by 3/30") +
  scale_x_continuous(limit = c(50, 390)) +
  scale_y_continuous(limit = c(50, 390)) +
  theme(axis.line = element_line(color = "grey40"),
        axis.ticks = element_line(color = "grey40"),
        axis.title = element_text(family = "Avenir")) +
  coord_fixed() 
ggsave("../figures/scatter_performance.png", width = 8, height = 8)    



data_clean %>%
  
  filter(date == ymd("2020-03-30")) %>%
  ggplot() +
  geom_col(aes(x = county_state, y = deaths_predicted_3day), alpha = 0.5) +
  geom_col(aes(x = county_state, y = actual_deaths), alpha = 0.5)
  
