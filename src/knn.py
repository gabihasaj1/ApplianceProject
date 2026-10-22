from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from modeling_utils import run_model

if __name__ == "__main__":
    model = Pipeline([
        ("scale", StandardScaler()),
        ("model", KNeighborsRegressor()),
    ])

    param_grid = {
        "model__n_neighbors": [3, 5, 10, 20, 50, 100],
        "model__weights": ["uniform", "distance"],
    }

    run_model(model_name="kNN", base_model=model, param_grid=param_grid)
