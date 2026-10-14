# Appliances Energy Prediction
CSI 5810 — Group 4

**Research question:** How accurately can household appliance energy use be predicted from indoor conditions, weather, and time-of-day features?

## Setup

Clone the repo, or pull the latest changes if you already have it. Open the project folder in VS Code and use **Python 3.12**.

Run these in the terminal from the project folder (Mac):

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

In VS Code, go to **Python: Select Interpreter** and select `.venv`.

You only need to create the environment once. For a new terminal session, activate it again:

```bash
source .venv/bin/activate
```

## Prepare the data

```bash
python -m src.prepare_data
```

This downloads the dataset, checks for missing values and duplicates, adds time features, and creates training, validation, and test splits.

The files are saved in `data/processed`. CSV files aren't tracked on GitHub, so everyone needs to run this locally.

There are chronological and random splits. Chronological is our main setup; random is for comparison.

## Use the prepared data

You can read the CSVs or use this helper in your code:

```python
from src.load_data import load_split

X_train, y_train, train_info = load_split("chronological", "train")
X_val, y_val, val_info = load_split("chronological", "validation")
```

- `X`: input features
- `y`: appliance energy use
- `info`: row IDs and dates

Change `"chronological"` to `"random"` for the other split. Save the test set for final evaluation after choosing the model and settings.

Don't run `load_data.py` directly. It's a helper that you import into your code.

## Check that everything works

```bash
python -m unittest discover -s tests -v
```

You should see five tests pass and `OK`.

## Team

- Ashley — coordination and data preparation
- Gabi — exploratory analysis and report
- Hala — modeling
- Jacob — evaluation and interpretation

Roles can overlap. Data preparation is set up; analysis, modeling, and evaluation are next.

## Dataset

[UCI Appliances Energy Prediction](https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction)

Candanedo, L. (2017). *Appliances Energy Prediction*. UCI Machine Learning Repository. DOI: 10.24432/C5VC8G. Licensed under CC BY 4.0.