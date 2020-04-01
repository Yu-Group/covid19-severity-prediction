# Create line plot figures for COVID-19 presentation
# Author: Rebecca Barter
# Date: 3/31/2020

library(tidyverse)
library(lubridate)
library(scales)

## Load data ##----------------------------------------------------------------

source("01_clean_data.R")


## Plot cases ## ---------------------------------------------------------------


# create a version of the data for plotting
data_plot_cases <- data_clean %>% 
  mutate(county_highlight = case_when(county_state == "Queens County, NY" ~ "Queens",
                                      county_state == "King County, WA" ~ "King",
                                      !(county_state %in% c("Queens County, NY", "King County, WA")) ~ "other")) 


# get text label locations
annotation_cases <- data_plot_cases %>%
  group_by(county_state) %>%
  mutate(x_text = max(days_since_100_cases),
         y_text = max(cases, na.rm = T)) %>%
  ungroup() %>%
  distinct(county_state, x_text, y_text, county_highlight)

# make line plots
data_plot_cases %>%
  ggplot() +
  geom_line(aes(x = days_since_100_cases, y = cases, 
                group = county_state, col = county_highlight, size = county_highlight)) +
  geom_text(aes(x = x_text + 1, y = y_text, label = paste0(comma_format(100)(y_text), "  ", county_state), 
                col = county_highlight), 
            data = annotation_cases, hjust = 0, check_overlap = TRUE, size = 5.5,
            family = "Avenir") +
  scale_x_continuous(limits = c(-30, 47)) +
  scale_y_continuous(limits = c(0, 18000)) +
  scale_color_manual(values = c("#445E93", "grey50", "#F93943"), guide = "none") +
  scale_size_manual(values = c(1.5, 0.5, 1.5), guide = "none") +
  theme_classic(base_size = 22)  +
  theme(axis.line.y = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks.y = element_blank(),
        axis.title.y = element_blank(),
        axis.line.x = element_line(color = "grey40"),
        axis.ticks.x = element_line(color = "grey40"),
        axis.title.x = element_text(family = "Avenir")) +
  labs(x = "Days since 100 cases")
ggsave("../figures/cumulative_cases.png", width = 8, height = 6)    








## Plot deaths data ## ---------------------------------------------------------------


# create a version of the data for plotting
data_plot_deaths <- data_clean %>% 
  # make the deaths data missing after 3 days before
  mutate(actual_deaths = if_else(date > ymd("2020-03-27"),
                                 as.numeric(NA), actual_deaths)) %>%
  mutate(county_highlight = case_when(county_state == "Queens County, NY" ~ "Queens",
                                      county_state == "King County, WA" ~ "King",
                                      !(county_state %in% c("Queens County, NY", "King County, WA")) ~ "other")) 
# remove the weird NY value
if (data_plot_deaths[["actual_deaths"]][330] == 4){
  data_plot_deaths[["actual_deaths"]][330] <- 0
}

# get text label locations
annotation <- data_plot_deaths %>%
  group_by(county_state) %>%
  mutate(x_text = max(days_since_10_deaths) - 3.5,
         y_text = max(actual_deaths, na.rm = T)) %>%
  ungroup() %>%
  distinct(county_state, x_text, y_text, county_highlight)

# make line plots
data_plot_deaths %>%
  ggplot() +
  geom_line(aes(x = days_since_10_deaths, y = actual_deaths, 
                group = county_state, col = county_highlight, size = county_highlight)) +
  geom_text(aes(x = x_text + 0.8, y = y_text, label = paste0(y_text, " -  ", county_state), 
                col = county_highlight), 
            data = annotation, hjust = 0, check_overlap = TRUE, size = 6,
            family = "Avenir") +
  scale_x_continuous(limits = c(-30, 47)) +
  scale_y_continuous(limits = c(0, 310)) +
  scale_color_manual(values = c("#445E93", "grey60", "#F93943"), guide = "none") +
  scale_size_manual(values = c(1.5, 0.5, 1.5), guide = "none") +
  theme_classic(base_size = 22)  +
  theme(axis.line.y = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks.y = element_blank(),
        axis.title.y = element_blank(),
        axis.line.x = element_line(color = "grey40"),
        axis.ticks.x = element_line(color = "grey40"),
        axis.title.x = element_text(family = "Avenir")) +
  labs(x = "Days since 10 deaths")
ggsave("../figures/cumulative_deaths.png", width = 8, height = 6)    









## Plot death blank plot ## ---------------------------------------------------------------


# create a version of the data for plotting
data_plot_deaths_subset <- data_clean %>% 
  # make the deaths data missing after 3 days before
  mutate(actual_deaths = if_else(date > ymd("2020-03-27"),
                                 as.numeric(NA), actual_deaths)) %>%
  filter(county_state %in% c("Queens County, NY", "King County, WA"))

# get text label locations
annotation <- data_plot_deaths_subset %>%
  group_by(county_state) %>%
  mutate(x_text = max(days_since_10_deaths) - 3.5,
         y_text = max(actual_deaths, na.rm = T)) %>%
  ungroup() %>%
  distinct(county_state, x_text, y_text)

