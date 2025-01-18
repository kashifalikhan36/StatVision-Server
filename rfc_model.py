from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error, classification_report
import pandas as pd

# Load the dataset
data = pd.read_csv("processed_dataset.csv")  # Replace with your dataset file name

# ------------------ Regression Model (Performance Score) ------------------

# Features and Target for Regression
X_reg = data[['Exit Velocity', 'Hit Distance', 'Launch Angle']]
y_reg = data['Performance Score']

# Split Data
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

# Train Regression Model
regressor = RandomForestRegressor(random_state=42)
regressor.fit(X_train_reg, y_train_reg)

# Predict and Evaluate Regression
predictions_reg = regressor.predict(X_test_reg)

# Compute Metrics
mse = mean_squared_error(y_test_reg, predictions_reg)  # Mean Squared Error
rmse = mse ** 0.5  # Root Mean Squared Error
mae = mean_absolute_error(y_test_reg, predictions_reg)  # Mean Absolute Error

# Express MSE and MAE as percentages of the average Performance Score
average_score = y_test_reg.mean()
mse_percentage = (mse / average_score) * 100
mae_percentage = (mae / average_score) * 100

# Print Results
print(f"Regression Evaluation:")
print(f"  Mean Squared Error (MSE): {mse:.2f}")
print(f"  Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"  Mean Absolute Error (MAE): {mae:.2f}")
print(f"  MSE as Percentage: {mse_percentage:.2f}%")
print(f"  MAE as Percentage: {mae_percentage:.2f}%")

# ------------------ Classification Model (Outcome) ------------------

# Features and Target for Classification
X_clf = data[['Exit Velocity', 'Hit Distance', 'Launch Angle']]
y_clf = data['Outcome']  # Categorical target

# Split Data
X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(X_clf, y_clf, test_size=0.2, random_state=42)

# Train Classification Model
classifier = RandomForestClassifier(random_state=42)
classifier.fit(X_train_clf, y_train_clf)

# Predict and Evaluate Classification
predictions_clf = classifier.predict(X_test_clf)
print("\nClassification Evaluation:")
print(classification_report(y_test_clf, predictions_clf))
