# Milestone 3: Anomaly Detection and Visualization

## Objective
The objective of Milestone 3 is to detect, label, and visualize anomalies in fitness device data using time-series forecasting, statistical thresholds, and clustering techniques. This milestone builds upon the modeling and feature extraction performed in Milestone 2 and focuses on identifying abnormal health patterns in resting heart rate and sleep behavior.

---

## Dataset Description
The dataset was manually uploaded in Google Colaboratory and contains time-series fitness data, including:
- Datetime
- Resting heart rate
- Daily steps
- Hours of sleep

The datetime column was converted into a timezone-free format to ensure compatibility with time-series models.

---

## Steps Followed

### 1. Data Preparation
- The dataset was uploaded manually using Google Colab file upload.
- The datetime column was parsed using mixed date formats and cleaned by removing timezone information.
- Data was sorted chronologically to maintain proper time-series order.

### 2. Residual Analysis using Prophet
- A Facebook Prophet model was trained on resting heart rate data.
- The model generated predicted values for the observed time period.
- Residuals were calculated as the difference between actual and predicted heart rate values.
- Anomalies were detected where residuals exceeded ±2 standard deviations from the mean.

### 3. Threshold-Based Anomaly Detection
Domain-specific rules were applied:
- Resting heart rate below 40 BPM or above 110 BPM was marked as abnormal.
- Sleep duration below 4 hours or above 10 hours was considered anomalous.
These rules helped identify physiologically unrealistic or risky values.

### 4. Cluster-Based Anomaly Detection
- Resting heart rate, daily steps, and sleep hours were standardized.
- KMeans clustering was applied to group similar behavioral patterns.
- The smallest cluster, representing rare behavior patterns, was labeled as anomalous.

### 5. Anomaly Labeling
- Results from residual analysis, threshold-based detection, and clustering were combined.
- A final anomaly label was assigned to each observation to clearly distinguish normal and abnormal data points.

### 6. Visualization of Anomalies
- Time-series plots were generated using Matplotlib.
- Heart rate anomalies were highlighted with red markers.
- Sleep pattern anomalies were visualized to show abnormal sleep segments.
- All plots were saved in the `visualizations/` directory for documentation.

---

## Tools Used
- Python (Pandas, NumPy)
- Facebook Prophet
- Scikit-learn (KMeans, StandardScaler)
- Matplotlib
- Google Colaboratory

---

## Key Insights and Visualizations
- Prophet residual analysis effectively identified sudden deviations in heart rate trends.
- Threshold-based rules captured extreme physiological values that may indicate health risks.
- Cluster-based detection highlighted rare behavioral patterns not visible through simple thresholds.
- Visualizations provided intuitive confirmation of detected anomalies.

---

---

## Conclusion
Milestone 3 successfully demonstrates a multi-method approach to anomaly detection in fitness data. By combining predictive modeling, rule-based thresholds, and unsupervised learning, the system provides a reliable and interpretable framework for identifying abnormal health behavior. These results establish a strong foundation for future milestones involving health risk scoring and alert generation.
