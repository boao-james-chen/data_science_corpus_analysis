import os
import json
import csv
from dateutil import parser
from datetime import datetime, timedelta
import pytz
import re

DOWNLOAD_PATH = "/Users/cba/Desktop/github_datascience_code/download_code/sklearn_function_sequence_usage.csv"

def find_timestamp_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("_timestamps.json"):
                yield os.path.join(root, file)

#last year 
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
            continue
    return False

#track sklearn
def identify_sklearn_functions(directory):

    sklearn_sequences = {}
    function_pattern = re.compile(r"from sklearn\..+ import .+|import sklearn\..+")
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.py'):
                with open(file_path, 'r', errors='ignore') as f:
                    sequence = []
                    for line_number, line in enumerate(f, 1):
                        match = function_pattern.search(line)
                        if match:
                            clean_line = match.group().replace("import", ",").split(",")
                            module_or_function = clean_line[-1].strip()
                            sequence.append((line_number, module_or_function))
                    if sequence:
                        sklearn_sequences[file_path] = sequence
    return sklearn_sequences

def export_sklearn_function_usage_to_csv(sklearn_sequences, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File Path', 'Line Number', 'Import Statement'])  
        for file_path, sequences in sklearn_sequences.items():
            for line_number, import_statement in sequences:
                writer.writerow([file_path, line_number, import_statement])

if __name__ == "__main__":
    if has_recent_commits(DOWNLOAD_PATH):
        sklearn_sequences = identify_sklearn_functions(DOWNLOAD_PATH)
        if sklearn_sequences:
            output_csv_path = os.path.join(DOWNLOAD_PATH, 'sklearn_function_sequence_usage.csv')
            export_sklearn_function_usage_to_csv(sklearn_sequences, output_csv_path)
            print(f"Scikit-learn sequence data exported to {output_csv_path}.")
        else:
            print("scikit-learn sequence data not found.")
    else:
        print("No recent commits found.")
