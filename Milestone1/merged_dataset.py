# it is used to merge the three dataset that contained heartrate, sleep and step into one dataset on the basis on "Id"

import pandas as pd

# Load datasets
hr = pd.read_csv("heartrate_seconds_merged.csv")
steps = pd.read_csv("hourlySteps_merged.csv")
sleep = pd.read_csv("minuteSleep_merged.csv")

# Convert to datetime (explicit format)
hr["Time"] = pd.to_datetime(hr["Time"], format="%m/%d/%Y %I:%M:%S %p")
steps["ActivityHour"] = pd.to_datetime(steps["ActivityHour"], format="%m/%d/%Y %I:%M:%S %p")
sleep["date"] = pd.to_datetime(sleep["date"], errors="coerce")

# Rename time columns
hr.rename(columns={"Time": "datetime"}, inplace=True)
steps.rename(columns={"ActivityHour": "datetime"}, inplace=True)
sleep.rename(columns={"date": "datetime"}, inplace=True)

# Expand hourly steps to minute-level
steps = (
    steps
    .set_index("datetime")
    .groupby("Id", group_keys=False)
    .resample("1min")
    .ffill()
    .reset_index()
)

# Merge datasets
merged = hr.merge(steps, on=["Id", "datetime"], how="inner")
merged = merged.merge(sleep, on=["Id", "datetime"], how="left")

# Sort
merged = merged.sort_values(["Id", "datetime"])

# Save file
output_path = "merged_fitness_data.csv"
merged.to_csv(output_path, index=False)

print("Merged dataset saved successfully")
print(merged.head())
