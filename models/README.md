Pipeline (approximately)

pums_geography_model - appends a probability distribution of puma regions given the joined feature set (function applied to household_electricity)

elep_divided_by_usage - uses KWH_MODELED to sanitize ELEP

elep_with_puma_probs - predicts ELEP (deprecated)

kwh_model - predicts usage

missing_features_model - fills NaN values predicted by given information

predict_pums - 
	append_kwh - predicts kwh and attaches it to pums table

vectorized_puma_regions - provides a mapping between feature index and puma region