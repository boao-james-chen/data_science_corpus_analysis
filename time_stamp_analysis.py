import os
import json
from collections import Counter
from dateutil import parser
import matplotlib.pyplot as plt

import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
DOWNLOAD_PATH = "/Users/cba/Desktop/github_datascience_code/download_code"

def find_timestamp_files(directory):
    """Recursively finds all timestamp JSON files in the given directory."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("_timestamps.json"):
                yield os.path.join(root, file)

def load_all_commit_timestamps(download_path):
    all_timestamps = []
    for json_file_path in find_timestamp_files(download_path):
        try:
            with open(json_file_path, 'r') as file:
                timestamps = json.load(file)
                all_timestamps.extend(timestamps)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {json_file_path}: {e}")
        except Exception as e:
            print(f"Unexpected error loading {json_file_path}: {e}")
    
    if not all_timestamps:
        print("No timestamps were loaded. Please check your repository directories and JSON files.")
    return all_timestamps

def parse_timestamps_to_monthly_counts(timestamps):
    dates = [parser.parse(commit['date']) for commit in timestamps]
    year_month = [date.strftime('%Y-%m') for date in dates]
    monthly_counts = Counter(year_month)
    return monthly_counts

def plot_commit_activity(monthly_counts):
    if not monthly_counts:
        print("No commit data available to plot.")
        return
    sorted_months = sorted(monthly_counts.items())
    months, counts = zip(*sorted_months) if sorted_months else ([], [])
    
    plt.figure(figsize=(15, 7))
    if months:
        plt.plot(months, counts, marker='o')
        plt.xticks(rotation=90)
        plt.xlabel('Month')
        plt.ylabel('Number of Commits')
        plt.title('Commit Activity Over Time Across All Repositories')
        plt.tight_layout()
        plt.show()
    else:
        print("No commit data found for plotting.")

# if we need to analyze more repo (500+) it is hard to put everything in a single graph
# def plot_commit_activity(monthly_counts):
#     if not monthly_counts:
#         print("No commit data available to plot.")
#         return
#     sorted_months = sorted(monthly_counts.items())
#     months, counts = zip(*sorted_months) if sorted_months else ([], [])
    
#     plt.figure(figsize=(15, 7))  # Adjust the figure size as necessary
#     ax = plt.gca()
    
# 
#     locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
#     formatter = mdates.ConciseDateFormatter(locator)
#     ax.xaxis.set_major_locator(locator)
#     ax.xaxis.set_major_formatter(formatter)

#     # Plot data
#     if months:
#         ax.plot(months, counts, marker='o')
        
#         # more clear?
#         plt.setp(ax.get_xticklabels(), rotation=30, ha='right')  # Rotate for readability
#         plt.xlabel('Month')
#         plt.ylabel('Number of Commits')
#         plt.title('Commit Activity Over Time Across All Repositories')
        
#         # Avoid too many number of label on x -axis to (hard to see)
#         ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=20))
#         plt.tight_layout()
#         plt.show()
#     else:
#         print("No commit data found for plotting.")


if __name__ == "__main__":
    all_timestamps = load_all_commit_timestamps(DOWNLOAD_PATH)
    if all_timestamps:
        monthly_commit_counts = parse_timestamps_to_monthly_counts(all_timestamps)
        plot_commit_activity(monthly_commit_counts)
    else:
        print("Analysis aborted due to lack of data.")
