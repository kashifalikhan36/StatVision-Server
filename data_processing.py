import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

data = pd.read_csv("collected_metrics_train.csv")

# Encode the 'Pitch Type' column as numeric values
label_encoder = LabelEncoder()
data['Pitch Type'] = label_encoder.fit_transform(data['Pitch Type'])

def calculate_performance_score(row):
    return (row['Exit Velocity'] * 0.3) + (row['Hit Distance'] * 0.3) + (row['Launch Angle'] * 0.2) + (row['Spray Angle'] * 0.1) + (row['Pitch Type'] * 0.1)

def classify_outcome(row):
    if row['Hit Distance'] > 400 and row['Exit Velocity'] > 100:
        return "Home Run"
    elif row['Hit Distance'] > 200:
        return "Double"
    elif row['Hit Distance'] > 100:
        return "Single"
    else:
        return "Out"

def calculate_ball_trajectory(row):
    return row['Launch Angle'] * row['Exit Velocity']

def is_home_run_pitch(row):
    return 1 if row['Pitch Type'] == label_encoder.transform(['Fastball'])[0] and row['Exit Velocity'] > 95 else 0

data['Performance Score'] = data.apply(calculate_performance_score, axis=1)
data['Outcome'] = data.apply(classify_outcome, axis=1)
data['Ball Trajectory'] = data.apply(calculate_ball_trajectory, axis=1)
data['Home Run Favorability'] = data.apply(is_home_run_pitch, axis=1)

scaler = MinMaxScaler()
data[['Exit Velocity', 'Hit Distance', 'Launch Angle', 'Spray Angle', 'Ball Trajectory']] = scaler.fit_transform(data[['Exit Velocity', 'Hit Distance', 'Launch Angle', 'Spray Angle', 'Ball Trajectory']])

data.to_csv("processed_dataset_with_features.csv", index=False)

print("Processed dataset saved as 'processed_dataset_with_features.csv'")
