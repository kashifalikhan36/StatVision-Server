import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import classification_report, confusion_matrix, mean_absolute_error
import xgboost as xgb
import joblib
import os

df=pd.read_csv("new_train_dataset/processed_dataset_with_features.csv")

# Step 1: Data Preprocessing
# Encoding categorical features (Pitch Type, Outcome)
label_encoder = LabelEncoder()
df['Outcome'] = label_encoder.fit_transform(df['Outcome'])

# Scaling numerical features (Exit Velocity, Hit Distance, etc.)
scaler = StandardScaler()
df[['Exit Velocity', 'Hit Distance', 'Launch Angle', 'Spray Angle', 'Performance Score', 'Ball Trajectory']] = scaler.fit_transform(
    df[['Exit Velocity', 'Hit Distance', 'Launch Angle', 'Spray Angle', 'Performance Score', 'Ball Trajectory']])

# Step 2: Feature and Target Variables for Classification (Outcome)
X = df[['Exit Velocity', 'Hit Distance', 'Launch Angle', 'Spray Angle', 'Pitch Type', 'Performance Score', 'Ball Trajectory']]
y_classification = df['Outcome']  # Classification target: Outcome (Home Run, Double, etc.)

# Step 3: Feature and Target Variables for Regression (Home Run Favorability)
y_regression = df['Home Run Favorability']  # Regression target: Home Run Favorability (Continuous value)

# Step 4: KFold Cross-Validation
kf = KFold(n_splits=2, random_state=42, shuffle=True)

# Prepare the directory to save models
if not os.path.exists('models'):
    os.makedirs('models')

# Initialize lists to hold model evaluation results
classification_reports = []
confusion_matrices = []
mae_scores = []

# Cross-validation loop
for train_index, test_index in kf.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_class_train, y_class_test = y_classification.iloc[train_index], y_classification.iloc[test_index]
    y_reg_train, y_reg_test = y_regression.iloc[train_index], y_regression.iloc[test_index]

    # Step 5: Model Creation - Random Forest Classifier (for Outcome)
    class_model = RandomForestClassifier(n_estimators=100, random_state=42)
    class_model.fit(X_train, y_class_train)

    # Step 6: Classification Prediction and Evaluation
    y_class_pred = class_model.predict(X_test)

    # Store classification evaluation results
    classification_reports.append(classification_report(y_class_test, y_class_pred))
    confusion_matrices.append(confusion_matrix(y_class_test, y_class_pred))

    # Step 7: Model Creation - Random Forest Regressor (for Home Run Favorability)
    reg_model = RandomForestRegressor(n_estimators=100, random_state=42)
    reg_model.fit(X_train, y_reg_train)

    # Step 8: Regression Prediction and Evaluation
    y_reg_pred = reg_model.predict(X_test)

    # Calculate Mean Absolute Error (MAE) for regression
    mae = mean_absolute_error(y_reg_test, y_reg_pred)
    mae_scores.append(mae)

    # Save the models after each fold
    joblib.dump(class_model, f'models/random_forest_classifier_outcome_fold{train_index[0]}.joblib')
    joblib.dump(reg_model, f'models/random_forest_regressor_home_run_favorability_fold{train_index[0]}.joblib')

# Step 9: Display Results after Cross-Validation
# Classification Report
print("Classification Reports (for Outcome) from each fold:")
for i, report in enumerate(classification_reports):
    print(f"\nFold {i + 1}:")
    print(report)

# Confusion Matrices for Classification
print("\nConfusion Matrices (for Outcome) from each fold:")
for i, matrix in enumerate(confusion_matrices):
    print(f"\nFold {i + 1}:")
    print(matrix)

# Mean Absolute Error (MAE) for Regression
print("\nMean Absolute Errors (for Home Run Favorability) from each fold:")
for i, mae in enumerate(mae_scores):
    print(f"Fold {i + 1}: MAE = {mae}")

print("\nModels saved successfully in the 'models' folder.")
