"""Ashley: download, validate, prepare features, and save reproducible splits.
Run from the project folder: python -m src.prepare_data
"""
import argparse
import hashlib
import io
import json
import platform
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://archive.ics.uci.edu/static/public/374/appliances+energy+prediction.zip"
TARGET = "Appliances"
SENSORS = [v for i in range(1, 10) for v in (f"T{i}", f"RH_{i}")]
WEATHER = ["T_out", "Press_mm_hg", "RH_out", "Windspeed", "Visibility", "Tdewpoint"]
RAW_COLUMNS = ["date", TARGET, "lights", *SENSORS, *WEATHER, "rv1", "rv2"]
TIME_FEATURES = ["hour", "day_of_week", "is_weekend", "hour_sin", "hour_cos", "weekday_sin", "weekday_cos"]
FEATURES = SENSORS + WEATHER + TIME_FEATURES


def acquire():
    """Keep original bytes; reuse the local file on subsequent runs."""
    path = ROOT / "data/raw/energydata_complete.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with urllib.request.urlopen(SOURCE, timeout=90) as response:
            archive = response.read()
        with zipfile.ZipFile(io.BytesIO(archive)) as z:
            payload = z.read("energydata_complete.csv")
        path.write_bytes(payload)
    return path


def prepare(raw):
    """Validate rather than silently invent replacements or delete energy peaks."""
    missing = sorted(set(RAW_COLUMNS) - set(raw.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    df = raw[RAW_COLUMNS].copy()
    audit = {"raw_rows": len(df), "raw_columns": len(raw.columns),
             "missing_cells": int(df.isna().sum().sum()),
             "exact_duplicate_rows_removed": int(df.duplicated().sum())}
    df = df.drop_duplicates().copy()
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S", errors="raise")
    for column in RAW_COLUMNS[1:]:
        df[column] = pd.to_numeric(df[column], errors="raise")
    if df.isna().any().any() or not np.isfinite(df[RAW_COLUMNS[1:]].to_numpy()).all():
        raise ValueError("Missing/non-finite values found. Review before preparing data.")
    if df["date"].duplicated().any():
        raise ValueError("Conflicting rows share a timestamp; review instead of arbitrarily deleting.")
    if (df[[TARGET, "lights"]] < 0).any().any():
        raise ValueError("Negative energy reading; investigate source data.")
    humidity = [c for c in df if c.startswith("RH_")]
    if ((df[humidity] < 0) | (df[humidity] > 100)).any().any():
        raise ValueError("Humidity outside 0-100%; investigate source data.")
    df = df.sort_values("date").reset_index(drop=True)
    # Stable IDs permit matching predictions to timestamps without using dates as predictors.
    df.insert(0, "row_id", np.arange(len(df)))
    df["hour"] = df.date.dt.hour
    df["day_of_week"] = df.date.dt.dayofweek  # Monday=0, Sunday=6
    df["is_weekend"] = (df.day_of_week >= 5).astype(int)
    fractional_hour = df.hour + df.date.dt.minute / 60
    # Sine/cosine preserve adjacency across midnight and the Sunday/Monday boundary.
    df["hour_sin"] = np.sin(2 * np.pi * fractional_hour / 24)
    df["hour_cos"] = np.cos(2 * np.pi * fractional_hour / 24)
    df["weekday_sin"] = np.sin(2 * np.pi * df.day_of_week / 7)
    df["weekday_cos"] = np.cos(2 * np.pi * df.day_of_week / 7)
    audit.update(clean_rows=len(df), start=str(df.date.min()), end=str(df.date.max()),
                 non_10_minute_gaps=int((df.date.diff().dropna() != pd.Timedelta(minutes=10)).sum()),
                 feature_count=len(FEATURES), dropped_predictors=["lights", "rv1", "rv2"],
                 missing_values_policy="Fail for review; no imputation needed for original dataset.",
                 outlier_policy="Retain all valid energy peaks; no clipping or IQR deletion.")
    return df, audit


def split_ids(n, seed=42):
    """Same 70/15/15 counts; chronological is primary, random is a comparison."""
    if n < 20:
        raise ValueError("Need at least 20 rows for the project splits.")
    first, second = int(n * .70), int(n * .85)
    chronological = np.arange(n)
    random = np.random.default_rng(seed).permutation(n)
    return {method: dict(zip(("train", "validation", "test"),
                             (ids[:first], ids[first:second], ids[second:])))
            for method, ids in (("chronological", chronological), ("random", random))}


def run():
    path = acquire()
    df, audit = prepare(pd.read_csv(path))
    processed = ROOT / "data/processed"
    reports = ROOT / "reports"
    processed.mkdir(parents=True, exist_ok=True)
    reports.mkdir(parents=True, exist_ok=True)
    df.to_csv(processed / "prepared.csv", index=False)
    memberships = pd.DataFrame({"row_id": df.row_id, "date": df.date})
    audit["splits"] = {}
    for method, partitions in split_ids(len(df)).items():
        memberships[method] = ""
        audit["splits"][method] = {}
        for name, ids in partitions.items():
            memberships.loc[ids, method] = name
            subset = df.iloc[ids].sort_values("date")
            subset[["row_id", "date", TARGET, *FEATURES]].to_csv(
                processed / f"{method}_{name}.csv", index=False)
            audit["splits"][method][name] = {"rows": len(subset),
                "start": str(subset.date.min()), "end": str(subset.date.max())}
    memberships.to_csv(processed / "split_membership.csv", index=False)
    # An unusual-value flag derived only from primary training data; nothing is removed.
    train = df.iloc[split_ids(len(df))["chronological"]["train"]]
    q1, q3 = train[TARGET].quantile([.25, .75])
    threshold = float(q3 + 1.5 * (q3 - q1))
    audit["training_energy_review"] = {"upper_IQR_threshold_Wh": threshold,
        "training_rows_above_threshold_retained": int((train[TARGET] > threshold).sum())}
    audit.update(raw_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                 run_utc=datetime.now(timezone.utc).isoformat(), seed=42,
                 python=platform.python_version(), pandas=pd.__version__, numpy=np.__version__)
    (reports / "data_quality.json").write_text(json.dumps(audit, indent=2) + "\n")
    (processed / "feature_config.json").write_text(json.dumps({"target": TARGET,
        "features": FEATURES, "time_features": TIME_FEATURES,
        "non_time_features": SENSORS + WEATHER,
        "excluded": ["row_id", "date", TARGET, "lights", "rv1", "rv2"]}, indent=2) + "\n")
    metadata_path = ROOT / "data/raw/source_metadata.json"
    if not metadata_path.exists():
        metadata_path.write_text(json.dumps({"source": SOURCE,
            "dataset_page": "https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction",
            "first_recorded_access_utc": audit["run_utc"], "sha256": audit["raw_sha256"],
            "license": "CC BY 4.0", "citation": "Candanedo, L. (2017). Appliances Energy Prediction. UCI. doi:10.24432/C5VC8G"}, indent=2) + "\n")
    print(f"Prepared {len(df):,} rows with {len(FEATURES)} predictors.")
    print("Saved data/processed, reports/data_quality.json, and source metadata.")
    print("Primary chronological split:", {k: len(v) for k,v in split_ids(len(df))["chronological"].items()})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    run()
