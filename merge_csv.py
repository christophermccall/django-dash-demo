import pandas as pd
import os

# setup directory paths
base_dir = "dashboard/static/data/"
raw_data_dir = os.path.join(base_dir, "raw_data")# raw_data directory
output_file = os.path.join(base_dir, "irs_nonprofits.csv")  # final output file

# make sure the raw_data directory exists
if not os.path.exists(raw_data_dir):
    print(f"{raw_data_dir} not found!")
    exit()

# get all CSV files in the raw_data directory
csv_files = [f for f in os.listdir(raw_data_dir) if f.endswith(".csv")]

if not csv_files:
    print("No CSV files found in the raw_data directory!")
    exit()

# read and merge all CSV files
df_list = [pd.read_csv(os.path.join(raw_data_dir, file)) for file in csv_files]
merged_df = pd.concat(df_list, ignore_index=True)

# save the merged DataFrame to a new CSV file
merged_df.to_csv(output_file, index=False)

print(f"file saved to {output_file}")