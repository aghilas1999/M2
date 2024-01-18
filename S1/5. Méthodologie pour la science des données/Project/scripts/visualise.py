from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns


def check_missing_values(data):
    print("\nMissing values in the dataset:")
    display(data.isna().sum())

def display_head(data, n=5):
    print("Head of the dataset:")
    display(data.head(n))

def display_info(data):
    print("\nDataset information:")
    display(data.info())

def display_summary_statistics(data):
    print("\nSummary statistics of the dataset:")
    display(data.describe())

def display_correlation_matrix(data):

    # Selecting only numeric columns
    numeric_columns = data.select_dtypes(include=['float64', 'int64'])

    # Calculating the correlation matrix for numeric columns
    correlation_matrix = numeric_columns.corr()

    # Plotting the correlation matrix as a heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Matrix')
    plt.show()