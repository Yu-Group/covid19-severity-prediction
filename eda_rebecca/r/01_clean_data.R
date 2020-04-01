# Clean data for COVID presentation
# Author: Rebecca Barter
# Date: 3/31/2020


library(tidyverse)
library(lubridate)
library(scales)

## Load data ##----------------------------------------------------------------

data <- read_csv("../data/line_plots.csv")


## clean data ##----------------------------------------------------------------

# functin to extract whatever kind of count
extractCounts <- function(county, 
                          state, 
                          variable, 
                          start_date = ymd("2020/1/22")) {
  # variable is one of deaths, predicted_deaths_ensemble_1 or 
  #     predicted_deaths_ensemble_3
  
  # calculate the number of entries for the variable in question
  length_deaths_vec <- data %>%
    transmute(var = str_replace({{ variable }}, "\\[", ""),
              var = str_replace(var, "\\]", ""),
              var = str_squish(var)) %>%
    mutate(length = length(str_split(var, " ")[[1]])) %>%
    distinct(length) %>% 
    pull(length)
  
  
  deaths_data <- data %>% filter(CountyName == county, 
                                 StateNameAbbreviation == state) %>% 
    transmute(var = str_replace({{ variable }}, "\\[", ""),
              var = str_replace(var, "\\]", ""),
              var = str_squish(var)) %>%
    separate(var, into = paste0("day", 1:length_deaths_vec), sep = " ") %>%
    mutate_all(parse_number) %>%
    pivot_longer(cols = everything(), names_to = "day") %>%
    mutate(date = start_date + 0:(length_deaths_vec - 1))  %>%
    select(-day) %>%
    mutate(county = county, state = state)
  return(deaths_data)
}

# function to extract the counts and join them to the predictions
extractDeaths = function(county, state,
                         deaths_start_date = ymd("2020/1/22"),
                         predicted_deaths_1day_start_date = ymd("2020/3/30"),
                         predicted_deaths_3day_start_date = ymd("2020/3/28")) {
  # extract the deaths data
  deaths <- extractCounts(county, state, 
                          deaths, 
                          start_date = deaths_start_date) %>%
    rename(actual_deaths = value)
  # extrct the 1-day predicted data
  predicted_deaths_1day <- extractCounts(county, state,
                                         predicted_deaths_ensemble_1, 
                                         start_date = predicted_deaths_1day_start_date) %>%
    rename(deaths_predicted_1day = value)
  # extract the 3-day predicted data
  predicted_deaths_3day <- extractCounts(county, state,
                                         predicted_deaths_ensemble_3, 
                                         start_date = predicted_deaths_3day_start_date) %>%
    rename(deaths_predicted_3day = value)
  # combine the data
  full_data <- left_join(deaths, predicted_deaths_1day, 
                         by = c("county", "state", "date")) %>%
    left_join(predicted_deaths_3day, by = c("county", "state", "date"))
  return(full_data)
  
}

# extract data for counties of interest
deaths_clean <- extractDeaths("King", "WA") %>%
  rbind(extractDeaths("Kings", "NY")) %>%
  rbind(extractDeaths("Queens", "NY")) %>%
  rbind(extractDeaths("Bronx", "NY")) %>%
  rbind(extractDeaths("New York", "NY")) %>%
  rbind(extractDeaths("Orleans", "LA")) %>%
  rbind(extractDeaths("Wayne", "MI")) 

cases_clean <- extractCounts("King", "WA", cases) %>%
  rbind(extractCounts("Kings", "NY", cases)) %>%
  rbind(extractCounts("Queens", "NY", cases)) %>%
  rbind(extractCounts("Bronx", "NY", cases)) %>%
  rbind(extractCounts("New York", "NY", cases)) %>%
  rbind(extractCounts("Orleans", "LA", cases)) %>%
  rbind(extractCounts("Wayne", "MI", cases)) %>%
  rename(cases = value)




# add a county-state variable
data_clean <- deaths_clean %>% 
  left_join(cases_clean, by = c("county", "state", "date")) %>%
  unite(county_state, county, state, sep = " County, ")


# days since 10 deaths
date_of_10_deaths <- data_clean %>%
  group_by(county_state) %>%
  filter(actual_deaths >= 10) %>%
  filter(date == min(date)) %>%
  ungroup() %>%
  select(county_state, date_of_10_deaths = date)

# days since 100 cases
date_of_100_cases <- data_clean %>%
  group_by(county_state) %>%
  filter(cases >= 100) %>%
  filter(date == min(date)) %>%
  ungroup() %>%
  select(county_state, date_of_100_cases = date)


# add days since 10 deaths
data_clean <- data_clean %>%
  left_join(date_of_10_deaths, by = c("county_state")) %>%
  mutate(days_since_10_deaths = as.numeric(date - date_of_10_deaths)) %>%
  left_join(date_of_100_cases, by = "county_state") %>%
  mutate(days_since_100_cases = as.numeric(date - date_of_100_cases)) 

