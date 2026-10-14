# Team handoff

Question: How accurately can household appliance energy use be predicted from indoor conditions, weather, and time-of-day features?

Unit: a 10-minute observation of one house. Target: Appliances, in Wh.
This is same-interval estimation using observed conditions. It is not a next-day
forecast: future weather/indoor readings would not be available in advance.
Proposed success criterion: improve MAE and RMSE over a training-mean baseline on
held-out later dates, with R² also reported. No performance claim has been made yet.

## Ashley — coordinator and preparation
Run and understand src/prepare_data.py and inspect reports/data_quality.json.
Code checks validity, removes exact duplicate rows if present, sorts timestamps,
adds seven calendar features, and saves both split schemes. Nothing is scaled,
imputed, clipped, or selected using full-data statistics.
Keep project log and task ownership current; actual meetings must be added by the team.

## Gabi — exploratory analysis and report
Start with chronological_train.csv for model-guiding EDA. Plot energy distribution,
energy by hour, temperature/humidity relationships, and correlations. Give axes
units and write interpretations. Leave the primary test data untouched until final evaluation.
Assemble 4–6 pages of IEEE main content, with every member writing their own section.
Full-data descriptive summaries can be reported later, labeled as descriptive only.

## Hala — modeling
Use the loader below. Compare a training-mean baseline and at least two models
(e.g. linear regression and random forest). Add needed packages to requirements
with versions once chosen. Fit scalers/imputers only inside a pipeline on training
rows. Tune on validation rows or use TimeSeriesSplit inside chronological training.
Do not put row_id/date/Appliances into X. Keep time-feature ablation available.

```python
from src.load_data import load_split
X_train, y_train, train_info = load_split('chronological', 'train')
X_val, y_val, val_info = load_split('chronological', 'validation')
# Fit on X_train/y_train. Choose settings using X_val/y_val.
# For the no-time-feature comparison:
X_train_no_time, y_train, _ = load_split('chronological', 'train', include_time=False)
```
Run scripts as modules from the root (for example python -m src.modeling).
Notebook users should set the working directory to the project root.

## Jacob — evaluation and interpretation
Use identical saved splits across models. Report MAE/RMSE in Wh and R², residual
plots, and errors by hour and high-use periods. Compare random and chronological
protocols; random splits mix neighboring observations and can look optimistic.
Their test rows differ, so comparisons also reflect different test composition.
Select methods using validation results. Evaluate test only after choices are fixed.
Keep the chronological experiment primary; don't use results from random training
(which includes later dates) to choose the primary model's settings.
For training-derived high-use thresholds, use training data only.
Analyze uncertainty/sensitivity and at least two realistic improvements.
Energy savings are potential applications, not demonstrated causal savings.

## Shared files
- data/processed/prepared.csv: complete prepared table, including excluded columns for auditing.
- data/processed/{chronological,random}_{train,validation,test}.csv: six modeling tables.
- data/processed/feature_config.json: exact approved feature lists.
- data/processed/split_membership.csv: reproducible row membership.
- reports/data_quality.json: actual preparation results.
- docs/DATASET.md and docs/DATA_DICTIONARY.md: source, variables, decisions.

Data CSVs are ignored by Git: each teammate generates the same files locally.
Python/numpy versions are pinned for consistent random memberships.
