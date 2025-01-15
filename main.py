from mlb import MLBStata
from data_extractor import Data

# Fetch the data
data_mlb = Data()
data, data1, data2 = data_mlb.call_data()
initial_data = [data, data1, data2]

for df in initial_data:
    if not df.empty:  
        for index, row in df.iterrows():
            launch_angle = row.get("LaunchAngle", None)
            exit_velocity = row.get("ExitVelocity", None)
            hit_distance = row.get("HitDistance", None)
            mlbstuff = MLBStata(row.get("video", None), row.get("title", None))
            data_json = mlbstuff.generate()
            for metric in data_json["metrics"]:
                print(f"Timestamp: {metric['timestamp']}")
                for key, value in metric["metrics"].items():
                    print(f"  {key}: {value}")
            print(f" and real one (LaunchAngle={launch_angle}, ExitVelocity={exit_velocity}, HitDistance={hit_distance})")
            break
    break