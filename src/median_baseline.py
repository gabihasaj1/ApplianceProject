
from sklearn.dummy import DummyRegressor

from modeling_utils import run_model

if __name__ == "__main__":
    run_model(
        model_name="Median baseline",
        base_model=DummyRegressor(strategy="median"),
        param_grid={},  # nothing to tune
    )
