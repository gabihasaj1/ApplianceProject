# Data preparation section — working draft

The UCI Appliances Energy Prediction dataset [1] contains 19,735 observations and
29 original columns, including the timestamp and target. The target, Appliances,
measures appliance energy use in Wh. Observations span January 11 to May 27, 2016,
at uninterrupted 10-minute intervals. Our executed preparation checks found no
missing cells or exact duplicate rows, so all 19,735 records were retained.
Timestamps were parsed and sorted, and measurements were validated for numeric
values, finite values, nonnegative energy, and humidity within 0–100%.
Valid energy spikes were retained rather than treated automatically as errors.

Seven calendar features were constructed: hour, weekday, weekend indicator, and
sine/cosine encodings of time of day and weekday. The primary predictor set contains
31 variables: 18 temperature/humidity sensor variables, six weather variables, and
seven calendar features. The synthetic random variables rv1 and rv2 were excluded.
The contemporaneous lights measurement was also excluded to keep the predictors
aligned with the stated conditions/weather/time question. Neither the timestamp,
row identifier, nor target was supplied as a predictor.

The primary chronological split allocates the earliest 13,814 observations to
training, the next 2,960 to validation, and the last 2,961 to testing. A reproducible
random comparison split uses the same counts and seed 42. No scaling, imputation,
or other learned transformation was applied to the entire dataset. Any such
transformations used in modeling must be fit on the training portion only.
The source checksum, preparation results, and split boundaries are stored with
the project. The final test sets are reserved for evaluation after model selection.

These predictors describe the same interval as the target; the task is estimation
from measured conditions, not an advance forecast. One house and a partial year
limit generalization. No causal energy savings are established by this preparation.

[1] L. Candanedo, “Appliances Energy Prediction,” UCI Machine Learning Repository,
2017, doi: 10.24432/C5VC8G. License: CC BY 4.0.

