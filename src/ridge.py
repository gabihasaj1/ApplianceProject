from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from modeling_utils import run_model

if __name__ == "__main__":
    model = Pipeline([
        ("scale", StandardScaler()),  # needed: the penalty treats all features alike
        ("model", Ridge()),
    ])

    param_grid = {
        "model__alpha": [0.01, 0.1, 1, 10, 100, 1000],
    }

    run_model(model_name="Ridge", base_model=model, param_grid=param_grid)
