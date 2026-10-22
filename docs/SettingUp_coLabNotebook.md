# Appliances Energy Prediction — data prep and modeling
**https://colab.research.google.com/drive/1haMbwn1Yakmil8M8LR29yNLQZcqVQFQd?usp=sharing**
### Changes from the Ashley original scripts

The data-preparation logic (cleaning, features, 70/15/15 splits, seed 42) is unchanged. Only three things were adapted so the code runs as a notebook:

1. **Project folder:** `Path(__file__)` does not exist in a notebook, so the project folder (`ROOT`) is found once in the setup cell: in Colab it searches the user's Drive for the group folder by name; locally it uses the notebook's folder. No paths need editing.
2. **`argparse` removed:** it fails inside Jupyter/Colab; the data preparation is called directly with `run()`.
3. **Skip if already built:** data preparation runs only when the processed files are missing (`REBUILD_DATA = True` forces a rebuild), so re-running the notebook does not rebuild the data each time.
4. **Data-prep `load_split` helper not included:** its relative import (`from .prepare_data import ROOT`) fails in a notebook, and its loading job is done by `load_split` in the modeling helpers. Two of its ideas are kept for later: returning `row_id`/`date` for error analysis, and `include_time=False` to test without time features.