# make line plots
data_plot_deaths_subset %>%
  ggplot() +
  geom_line(aes(x = days_since_10_deaths, y = actual_deaths, 
                group = county_state, col = county_state), size = 1.5) +
  geom_text(aes(x = x_text + 1, y = y_text, label = paste0(y_text, " -  ", county_state),
                col = county_state),
            data = annotation, hjust = 0, check_overlap = TRUE,
            family = "Avenir", size = 6) +
  scale_x_continuous(limits = c(-30, 47)) +
  scale_y_continuous(limits = c(0, 310)) +
  scale_color_manual(values = c("#445E93", "#F93943"), guide = "none") +
  theme_classic(base_size = 22)  +
  theme(axis.line.y = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks.y = element_blank(),
        axis.title.y = element_blank(),
        axis.line.x = element_line(color = "grey40"),
        axis.ticks.x = element_line(color = "grey40"),
        axis.title.x = element_text(family = "Avenir")) +
  labs(x = "Days since 10 deaths")
ggsave("../figures/cumulative_deaths_blank.png", width = 8, height = 6)    








## Plot death projections ## ---------------------------------------------------------------


# create a version of the data for plotting
data_plot_deaths_subset <- data_clean %>% 
  # make the deaths data missing after 3 days before
  mutate(actual_deaths_with_missing = if_else(date > ymd("2020-03-27"),
                                 as.numeric(NA), actual_deaths)) %>%
  filter(county_state %in% c("Queens County, NY", "King County, WA")) %>%
  # add the real data to the predicted data for March 27
  group_by(county_state) %>%
  mutate(deaths_predicted_3day = case_when(
    date == ymd("2020-03-27") ~ actual_deaths_with_missing, 
    date != ymd("2020-03-27") ~ deaths_predicted_3day
  )) %>%
  ungroup()

# get text label locations
annotation <- data_plot_deaths_subset %>%
  group_by(county_state) %>%
  mutate(x_text = max(days_since_10_deaths) - 3.5,
         y_text = max(actual_deaths_with_missing, na.rm = T)) %>%
  ungroup() %>%
  distinct(county_state, x_text, y_text)
annotation_predicted <- data_plot_deaths_subset %>%
  group_by(county_state) %>%
  mutate(x_text = max(days_since_10_deaths),
         y_text = round(max(deaths_predicted_3day, na.rm = T))) %>%
  ungroup() %>%
  distinct(county_state, x_text, y_text)

# make line plots
data_plot_deaths_subset %>%
  ggplot() +
  geom_line(aes(x = days_since_10_deaths, y = actual_deaths_with_missing, 
                group = county_state, col = county_state), size = 1.5) +
  geom_line(aes(x = days_since_10_deaths, y = deaths_predicted_3day, 
                group = county_state, col = county_state), 
            size = 1, linetype = "dashed", alpha = 0.7) +
  geom_text(aes(x = x_text + 1, y = y_text, label = y_text,
                col = county_state),
            data = annotation, hjust = 0, check_overlap = TRUE,
            family = "Avenir", alpha = 0.5, size = 5) +
  geom_text(aes(x = x_text + 1, y = y_text, label = paste0(y_text, " -  ", county_state),
                col = county_state),
            data = annotation_predicted, hjust = 0, check_overlap = TRUE,
            family = "Avenir", size = 5) +
  scale_x_continuous(limits = c(-30, 47)) +
  scale_y_continuous(limits = c(0, 310)) +
  scale_color_manual(values = c("#445E93", "#F93943"), guide = "none") +
  theme_classic(base_size = 22)  +
  theme(axis.line.y = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks.y = element_blank(),
        axis.title.y = element_blank(),
        axis.line.x = element_line(color = "grey40"),
        axis.ticks.x = element_line(color = "grey40"),
        axis.title.x = element_text(family = "Avenir")) +
  labs(x = "Days since 10 deaths")
ggsave("../figures/cumulative_deaths_predicted.png", width = 8, height = 6)    








## Plot death projections compared with real ## ---------------------------------------------------------------


# create a version of the data for plotting
data_plot_deaths_subset <- data_clean %>% 
  # make the deaths data missing after 3 days before
  mutate(actual_deaths_with_missing = if_else(date > ymd("2020-03-27"),
                                              as.numeric(NA), actual_deaths)) %>%
  filter(county_state %in% c("Queens County, NY", "King County, WA")) %>%
  # add the real data to the predicted data for March 27
  group_by(county_state) %>%
  mutate(deaths_predicted_3day = case_when(
    date == ymd("2020-03-27") ~ actual_deaths_with_missing, 
    date != ymd("2020-03-27") ~ deaths_predicted_3day
  )) %>%
  ungroup()

