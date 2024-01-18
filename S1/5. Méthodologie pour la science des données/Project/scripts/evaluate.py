# Evaluating model performance
def evaluate(model, X_test, y_test, f) :

    # Making predictions on the test set
    predictions = model.predict(X_test)

    # Calculating Error
    error =  f(y_test, predictions)

    return(error)