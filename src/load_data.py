# This lets everyone load the prepared data without repeating the setup.
# Run prepare_data first, then import this helper instead of running this file directly:
# from src.load_data import load_split
# X, y, info = load_split("chronological", "train")
# X = input features, y = energy use, info = row IDs and dates.
# You can change "train" to "validation"/"test" or "chronological" to "random".

import pandas as pd
from .prepare_data import ROOT


def load_split(method="chronological", partition="train", include_time=True):
    """Return X, y, metadata. Metadata is for error analysis, never predictors."""
    if method not in ("chronological", "random") or partition not in ("train", "validation", "test"):
        raise ValueError("Use chronological/random and train/validation/test.")
    folder = ROOT / "data/processed"
    config = json.loads((folder / "feature_config.json").read_text())
    df = pd.read_csv(folder / f"{method}_{partition}.csv", parse_dates=["date"])
    columns = config["features"] if include_time else config["non_time_features"]
    return df[columns].copy(), df[config["target"]].copy(), df[["row_id", "date"]].copy()
