import copy
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler


class SharedModel:
	def __init__(self, df, outcome, demographic_variables, auxiliary_time_features, feat_transforms, mode, target_days,
				 time_series_default_values=None, scale=True, include_diffs=False,outcome_start_threshold=3,direct_predict=False, family = sm.families.Poisson()):
		self.outcome = outcome
		self.df = copy.deepcopy(df)
		if time_series_default_values is None:
			assert auxiliary_time_features == []
		self.time_series_features = [outcome] + auxiliary_time_features
		if mode == 'eval_mode':
			for t in self.time_series_features:
				self.df[t] = [v[:-target_days[-1]] for v in self.df[t]]
		self.auxiliary_time_features = auxiliary_time_features
		self.auxiliary_time_data_dict = {aux_ts: list(self.df[aux_ts]) for aux_ts in self.auxiliary_time_features}

		self.demographics_variables = demographic_variables
		self.demographic_data_dict = {d: list(self.df[d]) for d in self.demographics_variables}

		self.feat_transforms = feat_transforms
		self.mode = mode
		self.target_days = target_days
		self.outcome = outcome
		self.outcome_data = list(list(v) for v in self.df[self.outcome])

		self.time_series_default_values = time_series_default_values

		self.time_series_index_dict = {i: self.time_series_features[i] for i in range(len(self.time_series_features))}
		self.feature_transforms = feat_transforms
		self.outcome_start_threshold = outcome_start_threshold
		if scale:
			self.scaler = StandardScaler
		else:
			self.scaler = None
		self.X_train = None
		self.y_train = None
		self.model = None

		self.predictions = None
		self.include_diffs = include_diffs
		self.direct_predict = direct_predict
		if self.direct_predict:
			assert len(self.target_days) == 1
		self.family = family

	def create_demographic_features(self, county_index):
		return [self.demographic_data_dict[d][county_index] for d in self.demographic_data_dict]

	def create_time_series_features(self, county_index, time_index):
		# Find outcome time series features:
		outcome_features = []
		for fn in self.feature_transforms[self.outcome]:
			outcome_features.append(fn(self.outcome_data[county_index][time_index]))
			if self.include_diffs:
				if time_index == 0:
					outcome_features.append(fn(self.outcome_data[county_index][time_index]))
					outcome_features.append(fn(self.outcome_data[county_index][time_index]))
				else:
					if self.outcome_data[county_index][time_index - 1] == 0:
						dif = 1
					else:
						dif = self.outcome_data[county_index][time_index] / self.outcome_data[county_index][time_index - 1]
					outcome_features.append(fn(dif))
					# outcome_features.append(fn(max(dif, 0)))
					# outcome_features.append(fn(max(-dif, 0)))

		# Find auxiliary time series features:
		if time_index - self.target_days[-1] < 0:
			auxiliary_features = []
			for feat in self.auxiliary_time_features:
				auxiliary_features.extend([self.time_series_default_values[feat]] * len(self.feature_transforms[feat]))
		else:
			auxiliary_features = []
			for feat in self.auxiliary_time_features:
				for fn in self.feature_transforms[feat]:
					auxiliary_features.append(
						fn(self.auxiliary_time_data_dict[feat][county_index][time_index - self.target_days[-1]]))

		return outcome_features + auxiliary_features

	def create_dataset(self):
		X_train = []
		y_train = []
		# For each county in a dataset:
		for county_index in range(len(self.df)):
			# For each time period in a dataset:
			for time_index in range(len(self.outcome_data[county_index])):
				thresh = self.outcome_data[county_index][time_index] >= self.outcome_start_threshold
				if self.outcome == 'deaths_per_cap':
					thresh = self.outcome_data[county_index][time_index] >= self.outcome_start_threshold/list(self.df['PopulationEstimate2018'])[county_index]*100000

				if thresh and time_index > 0:
					# Compute time series features
					time_series_features = self.create_time_series_features(county_index, time_index - 1)

					# Compute demographic features (if applicable)
					demographic_features = self.create_demographic_features(county_index)
					if self.direct_predict:
						if time_index++self.target_days[-1] < len(self.outcome_data[county_index]):
							X_train.append(time_series_features + demographic_features)
							y_train.append(self.outcome_data[county_index][time_index+self.target_days[-1]-1])
					else:
						X_train.append(time_series_features + demographic_features)
						y_train.append(self.outcome_data[county_index][time_index])


		# Fit and apply scaler if applicable
		if self.scaler:
			self.scaler = StandardScaler().fit(X_train)
			X_train = self.scaler.transform(X_train)
			X_train = [list(x) for x in X_train]

		# Add in bias term post scaling
		self.X_train = [x + [1] for x in X_train]
		self.y_train = y_train

	def fit_model(self):
		assert self.X_train, 'Create training data first'
		self.model = sm.GLM(self.y_train, self.X_train, family=self.family)
		# self.model = self.model.fit_regularized(alpha=.01, L1_wt=.5)
		self.model = self.model.fit_regularized(alpha=.00, L1_wt=.5)

	def predict(self):
		self.predictions = []
		tmp_df = copy.deepcopy(self.df)
		tmp_outcomes = copy.deepcopy(self.outcome_data)
		for county_index in range(len(self.df)):
			if self.direct_predict:
				time_index = len(self.outcome_data[county_index]) - 1
				time_series_features = self.create_time_series_features(county_index, time_index)
				demographic_features = self.create_demographic_features(county_index)
				if self.scaler:
					features = list(self.scaler.transform([time_series_features + demographic_features])[0]) + [1]
				else:
					features = time_series_features + demographic_features + [1]
				prediction = self.model.predict([features])[0]
				county_predictions = [prediction]

			else:
				county_predictions = []

				for i in range(self.target_days[-1]):
					time_index = len(self.outcome_data[county_index]) - 1
					time_series_features = self.create_time_series_features(county_index, time_index)
					demographic_features = self.create_demographic_features(county_index)
					if self.scaler:
						features = list(self.scaler.transform([time_series_features + demographic_features])[0]) + [1]
					else:
						features = time_series_features + demographic_features + [1]
					prediction = self.model.predict([features])[0]
					if i + 1 in self.target_days:
						county_predictions.append(prediction)
					## TODO: CHECK THAT THIS SHOULDNT BE TEMP OUTCOMES
					self.outcome_data[county_index].append(prediction)
			self.predictions.append(county_predictions)
		self.df = tmp_df
		self.outcome_data = tmp_outcomes
