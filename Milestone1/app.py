# # streamlit_app.py
# import streamlit as st
# import pandas as pd
# from preprocessing import read_file, preprocess_pipeline, save_clean_csv
# import io
# import os
# from datetime import datetime

# st.set_page_config(page_title="FitPulse - Milestone 1", layout="wide")
# st.title("FitPulse — Milestone 1: Upload & Preprocess Fitness Data")

# st.markdown("Upload CSV or JSON exported from a fitness watch (heart rate, steps, sleep).")

# uploaded = st.file_uploader("Upload CSV/JSON", type=["csv","json"], accept_multiple_files=False)

# col1, col2 = st.columns(2)

# if uploaded is not None:
#     try:
#         df_raw = read_file(uploaded)
#     except Exception as e:
#         st.error(f"Failed to read file: {e}")
#         st.stop()

#     with col1:
#         st.subheader("Raw data preview (first 10 rows)")
#         st.dataframe(df_raw.head(10), height=300)

#     st.sidebar.header("Preprocessing options")
#     freq = st.sidebar.selectbox("Resample frequency", options=["1T", "5T", "1H"], index=0, help="1T = 1 minute")
#     tz_target = st.sidebar.text_input("Target timezone (pytz name)", value="UTC")
#     ts_col = st.sidebar.text_input("Timestamp column (leave blank to auto-detect)", value="")

#     if st.button("Run preprocessing"):
#         with st.spinner("Preprocessing..."):
#             try:
#                 ts_col_arg = ts_col.strip() if ts_col.strip() else None
#                 df_clean = preprocess_pipeline(df_raw, ts_col=ts_col_arg, freq=freq, tz_target=tz_target)
#             except Exception as e:
#                 st.error(f"Preprocessing failed: {e}")
#                 st.stop()

#         with col2:
#             st.subheader("Cleaned & Resampled preview (first 20 rows)")
#             st.dataframe(df_clean.head(20), height=400)

#         # Save to csv in-memory and provide download
#         csv_buffer = io.StringIO()
#         df_for_save = df_clean.copy()
#         df_for_save.index = df_for_save.index.tz_convert('UTC').map(lambda x: x.isoformat())
#         df_for_save.to_csv(csv_buffer)
#         csv_bytes = csv_buffer.getvalue().encode()

#         st.download_button("Download cleaned CSV", data=csv_bytes,
#                            file_name=f"cleaned_fitpulse_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv",
#                            mime="text/csv")
#         st.success("Preprocessing complete. Download the cleaned CSV or inspect the preview above.")

# else:
#     st.info("Upload a CSV or JSON file to begin. Use the test data generator if you don't have a file.")
#     if st.button("Generate sample test data (5 minutes)"):
#         import test_data
#         buf = test_data.generate_sample_csv()
#         st.download_button("Download sample dataset", data=buf.getvalue().encode(), file_name="sample_fitpulse.csv", mime="text/csv")



import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="FitPulse | Milestone 1",
    layout="centered"
)

st.title(" FitPulse Health Anomaly Detection from Fitness Devices")
st.markdown("### Milestone 1")

st.markdown("""
**Objectives**
- Ingest fitness data (CSV / JSON)
- Normalize timestamps to UTC
- Handle missing / null values
- Align data to 1-minute granularity
""")

# ---------------------------
# File Upload UI
# ---------------------------
uploaded_file = st.file_uploader(
    "Upload Fitness Dataset (CSV / JSON)",
    type=["csv", "json"]
)

log_messages = []

if uploaded_file:
    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_json(uploaded_file)

    log_messages.append("✔ File uploaded successfully")

    st.subheader("📄 Raw Dataset Preview")
    st.dataframe(df.head(20))

    if st.button("🚀 Run Preprocessing"):
        with st.spinner("Preprocessing data..."):

            # ---------------------------
            # Detect datetime column
            # ---------------------------
            datetime_col = None
            for col in df.columns:
                if "time" in col.lower() or "date" in col.lower():
                    datetime_col = col
                    break

            if not datetime_col:
                st.error("No datetime column found in dataset")
                st.stop()

            log_messages.append(f"✔ Detected datetime column: {datetime_col}")

            # ---------------------------
            # Normalize timestamp to UTC
            # ---------------------------
            df[datetime_col] = pd.to_datetime(
                df[datetime_col],
                errors="coerce",
                utc=True
            )

            df = df.dropna(subset=[datetime_col])
            df = df.sort_values(datetime_col)

            log_messages.append("✔ Timestamps normalized to UTC")

            # ---------------------------
            # Align to 1-minute frequency
            # ---------------------------
            df.set_index(datetime_col, inplace=True)
            df = df.resample("1T").mean()

            log_messages.append("✔ Data aligned to 1-minute frequency")

            # ---------------------------
            # Handle missing values
            # ---------------------------
            numeric_cols = df.select_dtypes(include="number").columns
            df[numeric_cols] = df[numeric_cols].interpolate()
            df[numeric_cols] = df[numeric_cols].fillna(0)

            log_messages.append("✔ Missing / null values handled")

            # Reset index
            df.reset_index(inplace=True)

        # ---------------------------
        # Cleaned Dataset Preview
        # ---------------------------
        st.subheader("📊 Cleaned Dataset Preview")
        st.dataframe(df.head(50))

        # ---------------------------
        # Time-Normalized Data Log
        # ---------------------------
        st.subheader("🕒 Time-Normalized Data Log")
        for msg in log_messages:
            st.success(msg)

        # ---------------------------
        # Download Button
        # ---------------------------
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Download Cleaned Dataset",
            data=csv,
            file_name="final_1min_dataset_cleaned.csv",
            mime="text/csv"
        )

else:
    st.info("Please upload a fitness dataset to begin preprocessing.")