# get text label locations
annotation <- data_plot_deaths_subset %>%
  group_by(county_state) %>%
  mutate(x_text = max(days_since_10_deaths),
         y_text = max(actual_deaths, na.rm = T)) %>%
  ungroup() %>%
  distinct(county_state, x_text, y_text)
annotation_predicted <- data_plot_deaths_subset %>%
  group_by(county_state) %>%
  mutate(x_text = max(days_since_10_deaths),
         y_text = round(max(deaths_predicted_3day, na.rm = T))) %>%
  ungroup() %>%
  distinct(county_state, x_text, y_text)

# make line plots
data_plot_deaths_subset %>%
  ggplot() +
  geom_line(aes(x = days_since_10_deaths, y = actual_deaths, 
                group = county_state, col = county_state), size = 1.5) +
  geom_line(aes(x = days_since_10_deaths, y = deaths_predicted_3day, 
                group = county_state, col = county_state), 
            size = 1, linetype = "dashed", alpha = 0.7) +
  geom_text(aes(x = x_text + 1, y = y_text, label = paste(y_text, " - ", county_state),
                col = county_state),
            data = annotation, hjust = 0, check_overlap = TRUE,
            family = "Avenir", size = 5) +
  geom_text(aes(x = x_text + 1, y = y_text, label = paste0(y_text, " (predicted)"),
                col = county_state),
            data = annotation_predicted, hjust = 0, check_overlap = TRUE,
            family = "Avenir", alpha = 0.5, size = 5) +
  scale_x_continuous(limits = c(-30, 47)) +
  scale_y_continuous(limits = c(0, 310)) +
  scale_color_manual(values = c("#445E93", "#F93943"), guide = "none") +
  theme_classic(base_size = 22)  +
  theme(axis.line.y = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks.y = element_blank(),
        axis.title.y = element_blank(),
        axis.line.x = element_line(color = "grey40"),
        axis.ticks.x = element_line(color = "grey40"),
        axis.title.x = element_text(family = "Avenir")) +
  labs(x = "Days since 10 deaths")
ggsave("../figures/cumulative_deaths_predicted_with_true.png", width = 8, height = 6)    







## Many line plots death projections compared with real ## ---------------------------------------------------------------


# create a version of the data for plotting
data_plot_deaths_subset <- data_clean %>% 
  filter(county_state != "Kings County, NY") %>%
  # make the deaths data missing after 3 days before
  mutate(actual_deaths_with_missing = if_else(date > ymd("2020-03-27"),
                                              as.numeric(NA), actual_deaths)) %>%
  #filter(county_state %in% c("Queens County, NY", "King County, WA")) %>%
  # add the real data to the predicted data for March 27
  mutate(highlight = date >= ymd("2020-03-27")) %>%
  group_by(county_state) %>%
  mutate(deaths_predicted_3day = case_when(
    date == ymd("2020-03-27") ~ actual_deaths_with_missing, 
    date != ymd("2020-03-27") ~ deaths_predicted_3day
  )) %>%
  ungroup()

# get text label locations
annotation <- data_plot_deaths_subset %>%
  group_by(county_state) %>%
  mutate(x_text = max(days_since_10_deaths),
         y_text = max(actual_deaths, na.rm = T)) %>%
  ungroup() %>%
  distinct(county_state, x_text, y_text)
annotation_predicted <- data_plot_deaths_subset %>%
  group_by(county_state) %>%
  mutate(x_text = max(days_since_10_deaths),
         y_text = round(max(deaths_predicted_3day, na.rm = T))) %>%
  ungroup() %>%
  distinct(county_state, x_text, y_text)

# make line plots
data_plot_deaths_subset %>%
  ggplot() +
  geom_line(aes(x = days_since_10_deaths, y = actual_deaths, col = highlight)) +
  geom_line(aes(x = days_since_10_deaths, y = deaths_predicted_3day), 
            linetype = "dashed", alpha = 0.7, col = "#445E93") +
  geom_text(aes(x = x_text + 1, y = y_text, label = paste(y_text, " (observed)")),
            data = annotation, hjust = 0, check_overlap = TRUE,
            family = "Avenir", size = 3) +
  geom_text(aes(x = x_text + 1, y = y_text, label = paste0(y_text, " (predicted)")),
            data = annotation_predicted, hjust = 0, check_overlap = TRUE,
            family = "Avenir", alpha = 0.8, size = 3, col = "#445E93") +
  scale_x_continuous(limits = c(-5, 27)) +
  scale_y_continuous(limits = c(0, 310)) +
  scale_color_manual(values = c("black", "grey50"), guide = "none") +
  theme_minimal(base_size = 16)  +
  theme(axis.line.y = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks.y = element_blank(),
        axis.title.y = element_blank(),
        axis.line.x = element_line(color = "grey40"),
        axis.ticks.x = element_line(color = "grey40"),
        axis.title.x = element_text(family = "Avenir")) +
  labs(x = "Days since 10 deaths") +
  facet_wrap(~county_state, ncol = 3)
ggsave("../figures/cumulative_deaths_predicted_grid.png", width = 8, height = 6)    




