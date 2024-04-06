import os
import json
import csv
from dateutil import parser
from datetime import datetime, timedelta
import pytz
import re

DOWNLOAD_PATH = "/Users/cba/Desktop/github_datascience_code/download_code"

def find_timestamp_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("_timestamps.json"):
                yield os.path.join(root, file)

def has_recent_commits(directory):
    one_year_ago = datetime.now(pytz.utc) - timedelta(days=365)
    for json_file_path in find_timestamp_files(directory):
        try:
            with open(json_file_path, 'r') as file:
                timestamps = json.load(file)
                for ts in timestamps:
                    if parser.parse(ts['date']) > one_year_ago:
                        return True
        except Exception as e:
            print(f"Error processing file {json_file_path}: {e}")
            continue
    return False

function_call_pattern = re.compile(r"(\.fit|\.transform|\.fit_transform|\.predict|\.score|\.fit_predict)\(")

def identify_sklearn_function_calls(directory):
    sklearn_function_calls = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', errors='ignore') as f:
                    sequence = []
                    for line_number, line in enumerate(f, 1):
                        match = function_call_pattern.search(line)
                        if match:
                            function_call = match.group(0)
                            sequence.append((line_number, line.strip()))
                    if sequence:
                        sklearn_function_calls[file_path] = sequence
    return sklearn_function_calls

def export_sklearn_function_usage_to_csv(sklearn_function_calls, output_path):
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File Path', 'Line Number', 'Function Call'])
        for file_path, sequences in sklearn_function_calls.items():
            for line_number, function_call in sequences:
                writer.writerow([file_path, line_number, function_call])

if __name__ == "__main__":
    if has_recent_commits(DOWNLOAD_PATH):
        sklearn_function_calls = identify_sklearn_function_calls(DOWNLOAD_PATH)
        if sklearn_function_calls:
            output_csv_path = os.path.join(DOWNLOAD_PATH, 'sklearn_function_calls_usageCOUNT.csv')
            export_sklearn_function_usage_to_csv(sklearn_function_calls, output_csv_path)
            print(f"Scikit-learn function calls data exported to {output_csv_path}.")
        else:
            print("Scikit-learn function calls data not found.")
    else:
        print("No recent commits found.")
