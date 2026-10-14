# Appliances Energy Prediction — CSI 5810, Group 4

**Question:** How accurately can household appliance energy use be predicted from
indoor conditions, weather, and time-of-day features?

Ashley: coordinator/data preparation. Gabi: exploratory analysis/report.
Hala: modeling. Jacob: evaluation/interpretation. Roles may overlap.

## Start here
Python 3.10–3.13 recommended. Open this folder in VS Code; install Microsoft's Python
extension. Open Terminal > New Terminal, then on macOS run:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.prepare_data
python -m unittest discover -s tests -v
```

Windows PowerShell: use `py -m venv .venv`, then `.\.venv\Scripts\Activate.ps1`.
If activation is blocked, invoke `.\.venv\Scripts\python.exe` instead of `python`.
Select the .venv interpreter using “Python: Select Interpreter” in VS Code.

The preparation command downloads the public UCI dataset if absent. An offline option:
download the ZIP from the source link in docs/DATASET.md and place its
energydata_complete.csv in data/raw, then run the same command.

Expected: 19,735 rows, 31 predictors; chronological partitions 13,814 / 2,960 / 2,961.
Generated CSV files stay local and are excluded from Git. Source metadata and the
preparation report are tracked for review. Re-running updates the report run timestamp.

Read **docs/HANDOFF.md** for each teammate's next task and the shared loader.
Read **docs/START_IN_VSCODE.md** for GitHub instructions.
Read **docs/ASHLEY_WALKTHROUGH.md** to understand and explain your code.

## What is ready
- Reproducible download, validation, calendar features, and split generation.
- Dataset documentation, variable dictionary, and actual quality report.
- Common loader plus preparation checks.
- Coordination log and honest contribution/AI disclosure draft.

EDA, model training, evaluation results, and the final IEEE report remain team work.
Source: https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction
Dataset license: CC BY 4.0. Attribution: Candanedo (2017), doi:10.24432/C5VC8G.
