# SafeGraph Social Distancing Data

- **Data source**: https://www.safegraph.com/covid-19-data-consortium

- **Last downloaded**: updated daily

- **Data description**: aggregated daily views of USA foot-traffic summarizing movement between counties; data is available going back to Jan 1, 2020; data provided by SafeGraph

- **Known data quality issues**: 
    - There is a 3 day lag in the data.
    - To preserve privacy, differential privacy was applied to all of the device count metrics other than the device_count

- **Short list of data columns**: (long format)
    - **countyFIPS**: county FIPS
    - **date**: date of foot traffic data
    - **device_count**: number of devices seen in our panel during the date range whose home is in this countyFIPS. Home is defined as the common nighttime location for the device over a 6 week period where nighttime is 6 pm - 7 am. Note that we do not include any census blocks where the count <5.
    - **completely_home_device_county**: out of the device_count, the number of devices which did not leave the geohash-7 in which their home is located during the time period
    - **part_time_work_behavior_devices**: out of the device_count, the number of devices that spent one period of between 3 and 6 hours at one location other than their geohash-7 home during the period of 8 am - 6 pm in local time. This does not include any device that spent 6 or more hours at a location other than home.
    - **full_time_work_behavior_devices**: out of the device_count, the number of devices that spent greater than 6 hours at a location other than their home geohash-7 during the period of 8 am - 6 pm in local time.
    - **delivery_behavior_devices**: out of the device_count, the number of devices that stopped for < 20 minutes at > 3 locations outside of their geohash-7 home.
    - **bucketed_distance_traveled_{BUCKET}**: {BUCKET} is range of meters (from geohash-7 of home) and value is the number of devices that fall into the given distance traveled bucket; if a device made multiple trips, we use the median distance for the device
    - **bucketed_home_dwell_time_{BUCKET}**: {BUCKET} is range of minutes and value is the number of devices that dwelled at geohash-7 of home for some time within the given {BUCKET}. For each device, we summed the observed minutes at home across the day (whether or not these were contiguous) to get the total minutes for each device this day. Then we count how many devices are in each bucket. We include the portion of any stop within the time range regardless of whether the stop start time was in the time period.
    - **bucketed_away_from_home_time_{BUCKET}**: {BUCKET} is range of minutes and value is device count of devices that dwelled outside of geohash-7 of home for some time within the given {BUCKET}. For each device, we summed the stops away home and then found the median of the sums. We include any stop that crossed over into the time period regardless of whether the stop start time was in the time period.
    - **bucketed_percentage_time_home_{BUCKET}**: {BUCKET} is a range of percentage of time a device was observed at home (numerator) out of total hours observed that day at any location (denominator). Value is the number of devices observed in this {BUCKET} range.
    - **at_home_by_each_hour_{#}**: {#} is an hour of the day (e.g., 0 = midnight to 1am, 1 = 1am to 2am) and value is the number of devices at geohash-7 home in the given hour (in local time)
    - **destination_cbgs**: dictionary; key is a destination countyFIPS and value is the number of devices with a home in the current (origin) countyFIPS that stopped in the given destination countyFIPS for >1 minute during the time period; destination countyFIPS will also include the origin countyFIPS in order to see if there are any devices that originate from the origin countyFIPS but are staying completely outside of it.

- **Notes**:

    - This data has been cleaned already. For the original schema and details, please see https://docs.safegraph.com/docs/social-distancing-metrics. 
    - Note: the original data from SafeGraph is collected at the census block level, which is more granular than the county level data provided in this repo.
    - Thank you to SafeGraph for kindly sharing their data with us.