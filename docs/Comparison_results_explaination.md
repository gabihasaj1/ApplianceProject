# Comparison results: what we got for the validation set 

## What the comparison cell does

Using the comparision cell in the notebook which  reads the result files that each model cell saved in the `results` folder and puts them in one table, so we can see every model next to each other.

For every model it shows three scores, once for the chronological split and once for the random split:

- **MAE**: on average, how many Wh the model is off by. Lower is better.
- **RMSE**: also in Wh, but big misses count a lot more. Lower is better.
- **R²**: how much of the ups and downs in energy use the model follows. 1 is perfect, 0 means no better than always guessing the average, below 0 means worse than that.

It also adds one extra column, the **gap**, which is chronological MAE minus random MAE. A big positive gap means the model looked a lot better on the random split than on the chronological one.

## The table we got

| Model | MAE chrono | MAE random | RMSE chrono | RMSE random | R² chrono | R² random | Gap |
|---|---|---|---|---|---|---|---|
| Median baseline | 42.6 | 48.5 | 98.1 | 104.1 | -0.13 | -0.15 | -5.9 |
| kNN | 43.5 | 29.3 | 88.8 | 65.9 | 0.07 | 0.54 | 14.3 |
| Ridge | 49.3 | 50.9 | 86.2 | 89.3 | 0.13 | 0.16 | -1.6 |
| Random forest | 52.6 | 29.2 | 87.0 | 61.3 | 0.11 | 0.60 | 23.5 |
| Linear regression | 53.4 | 51.4 | 87.9 | 89.0 | 0.09 | 0.16 | 2.0 |

## Going through it model by model

**Median baseline.** It guesses the same number every time. On the chronological split it's off by 42.6 Wh on average, and its R² is -0.13. The negative R² is expected, since a single fixed guess can't follow any ups and downs. Its MAE is still low, because most readings are quiet and the median is close to them.

**kNN.** On the random split it's off by 29.3 Wh and R² is 0.54, which looks good. On the chronological split it's off by 43.5 Wh and R² falls to 0.07. That's a gap of 14.3 Wh. So most of what looked good on the random split doesn't carry over to future dates.

**Random forest.** Same story, even stronger. 29.2 Wh and R² 0.60 on the random split, but 52.6 Wh and R² 0.11 on the chronological split. The gap is 23.5 Wh, the biggest in the table.

**Ridge.** Almost the same on both splits (49.3 and 50.9 Wh). The gap is small, -1.6 Wh. On the chronological split it has the best RMSE (86.2) and the best R² (0.13) of all the models.

**Linear regression.** Also almost the same on both splits (53.4 and 51.4 Wh), gap 2.0 Wh. Slightly worse than Ridge on the chronological split.

## What it means

**1. The random split makes kNN and random forest look much better than they really are.**
Readings 10 minutes apart are almost the same. When rows are shuffled, the moments right before and after a validation moment usually end up in training, and kNN and random forest can basically match them. On the chronological split those near-copies aren't there, and their scores drop a lot. The linear models can't use that trick, so their scores barely move. This is the main finding the project asked us to show. It fits the usual explanation, but we haven't tested the reason directly.

**2. On the chronological split, no model beats the median baseline on MAE, but all of them beat it on RMSE and R².**
That sounds like a contradiction, but it isn't. The median is close on the many quiet moments, so its average miss is small. It badly misses the spikes, and RMSE punishes those. The models do better on the spikes but make bigger mistakes on the quiet moments.

One possible reason, which we still need to test: these models are trained to reduce squared error, so their guesses get pulled toward the average, and the spikes push the average up. That would make them guess a bit too high on quiet moments. Training on a log version of the energy values is one way to check this.

**3. For the gap**
The median baseline learns nothing, but its MAE still differs by 5.9 Wh between the splits. That's because the two validation sets are different data. The chronological one is one stretch of time and the random one mixes all months. So part of every gap is just different validation periods.

A fairer way to show finding 1 is to compare each model to the baseline inside the same split:

| Model | Random split | Chronological split |
|---|---|---|
| kNN | about 40% better than baseline | about 2% worse |
| Random forest | about 40% better | about 24% worse |
| Ridge | about 5% worse | about 16% worse |
| Linear regression | about 6% worse | about 25% worse |

Finding 1 still holds this way: kNN and random forest go from clearly better than the baseline to worse than it.

