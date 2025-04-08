#!/bin/bash
# This script downloads the latest data from IRS website and merges the data into a single CSV file
# https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf

# Change directory to the root of the project
echo "Changing directory to the root of the project"
cd "$(dirname "$0")/../../"

# delete old raw_data
echo "Removing the old data from dashboard/static/data/raw_data"
rm -rf dashboard/static/data/raw_data/*
mkdir -p dashboard/static/data/raw_data

# Download the latest data from IRS website
echo "Downloading the latest data from IRS website"
curl -o dashboard/static/data/raw_data/region_1.csv "https://www.irs.gov/pub/irs-soi/eo1.csv"
curl -o dashboard/static/data/raw_data/region_2.csv "https://www.irs.gov/pub/irs-soi/eo2.csv"
curl -o dashboard/static/data/raw_data/region_3.csv "https://www.irs.gov/pub/irs-soi/eo3.csv"
curl -o dashboard/static/data/raw_data/region_4.csv "https://www.irs.gov/pub/irs-soi/eo4.csv"

# Run merge_csv.py to merge the data
echo "Running merge_csv.py to merge the data"
python merge_csv.py

echo "Data update complete"
