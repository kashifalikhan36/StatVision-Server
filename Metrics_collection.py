import pandas as pd
import time
from mlb import MLBStata
from data_extractor import Data

# Fetch the data
data_mlb = Data()
data, data1, data2 = data_mlb.call_data()
initial_data = [data, data1, data2]

collected_data = []

counter = 0

for df in initial_data:
    if not df.empty:  
        for index, row in df.iterrows():
            if counter >= 200:
                break
            mlbstuff = MLBStata(row.get("video", None))
            try:
                data_json = mlbstuff.generate()
            except:
                time.sleep(120)
                data_json = mlbstuff.generate()

            for metric in data_json["metrics"]:
                timestamp = metric['timestamp']
                exit_velocity = metric["metrics"].get("Exit Velocity", None)
                hit_distance = metric["metrics"].get("Hit Distance", None)
                launch_angle = metric["metrics"].get("Launch Angle", None)
                spray_angle = metric["metrics"].get("Spray Angle", None)
                pitch_type = metric["metrics"].get("Pitch Type", None)

                # Save only the metrics with valid values (remove 0 or None values)
                if exit_velocity and hit_distance and launch_angle and spray_angle and pitch_type:
                    collected_data.append({
                        "Timestamp": timestamp,
                        "Exit Velocity": exit_velocity,
                        "Hit Distance": hit_distance,
                        "Launch Angle": launch_angle,
                        "Spray Angle": spray_angle,
                        "Pitch Type": pitch_type
                    })
                    counter += 1
                if counter >= 200:
                    break
        if counter >= 200:
            break

# Convert collected data to a DataFrame
df_metrics = pd.DataFrame(collected_data)

# Save to a CSV file
df_metrics.to_csv("collected_metrics_train.csv", index=False)

print("Data collection complete. Saved to 'collected_metrics_train.csv'.")