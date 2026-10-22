from sklearn.ensemble import RandomForestRegressor

from modeling_utils import SEED, run_model

if __name__ == "__main__":
    model = RandomForestRegressor(n_estimators=200, random_state=SEED, n_jobs=-1)

    param_grid = {
        "max_depth": [10, 20, None],
        "min_samples_leaf": [1, 5],
        "max_features": [1.0, "sqrt"],
    }

    run_model(model_name="Random forest", base_model=model, param_grid=param_grid)
