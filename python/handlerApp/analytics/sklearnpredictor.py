import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import warnings
import base64
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    confusion_matrix,
    classification_report
)
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB

warnings.filterwarnings('ignore')


def train_model(data, **kwargs):
    """
    Train a scikit-learn model and return predictions with precision, recall, and F1 metrics.
    
    Parameters:
    -----------
    model_name : str
        Name of the sklearn model (e.g., 'LogisticRegression', 'RandomForestClassifier')
    label_column : str
        Name of the column to use as the target variable
    data : numpy.ndarray or pandas.DataFrame
        The dataset containing features and target
    column_names : list
        List of column names corresponding to the data
    test_size : float, optional (default=0.2)
        Proportion of dataset to use as test set
    random_state : int, optional (default=42)
        Random state for reproducibility
        
    Returns:
    --------
    str : Formatted string containing model evaluation metrics and plot.
    """

    test_size = kwargs.get('test_size', 0.2)
    random_state = kwargs.get('random_state', 42)
    model_name = kwargs.get('model', 'RandomForestClassifier')
    column_names = kwargs.get('column', list(data[-1]))
    label_column = kwargs.get('label', column_names[-1])
    data = data[0]
    
    # Convert to DataFrame if numpy array
    if isinstance(data, np.ndarray):
        df = pd.DataFrame(data, columns=column_names)
    else:
        df = data
    
    # Check if label column exists
    if label_column not in column_names:
        raise ValueError(f"Label column '{label_column}' not found in data. Available columns: {list(df.columns)}")
    
    # Separate features and target
    X = df.drop(columns=[label_column])
    y = df[label_column]
    
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Model mapping dictionary
    model_mapping = {
        # Classification models
        'LogisticRegression': LogisticRegression(max_iter=1000),
        'DecisionTreeClassifier': DecisionTreeClassifier(),
        'RandomForestClassifier': RandomForestClassifier(),
        'GradientBoostingClassifier': GradientBoostingClassifier(),
        'SVC': SVC(),
        'KNeighborsClassifier': KNeighborsClassifier(),
        'GaussianNB': GaussianNB(),
        
        # Regression models
        'LinearRegression': LinearRegression(),
        'Ridge': Ridge(),
        'Lasso': Lasso(),
        'DecisionTreeRegressor': DecisionTreeRegressor(),
        'RandomForestRegressor': RandomForestRegressor(),
        'GradientBoostingRegressor': GradientBoostingRegressor(),
        'SVR': SVR(),
        'KNeighborsRegressor': KNeighborsRegressor(),
    }
    
    # Get the model
    if model_name not in model_mapping:
        raise ValueError(f"Model '{model_name}' not supported. Available models: {list(model_mapping.keys())}")
    
    model = model_mapping[model_name]
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions on test set
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    
    # Determine if binary or multiclass
    unique_classes = np.unique(y)
    n_classes = len(unique_classes)
    
    # Calculate precision, recall, F1 for each class and overall
    if n_classes == 2:
        # Binary classification
        precision_binary = precision_score(y_test, y_pred, average='binary', zero_division=0)
        recall_binary = recall_score(y_test, y_pred, average='binary', zero_division=0)
        f1_binary = f1_score(y_test, y_pred, average='binary', zero_division=0)
        
        precision_per_class = precision_score(y_test, y_pred, average=None, zero_division=0)
        recall_per_class = recall_score(y_test, y_pred, average=None, zero_division=0)
        f1_per_class = f1_score(y_test, y_pred, average=None, zero_division=0)
    else:
        # Multiclass classification
        precision_binary = None
        recall_binary = None
        f1_binary = None
        
        precision_per_class = precision_score(y_test, y_pred, average=None, zero_division=0)
        recall_per_class = recall_score(y_test, y_pred, average=None, zero_division=0)
        f1_per_class = f1_score(y_test, y_pred, average=None, zero_division=0)

    # Weighted average (for both binary and multiclass)
    precision_weighted = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall_weighted = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1_weighted = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    # Macro average
    precision_macro = precision_score(y_test, y_pred, average='macro', zero_division=0)
    recall_macro = recall_score(y_test, y_pred, average='macro', zero_division=0)
    f1_macro = f1_score(y_test, y_pred, average='macro', zero_division=0)
    
    # Confusion matrix
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    # Classification report
    class_report = classification_report(y_test, y_pred, zero_division=0)
    
    # Build summary string
    summary_lines = []
    summary_lines.append(f"**Model:** {model_name}")
    summary_lines.append(f"**Target Column:** {label_column}")
    summary_lines.append(f"**Training Samples:** {len(X_train)}")
    summary_lines.append(f"**Test Samples:** {len(X_test)}")
    summary_lines.append(f"**Accuracy:** {accuracy:.4f}")
    
    summary_lines.append("\n### Precision, Recall, F1-Score")
    if n_classes == 2:
        summary_lines.append(f"- **Binary Precision:** {precision_binary:.4f}")
        summary_lines.append(f"- **Binary Recall:** {recall_binary:.4f}")
        summary_lines.append(f"- **Binary F1-Score:** {f1_binary:.4f}")
    
    summary_lines.append(f"- **Weighted Precision:** {precision_weighted:.4f}")
    summary_lines.append(f"- **Weighted Recall:** {recall_weighted:.4f}")
    summary_lines.append(f"- **Weighted F1-Score:** {f1_weighted:.4f}")
    summary_lines.append(f"- **Macro Precision:** {precision_macro:.4f}")
    summary_lines.append(f"- **Macro Recall:** {recall_macro:.4f}")
    summary_lines.append(f"- **Macro F1-Score:** {f1_macro:.4f}")
    
    summary_lines.append("\n### Per-Class Metrics")
    for i, class_label in enumerate(unique_classes):
        summary_lines.append(f"**Class {class_label}:**")
        summary_lines.append(f"  - Precision: {precision_per_class[i]:.4f}")
        summary_lines.append(f"  - Recall: {recall_per_class[i]:.4f}")
        summary_lines.append(f"  - F1-Score: {f1_per_class[i]:.4f}")

    summary_lines.append("\n### Confusion Matrix")
    summary_lines.append(f"\n```\n{conf_matrix}\n```")
    
    summary_lines.append("\n### Classification Report")
    summary_lines.append(f"\n```\n{class_report}\n```")

    # Plotting if target is numeric
    plot_png = None
    if np.issubdtype(y.dtype, np.number):
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, y_pred, alpha=0.7)
        plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)  # Line for perfect prediction
        plt.title('Actual vs Predicted')
        plt.xlabel('Actual Values')
        plt.ylabel('Predicted Values')
        plt.grid()
        
        # Save plot to a BytesIO object
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()  # Close the plot to free memory
        buf.seek(0)
        
        # Get the PNG data and encode it in base64
        plot_png = base64.b64encode(buf.getvalue()).decode('utf-8')
        plot_png = f"data:image/png;base64,{plot_png}"
    
    # Append the plot to the summary if available
    if plot_png:
        summary_lines.append("\n### Plot")
        summary_lines.append(f"![Actual vs Predicted]({plot_png})")

    # Return the formatted summary
    return "\n".join(summary_lines)


