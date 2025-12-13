# FitPulse-Health-Anomaly-Detection-from-Fitness-Devices
## Milestone 1: Data collection and preprocessing

## project Overview
This project focuses on building a robust data preprocessing pipeline of a fitness tracker data.
the goal of this is to ingest raw fitness data,clean and normalize timestamps, handle missing values and align all health metrics to consistent time frequency for future analysis and anomaly detection.

### Datset:
The dataset is taken fron kaggle: https://www.kaggle.com/datasets/jahanzaibqamar/fitbit-fitness-tracker-data
that inlcude heartrate, steps and sleep.
These datasets are merged together and aligned on a common timeline and sampled at 1-minute intervals.

### Technologies used
1. python
2. streamlit for file upload UI
3. pandas for data processing and resampling

### how to run
`bash`
 streamlit run app.py
 ### upload dataset:
 upload fitness data file in csv or json
   
### Output

Cleaned Dataset Preview (displayed in the app)

Time-normalized processing log

Downloadable CSV file (cleaned_data.csv)
   
