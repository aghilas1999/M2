from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
import joblib

def train_lr(X_train, y_train, file = None):

    # Initializing the linear regression model
    model = LinearRegression()

    # Training the model
    model.fit(X_train, y_train)

    # Save the model
    if file : joblib.dump(model, file)

    return model

def train_gradient_boosting_regressor(X_train, y_train, param, file = None):
    # GradientBoostingRegressor
    model = GradientBoostingRegressor()

    # Create the GridSearchCV object
    grid_search = GridSearchCV(model, param, scoring='neg_mean_squared_error', cv=5)

    # Fit the model to the data
    grid_search.fit(X_train, y_train)

    # Print the best hyperparameters
    print("Best hyperparameters:", grid_search.best_params_)

    # Get the best model
    best_model = grid_search.best_estimator_

    # Save the model
    if file : joblib.dump(best_model, file)

    return best_model

def train_xgboost(X_train, y_train, param, file = None):
# Initialize the XGBoost regressor with adjusted parameters
    xgb_model = XGBRegressor(objective='reg:squarederror', n_estimators=param[0], max_depth=param[1])

# Train the model
    xgb_model.fit(X_train, y_train)

    # Save the model
    if file : joblib.dump(xgb_model, file)

    return xgb_model

def train_random_forest_regressor(X_train, y_train, param, file=None):
    # RandomForestRegressor
    model = RandomForestRegressor()

    # Create the GridSearchCV object
    grid_search = GridSearchCV(model, param, scoring='neg_mean_squared_error', cv=5)

    # Fit the model to the data
    grid_search.fit(X_train, y_train)

    # Print the best hyperparameters
    print("Best hyperparameters:", grid_search.best_params_)

    # Get the best model
    best_model = grid_search.best_estimator_

    # Save the model
    if file:
        joblib.dump(best_model, file)

    return best_model