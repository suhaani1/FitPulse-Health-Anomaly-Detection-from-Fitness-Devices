# Milestone 4 – Dashboard for Insights  
FitPulse Health Anomaly Detection from Fitness Devices

## Objective
The objective of this milestone is to develop an interactive health monitoring dashboard using **Streamlit executed in Google Colaboratory**. The dashboard enables users to upload fitness data, visualize health metrics with detected anomalies, and download anomaly summary reports.

## Execution Environment
- Google Colaboratory (.ipynb)
- Streamlit application executed inside Colab
- ngrok used to expose the Streamlit dashboard via a public URL

## Dashboard Workflow
1. The Streamlit application is launched inside Google Colab.
2. ngrok creates a public URL to access the dashboard.
3. Users upload fitness data files in CSV or JSON format.
4. The uploaded dataset is processed and the `date` column is converted to a proper timestamp.
5. Users filter data using date range selectors from the sidebar.
6. Interactive visualizations display health metrics with anomaly markers.
7. An anomaly summary report is generated and made available for download in CSV format.

## Features Implemented
- File upload support for CSV and JSON files
- Date-wise filtering of fitness data
- Metric-wise visualization using tabs:
  - Heart Rate
  - Sleep Duration
  - Step Count
- Anomaly markers displayed using red points on trend graphs
- KPI metric cards showing average values
- Downloadable anomaly summary report (CSV)

## Visualizations
The dashboard provides interactive plots for:
- Heart rate trends with detected anomalies
- Sleep duration patterns highlighting abnormal behavior
- Step count behavior with anomaly alerts

All visualizations are implemented using Plotly for interactivity.

## Tools & Libraries Used
- Python
- Streamlit
- Pandas
- Plotly Express
- Pyngrok
- Google Colaboratory

## Key Insights
- Sudden spikes and drops in heart rate are clearly visible through anomaly markers.
- Abnormal sleep duration patterns are identified across selected date ranges.
- Step count analysis highlights irregular activity behavior.

## Screenshots
The following screenshots are included in the `screenshots/` folder:
- `dashboard_ui.png` – Streamlit dashboard running via ngrok in Google Colab
- `report_download.png` – CSV anomaly report download output

## Conclusion
This milestone successfully demonstrates an end-to-end dashboard for health anomaly detection, integrating data upload, visualization, filtering, and report generation within a Google Colab environment using Streamlit and ngrok.
