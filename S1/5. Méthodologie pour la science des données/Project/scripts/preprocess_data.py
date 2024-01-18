import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from IPython.display import display

def load_dataset(file_path):
    return pd.read_excel(file_path)

def load_dataset(file_path):
    return pd.read_excel(file_path)

def drop_na(dataset) :
    dataset = dataset.dropna()
    return dataset


def split_data(dataset, features, test_size, val_size):
    dataset_size = len(dataset)

    X = dataset[features].head(dataset_size - val_size)
    y = dataset['mass_X (g)'].head(dataset_size - val_size)

    X_val = dataset[features].tail(val_size)
    y_val = dataset['mass_X (g)'].tail(val_size)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_size, random_state=42)

    return X_train, X_test, X_val, y_train, y_test, y_val

def normalize(dataset,features):
    scaler = MinMaxScaler()
    dataset[features] = scaler.fit_transform(dataset[features])
    return dataset


def preprocess(dataset, features, test_size, val_size):
    dataset = dataset.dropna()
    normalize(dataset,features)
    return split_data(dataset, features, test_size, val_size)