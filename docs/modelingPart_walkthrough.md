## modeling_utils.py - shared helpers used by every model script

Every model script imports from this file, so the loading, scoring, and tuning steps are written once and are identical for
every model. That matters: if each model were scored slightly differently, the comparison would not be fair.

##### What is in here:
  1. Where the data lives (DATA_DIR) and where results are saved (RESULTS_DIR)
  2. Reading the target and feature names from feature_config.json
  3. Loading the train / validation files for one split
  4. Calculating the three scores: MAE, RMSE, R2
  5. Trying several settings and keeping the best one (judged on VALIDATION)
  6. run_model(): runs steps 3-5 for both splits and saves the results

IMPORTANT: nothing here uses the TEST files. it's just used at the very end, in a separate script.

`load_config()` : Reads the data-prep lead's config file instead of typing the 31 feature names by hand
`load_split()` : loads the train and validation files for one split (chronological or random) and separates each into the features (X) and the energy values (y).
`score() ` : compares the real energy values with the model’s guesses and returns three scores: MAE, RMSE, and R².
`tune_on_validation()`: tries every combination of settings for a model, training on train and checking on validation each time, and keeps the one with the smallest mistakes (lowest MAE).
`run_model()`: the “do everything” function. It runs the tuning for both splits the same way, saves the results to the results folder, and prints a short summary.

## median_baseline.py

##### What it does
------------
Takes the median (middle value) of Appliances in the TRAINING file and
predicts that same number for every row in the validation file. It never
looks at temperature, humidity, weather, or time.

##### Why we need it
--------------
It is the floor. It answers: "do the features help at all?"
Any real model that cannot beat this has learned nothing useful.

##### Why median and not mean?
 The target has many low values and a few large spikes. The spikes pull the mean upward, while the median stays near a typical 10-minute reading. The median also tends to give a lower MAE.



##  Linear regression (second baseline)

##### What it does
------------
Finds the best straight-line relationship between the 31 features and
Appliances. Each feature gets one number (a coefficient) saying how much
energy goes up or down when that feature goes up.

##### Why we need it
--------------
It is the "simple model" bar. If kNN or random forest only barely beat it,
that is worth knowing, because linear regression is much easier to explain.

##### What to expect 
---------------------------------------------
- Better than the median baseline, but probably not by a lot. It cannot
  capture curved patterns like "a spike at dinner time only."
- A fairly small gap between chronological and random, because it learns one
  overall relationship and cannot "memorize" neighboring moments.

##### Why the scaler?
---------------
Scaling does not change linear regression's predictions. We keep it so the
coefficients are on comparable scales (useful later for interpretation) and
so the setup matches Ridge and kNN.

## Ridge regression

#####  What it does
------------
The same straight-line idea as linear regression, but it adds a "penalty"
that keeps the coefficients from getting too large. Bigger alpha = stronger
penalty = simpler, more cautious model.

#####  Why it fits this problem
------------------------
The room temperatures T1-T9 are probably strongly related to each other
(when one room is warm, others usually are too). Plain linear regression can
get unstable with related features; Ridge handles that better.

#####  Assumptions
-----------
Same as linear regression.

##### The setting we tune
-------------------
alpha - how strong the penalty is.
    very small alpha -> almost identical to plain linear regression
    large alpha      -> coefficients pushed toward 0, simpler model

#####  What to expect 
---------------------------------------------
- Very close to linear regression, maybe slightly better.
- If the best alpha is the smallest one in the list, the penalty did not
  really help here. 


## k-nearest neighbors (kNN)

##### What it does
------------
For each validation row, it finds the k most similar rows in the training
file (similar temperatures, humidity, weather, time) and predicts the
average of their Appliances values.

##### Why it fits this problem
------------------------
Moments with similar conditions probably used similar
amounts of energy.

##### Assumptions
-----------
- Rows that are close in feature space have similar energy use.
- Every feature counts equally when measuring "closeness" (after scaling).
  Weak point: kNN cannot ignore unhelpful features. Also, time appears twice
  in the features (hour AND hour_sin/hour_cos, day_of_week AND weekday
  sin/cos), so time may get extra weight in the distance.

##### Why scaling is essential
------------------------
Without it, a feature with big numbers (pressure is around 750) would
dominate a feature with small numbers (wind speed around 4).

##### Settings we tune
----------------
n_neighbors (k) - how many similar moments to average.
    small k -> follows noise, very "local"
    large k -> smoother, may blur real patterns
weights - "uniform" (all k neighbors count equally) or
          "distance" (closer neighbors count more)

##### What to expect 
---------------------------------------------
- This is where the random vs. chronological gap may be large. On the random
  split, the nearest neighbor of 7:40 PM is often 7:30 PM or 7:50 PM of the
  same day, which is almost a copy. On the chronological split, those
  neighbors are not available.
- The best k may be small on the random split and larger on the
  chronological split.

##### Speed
-----
Prediction is slower than the other models (it compares every validation row
to every training row), but this dataset is small enough that it should be OK.


## Random forest
==================

##### What it does
------------
Builds many decision trees. Each tree asks yes/no questions like
"is the kitchen humidity above 45?" -> "is the hour after 17?" -> guess.
Each tree is trained on a slightly different random sample of the data,
and the final prediction is the average of all trees.

##### Why it fits this problem
------------------------
- Handles curved patterns and combinations ("humid kitchen AND dinner
  time") without us having to describe them.
- Gives feature importances, which helps the evaluation part.

##### Assumptions
-----------
Very few about the shape of the relationship. One important limitation:
trees CANNOT predict outside the range they saw in training. If the test
weeks (May) are warmer than anything in training, the forest treats them like
the warmest days it knows. Good material for error analysis, but check
whether it actually shows up before claiming it.

##### Why no scaling?
---------------
Trees split on "above or below a value," so the scale of a feature does not
matter.

##### Settings we tune
----------------
max_depth        - how many questions deep each tree can go
                   (None = no limit; deeper = more detailed, more overfitting risk)
min_samples_leaf - smallest group a tree is allowed to end on
                   (bigger = smoother, less overfitting)
max_features     - how many features each question may choose from
                   (1.0 = all of them, "sqrt" = a random smaller subset)
n_estimators     - number of trees. Fixed at 200 here to save time; more
                   trees usually help a little but take longer.

##### What to expect 
---------------------------------------------
- Probably among the best on the random split.
- On the chronological split, its advantage over the simpler models may
  shrink. 

##### Speed
-----
12 combinations x 2 splits = 24 forests. This may take a few minutes.

