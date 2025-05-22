import pandas as pd

file1 = './data/scraped_beach_data_details.csv'
file2 = './data/snirh_praias_infopraia_vwm.csv'

# Load the CSV files
try:
    df1 = pd.read_csv(file1, dtype={'id': int}, encoding='utf-8')
    df2 = pd.read_csv(file2, dtype={'id': int}, encoding='utf-8')
except Exception as e:
    print(f"Error loading CSV files: {e}")
    exit()

# Verify 'id' column exists
if 'id' not in df1.columns or 'id' not in df2.columns:
    raise ValueError("One or both CSV files are missing the 'id' column.")

# Debug: Print first few rows of both DataFrames
print("First few rows of file1.csv:")
print(df1[['id']].head())
print("\nFirst few rows of file2.csv:")
print(df2[['id']].head())

# Debug: Check for matching IDs
common_ids = set(df1['id']).intersection(set(df2['id']))
print(f"\nNumber of common IDs: {len(common_ids)}")
if len(common_ids) == 0:
    print("No matching IDs found. Check for data type mismatches or incorrect ID values.")

# Merge the DataFrames
merged_df = pd.merge(df1, df2, on='id', how='inner')

# Debug: Check for NaN values in merged DataFrame
print("\nMerged DataFrame (first few rows):")
print(merged_df.head())
print("\nNaN counts in merged DataFrame:")
print(merged_df.isna().sum())

# Save the merged DataFrame (optional)
merged_df.to_csv('./data/merged_output.csv', index=False)