# Example usage with your sample data
if __name__ == "__main__":
    # Sample data (expanded for demonstration)
    np.random.seed(42)
    n_samples = 100
    
    sample_data = np.column_stack([
        np.random.uniform(25, 50, n_samples),  # age
        np.random.uniform(30000, 100000, n_samples),  # income
        np.random.uniform(40000, 120000, n_samples),  # salary
        np.random.randint(0, 2, n_samples),  # target
        np.random.randint(0, 2, n_samples),  # education_Bachelor
        np.random.randint(0, 2, n_samples),  # education_High School
        np.random.randint(0, 2, n_samples),  # education_Master
        np.random.randint(0, 2, n_samples),  # education_PhD
        np.random.randint(0, 2, n_samples),  # city_Chicago
        np.random.randint(0, 2, n_samples),  # city_Houston
        np.random.randint(0, 2, n_samples),  # city_Los Angeles
    ])
    
    column_names = [
        'age', 'income', 'salary', 'target', 'education_Bachelor', 
        'education_High School', 'education_Master', 'education_PhD', 
        'city_Chicago', 'city_Houston', 'city_Los Angeles'
    ]
    
    # Train the model
    result = train_model(
        model='RandomForestClassifier',
        label='target',
        data=[sample_data,column_names],
        test_size=0.2,
        random_state=42
    )
    
    # Print the formatted summary
    print(result)
