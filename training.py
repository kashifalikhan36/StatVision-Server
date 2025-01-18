import pandas as pd
import time
from mlb import MLBStata
from data_extractor import Data
import time

# Fetch the data
data_mlb = Data()
data, data1, data2 = data_mlb.call_data()
initial_data = [data, data1, data2]

# Initialize a list to store the collected metrics
collected_data = []

# Counter to keep track of iterations
counter = 0

# Iterate through initial_data
for df in initial_data:
    if not df.empty:  
        for index, row in df.iterrows():
            # Break the loop after collecting 20 records
            if counter >= 20:
                break

            mlbstuff = MLBStata(row.get("video", None))
            try:
                # Generate data
                data_json = mlbstuff.generate()
            except:
                # Retry after a delay in case of an error
                time.sleep(120)
                data_json = mlbstuff.generate()

            # Extract metrics
            for metric in data_json["metrics"]:
                timestamp = metric['timestamp']
                exit_velocity = metric["metrics"].get("Exit Velocity", None)
                hit_distance = metric["metrics"].get("Hit Distance", None)
                launch_angle = metric["metrics"].get("Launch Angle", None)

                # Save the metrics
                collected_data.append({
                    "Timestamp": timestamp,
                    "Exit Velocity": exit_velocity,
                    "Hit Distance": hit_distance,
                    "Launch Angle": launch_angle
                })

                # Increment the counter
                counter += 1

                # Break the inner loop if 20 records are collected
                if counter >= 20:
                    break

        # Break the outer loop if 20 records are collected
        if counter >= 20:
            break

# Convert collected data to a DataFrame
df_metrics = pd.DataFrame(collected_data)

# Save to a CSV file
df_metrics.to_csv("collected_metrics.csv", index=False)

print("Data collection complete. Saved to 'collected_metrics.csv'.")
