# Dataset and preparation decisions

Source: https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction
Download: https://archive.ics.uci.edu/static/public/374/appliances+energy+prediction.zip
Citation: L. Candanedo, “Appliances Energy Prediction,” UCI Machine Learning Repository,
2017, doi: 10.24432/C5VC8G. License: CC BY 4.0,
https://creativecommons.org/licenses/by/4.0/ . Credit the dataset in the final report.
The recorded access timestamp and raw checksum are in data/raw/source_metadata.json.

UCI describes about 4.5 months of observations from one low-energy house in Belgium.
Indoor sensors were averaged into 10-minute intervals; external station weather was
merged by time, with hourly weather interpolated. This is public environmental and
energy data, with no direct personal identifiers in the supplied table. Consumption
patterns may indirectly reveal occupancy; no occupant inference is part of this project.
One house and a partial year limit generalization to other homes, seasons, and climates.

## Decisions fixed before modeling
- The unmodified downloaded CSV is preserved in data/raw.
- Exact duplicate rows are removed if present. Conflicting timestamps stop the run.
- Missing/non-numeric/infinite values, invalid timestamps, negative energy, and
  humidity outside 0–100% stop the run for review. No automatic imputation.
- Valid high-energy peaks are retained. They may be meaningful demand, not errors.
- Timestamps remain timezone-naive because the source does not specify a timezone
  offset; no timezone or daylight-saving conversion is invented.
- Calendar features require no learning from data: hour, weekday, weekend, and
  sine/cosine pairs for time of day and weekday.
- rv1/rv2 are source-injected random controls and excluded from the main model.
- lights is a contemporaneous energy measurement, outside the specified conditions/
  weather/time question; exclude it from primary predictors. This is a scope and
  availability decision, not a claim that the column is inherently leakage.
- Raw timestamps, row IDs, and target are never predictors.
- No normalization or scaling before splitting. Hala fits any learned preprocessing
  only on training data. Numeric calendar features need no categorical encoding.
- Use a chronological 70/15/15 split as primary and a seeded random split with the
  same counts as comparison. Adjacent observations are correlated; a later sensitivity
  analysis with a temporal gap can test dependence around split boundaries.

Counts and date boundaries are generated in reports/data_quality.json. There are no
model scores yet; teammates will complete EDA, modeling, evaluation, and the final report.
