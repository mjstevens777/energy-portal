# Weather Station to Geography

Implement some kind of Inverse Distance Weighting metric for matching up
geographies with weather stations. Start with simple nearest neighbors.

Using a hybrid of python and PostGIS will be helpful.

--

Weighted stations per census tract takes the five nearest stations and gives the weight to each, which is 1/euclidian_distance(census tract center, weather station location). Euclidean distance uses raw lat/long values so is super meaningless except to compare the relative closeness of each station.