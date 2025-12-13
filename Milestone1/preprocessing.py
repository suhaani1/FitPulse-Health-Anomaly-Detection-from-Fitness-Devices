# # preprocessing.py
# import pandas as pd
# import numpy as np
# import pytz
# from dateutil import parser
# from typing import Optional, Tuple

# COMMON_TS_COLS = ['timestamp', 'time', 'datetime', 'date', 'ts']

# def _find_timestamp_column(df: pd.DataFrame) -> Optional[str]:
#     # Heuristic: exact name, then dtype datetime-like, then contains 'time' or 'date'
#     for c in df.columns:
#         if c.lower() in COMMON_TS_COLS:
#             return c
#     for c in df.columns:
#         if np.issubdtype(df[c].dtype, np.datetime64):
#             return c
#     for c in df.columns:
#         if 'time' in c.lower() or 'date' in c.lower():
#             return c
#     return None

# def read_file(path_or_buffer) -> pd.DataFrame:
#     # Accepts a file path or file-like (from Streamlit)
#     try:
#         df = pd.read_json(path_or_buffer, convert_dates=False)
#     except Exception:
#         df = pd.read_csv(path_or_buffer)
#     return df

# def to_datetime_series(series: pd.Series) -> pd.Series:
#     # robust parse with dateutil; invalid -> NaT
#     def _try_parse(x):
#         if pd.isna(x):
#             return pd.NaT
#         if isinstance(x, (pd.Timestamp, np.datetime64)):
#             return pd.to_datetime(x, errors='coerce')
#         try:
#             return pd.to_datetime(x, utc=False, errors='coerce')
#         except Exception:
#             try:
#                 return parser.parse(str(x))
#             except Exception:
#                 return pd.NaT
#     return series.map(_try_parse)

# def normalize_timestamps(df: pd.DataFrame, ts_col: Optional[str]=None, tz_target='UTC') -> Tuple[pd.DataFrame,str]:
#     if ts_col is None:
#         ts_col = _find_timestamp_column(df)
#         if ts_col is None:
#             raise ValueError("No timestamp column found. Please include a timestamp column.")
#     ts = df[ts_col]
#     ts_parsed = to_datetime_series(ts)
#     # try infer timezone: if timezone-aware -> convert, else localize as UTC then convert
#     # First, detect if any parsed tz info exists in any non-null value
#     has_tzinfo = ts_parsed.dt.tz is not None
#     # If tz naive, assume local timezone or UTC? We'll assume UTC for safety but allow user to pass tz_target override
#     ts_parsed = pd.to_datetime(ts_parsed, utc=False, errors='coerce')
#     # If tz-naive but looks like local times, user can specify; we'll localize naive to UTC
#     if ts_parsed.dt.tz is None:
#         ts_parsed = ts_parsed.dt.tz_localize('UTC', ambiguous='NaT', nonexistent='NaT')
#     # Convert to target tz
#     ts_parsed = ts_parsed.dt.tz_convert(tz_target)
#     df = df.copy()
#     df[ts_col] = ts_parsed
#     return df, ts_col

# def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
#     # Lowercase col names and common renames
#     rename_map = {}
#     for c in df.columns:
#         cn = c.strip()
#         lc = cn.lower()
#         if lc in ['hr', 'heart_rate', 'heartrate', 'bpm']:
#             rename_map[c] = 'heart_rate'
#         elif lc in ['step', 'steps', 'step_count', 'stepcount']:
#             rename_map[c] = 'steps'
#         elif 'sleep' in lc:
#             rename_map[c] = 'sleep'
#         elif lc in ['timestamp','time','datetime','date']:
#             rename_map[c] = 'timestamp'
#     df = df.rename(columns=rename_map)
#     return df

# def fill_and_interpolate(df: pd.DataFrame, ts_col='timestamp') -> pd.DataFrame:
#     # Assumes df indexed by timestamp or has ts_col column
#     df = df.copy()
#     if ts_col not in df.columns:
#         raise ValueError("Timestamp column missing")
#     # ensure timestamp dtype
#     df[ts_col] = pd.to_datetime(df[ts_col], utc=True, errors='coerce')
#     # Drop rows with NaT timestamp
#     df = df.dropna(subset=[ts_col])
#     df = df.sort_values(ts_col)
#     df = df.set_index(ts_col)
#     # Common strategies:
#     # - heart_rate: interpolate (linear), then forward/backfill
#     if 'heart_rate' in df.columns:
#         df['heart_rate'] = pd.to_numeric(df['heart_rate'], errors='coerce')
#         df['heart_rate'] = df['heart_rate'].interpolate(method='time', limit=10)
#         df['heart_rate'] = df['heart_rate'].fillna(method='ffill').fillna(method='bfill')
#     # - steps: replace NaN with 0
#     if 'steps' in df.columns:
#         df['steps'] = pd.to_numeric(df['steps'], errors='coerce').fillna(0)
#     # - sleep: keep blocks; fill forward small gaps
#     if 'sleep' in df.columns:
#         df['sleep'] = df['sleep'].fillna(method='ffill').fillna(method='bfill')
#     return df

