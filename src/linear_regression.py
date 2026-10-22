from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from modeling_utils import run_model

if __name__ == "__main__":
    model = Pipeline([
        ("scale", StandardScaler()),     # learned from TRAIN only, inside fit()
        ("model", LinearRegression()),
    ])

    run_model(
        model_name="Linear regression",
        base_model=model,
        param_grid={},  # nothing to tune
    )
