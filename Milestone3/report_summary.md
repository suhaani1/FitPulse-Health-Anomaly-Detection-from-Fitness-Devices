# Milestone 3: Anomaly Detection and Visualization

## Objective
The objective of Milestone 3 is to identify, label, and visualize health-related anomalies from fitness device data. This milestone focuses on detecting abnormal patterns in heart rate and sleep behavior using predictive modeling, statistical thresholds, and clustering techniques. The aim is to highlight deviations from normal physiological behavior that may indicate potential health risks.

---

## Steps Followed

### 1. Residual Analysis using Prophet
- Time-series forecasting models were built using Facebook Prophet for heart rate data.
- Predicted values were compared with actual observations.
- Residuals (actual − predicted) were calculated.
- Data points with residuals exceeding a statistical threshold (±2 standard deviations) were flagged as anomalies.

### 2. Threshold-Based Anomaly Detection
- Domain-specific thresholds were applied based on physiological norms:
  - Resting heart rate below 40 BPM or above 110 BPM.
  - Sleep duration below 4 hours or above 10 hours.
- Observations violating these thresholds were labeled as abnormal.

### 3. Cluster-Based Anomaly Detection
- Behavioral features (heart rate, daily steps, sleep hours) were standardized.
- KMeans clustering was applied to group similar behavioral patterns.
- The smallest cluster, representing rare behavior patterns, was identified as anomalous.

### 4. Anomaly Labeling
- Anomalies detected from residual analysis, threshold violations, and cluster-based methods were combined.
- A final anomaly label was assigned to clearly distinguish normal and abnormal observations.

### 5. Visualization of Anomalies
- Time-series plots were created for heart rate and sleep data.
- Anomalous points were highlighted using distinct colors.
- Visualizations were saved as image files for documentation and reporting.

---

## Tools Used
- Python (Pandas, NumPy)
- Facebook Prophet
- Scikit-learn (KMeans, StandardScaler)
- Matplotlib
- Google Colaboratory

---

## Key Insights and Visualizations
- Heart rate anomalies revealed sudden spikes and drops that deviated significantly from predicted trends.
- Sleep pattern visualization highlighted periods of insufficient and excessive sleep.
- Combining multiple anomaly detection techniques improved reliability and interpretability.
- Visual inspection of anomalies provided intuitive understanding of abnormal health behavior.

---


---

## Conclusion
Milestone 3 successfully demonstrated how predictive modeling, statistical rules, and unsupervised learning can be integrated to detect and visualize health anomalies from fitness device data. These results form a strong foundation for future milestones involving health risk scoring and alert systems.