# def resample_df(df: pd.DataFrame, freq='1T') -> pd.DataFrame:
#     # df must have datetime index (tz-aware)
#     if not isinstance(df.index, pd.DatetimeIndex):
#         raise ValueError("Dataframe must be indexed by datetime index before resampling.")
#     # Handle each column by aggregation
#     agg = {}
#     if 'heart_rate' in df.columns:
#         agg['heart_rate'] = 'mean'
#     if 'steps' in df.columns:
#         # When resampling to 1-min, sum the steps
#         agg['steps'] = 'sum'
#     # for any non-numeric columns use last
#     for c in df.columns:
#         if c not in agg:
#             agg[c] = 'last'
#     df_resampled = df.resample(freq).agg(agg)
#     # After resample, re-apply interpolation for numeric columns to fill small gaps
#     if 'heart_rate' in df_resampled.columns:
#         df_resampled['heart_rate'] = df_resampled['heart_rate'].interpolate(method='time', limit=5)
#     df_resampled = df_resampled.fillna(method='ffill').fillna(method='bfill')
#     return df_resampled

# def preprocess_pipeline(df: pd.DataFrame, ts_col: Optional[str]=None, freq='1T', tz_target='UTC') -> pd.DataFrame:
#     df = standardize_columns(df)
#     df, ts_col = normalize_timestamps(df, ts_col=ts_col, tz_target=tz_target)
#     df = fill_and_interpolate(df, ts_col=ts_col)
#     df_resampled = resample_df(df, freq=freq)
#     return df_resampled

# def save_clean_csv(df: pd.DataFrame, out_path: str):
#     # Save timezone-aware index as ISO strings
#     df_copy = df.copy()
#     df_copy.index = df_copy.index.map(lambda x: x.isoformat() if hasattr(x, 'isoformat') else str(x))
#     df_copy.to_csv(out_path)



import pandas as pd
import os

print("\n===== FitPulse | Milestone 1: Data Preprocessing =====\n")

# -----------------------------------
# Utility: Read CSV or JSON
# -----------------------------------
def read_file(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found")

    if filename.endswith(".csv"):
        return pd.read_csv(filename)
    elif filename.endswith(".json"):
        return pd.read_json(filename)
    else:
        raise ValueError("Only CSV or JSON supported")


# -----------------------------------
# Normalize timestamps to UTC
# -----------------------------------
def normalize_timestamp(df, column):
    df[column] = pd.to_datetime(df[column], errors="coerce", utc=True)
    df = df.dropna(subset=[column])
    df = df.sort_values(column)
    return df


# -----------------------------------
# Heart Rate Processing
# -----------------------------------
def preprocess_heartrate(df):
    print("• Processing heart rate data...")
    df = normalize_timestamp(df, "Time")
    df.rename(columns={"Time": "datetime", "Value": "heart_rate"}, inplace=True)
    df.set_index("datetime", inplace=True)

    df = df.resample("1T").mean()
    df["heart_rate"] = df["heart_rate"].interpolate()

    return df.reset_index()


# -----------------------------------
# Steps Processing
# -----------------------------------
def preprocess_steps(df):
    print("• Processing steps data...")
    df = normalize_timestamp(df, "ActivityHour")
    df.rename(columns={"ActivityHour": "datetime"}, inplace=True)
    df.set_index("datetime", inplace=True)

    df = df.resample("1T").ffill()
    df["steps_per_min"] = df["StepTotal"] / 60

    return df[["steps_per_min"]].reset_index()


# -----------------------------------
# Sleep Processing
# -----------------------------------
def preprocess_sleep(df):
    print("• Processing sleep data...")
    df = normalize_timestamp(df, "date")
    df.rename(columns={"date": "datetime"}, inplace=True)
    df.set_index("datetime", inplace=True)

    df = df.resample("1T").max()
    df = df.fillna(0)

    return df.reset_index()


# -----------------------------------
# Main Execution
# -----------------------------------
def main():
    # Load files
    hr = read_file("heartrate.csv")
    steps = read_file("steps.csv")
    sleep = read_file("sleep.csv")

    print("✔ Files loaded successfully")

    # Preprocess
    hr_clean = preprocess_heartrate(hr)
    steps_clean = preprocess_steps(steps)
    sleep_clean = preprocess_sleep(sleep)

    print("✔ Timestamps normalized to UTC")
    print("✔ Missing values handled")
    print("✔ Data aligned to 1-minute frequency")

    # Merge all
    final_df = hr_clean.merge(steps_clean, on="datetime", how="left")
    final_df = final_df.merge(sleep_clean, on="datetime", how="left")
    final_df.fillna(0, inplace=True)

    # Save output
    final_df.to_csv("final_1min_dataset.csv", index=False)

    print("\n===== OUTPUT =====")
    print("✔ Cleaned dataset saved as final_1min_dataset.csv")
    print("✔ Rows:", len(final_df))
    print("✔ Columns:", list(final_df.columns))
    print("\n===== PREPROCESSING COMPLETED SUCCESSFULLY =====\n")


if __name__ == "__main__":
    main()
