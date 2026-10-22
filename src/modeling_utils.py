# modeling_utils.py - shared helpers used by every model script


import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import ParameterGrid


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
RESULTS_DIR = PROJECT_ROOT / "results"

SEED = 42  
SPLITS = ["chronological", "random"]  # we run every model on both splits


# Target and feature names 
def load_config():
    with open(DATA_DIR / "feature_config.json") as f:
        config = json.load(f)
    return config["target"], config["features"]


TARGET, FEATURES = load_config()


def load_split(split_name, parts=("train", "validation")):
 
    # Load the given parts of one split 
    data = {}
    for part in parts:
        df = pd.read_csv(DATA_DIR / f"{split_name}_{part}.csv")
        data[part] = (df[FEATURES], df[TARGET])
    return data

def score(y_true, y_pred):

    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "R2": r2_score(y_true, y_pred),
    }


#  Try several settings, keep the best one on VALIDATION
def tune_on_validation(base_model, param_grid, X_train, y_train, X_val, y_val):
  
    tried_rows = []
    best_params, best_scores = None, None

    for params in ParameterGrid(param_grid):
        model = clone(base_model).set_params(**params)  # fresh, untrained copy
        model.fit(X_train, y_train)
        scores = score(y_val, model.predict(X_val))

        tried_rows.append({**params, **scores})

        if best_scores is None or scores["MAE"] < best_scores["MAE"]:
            best_params, best_scores = params, scores

    return best_params, best_scores, pd.DataFrame(tried_rows)


# Runs the same steps for the chronological and the random split, so the ONLY difference between the two results is how the data was split.
def run_model(model_name, base_model, param_grid):
   
    RESULTS_DIR.mkdir(exist_ok=True)
    slug = model_name.lower().replace(" ", "_")
    summary_rows = []

    for split_name in SPLITS:
        data = load_split(split_name)
        X_train, y_train = data["train"]
        X_val, y_val = data["validation"]

        best_params, best_scores, tried = tune_on_validation(
            base_model, param_grid, X_train, y_train, X_val, y_val
        )
        tried.to_csv(RESULTS_DIR / f"tuning_{slug}_{split_name}.csv", index=False)

        summary_rows.append(
            {"model": model_name, "split": split_name,
             "best_params": str(best_params), **best_scores}
        )

    summary = pd.DataFrame(summary_rows)
    summary.to_csv(RESULTS_DIR / f"val_{slug}.csv", index=False)

    print(f"\n=== {model_name} (validation scores) ===")
    print(summary.round(3).to_string(index=False))
    return summary
