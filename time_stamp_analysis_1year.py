import os
import json
from collections import Counter
from dateutil import parser
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import pytz  

DOWNLOAD_PATH = "/Users/cba/Desktop/github_datascience_code/download_code"

def find_timestamp_files(directory):
    """Recursively finds all timestamp JSON files in the given directory."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("_timestamps.json"):
                yield os.path.join(root, file)

def is_scikit_learn_used(directory):
    """Check if scikit-learn is used in the repository."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file == 'requirements.txt':
                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        if 'scikit-learn' in f.read():
                            return True
                except UnicodeDecodeError:
                    continue
            elif file.endswith('.py'):
                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        for line in f:
                            if 'import sklearn' in line:
                                return True
                except UnicodeDecodeError:
                    continue
    return False

def load_all_commit_timestamps(download_path):
    all_timestamps = []
    one_year_ago = datetime.now(pytz.utc) - timedelta(days=365)
    for repo_dir in next(os.walk(download_path))[1]:  # Iterate over each repository directory
        repo_path = os.path.join(download_path, repo_dir)
        if not is_scikit_learn_used(repo_path):  # Skip repositories that don't use scikit-learn
            continue
        for json_file_path in find_timestamp_files(repo_path):  # Only check timestamp files within this repo
            if not os.path.exists(json_file_path):  # Check if the timestamp file exists
                print(f"Error with {json_file_path}: File not found.")
                continue
            try:
                with open(json_file_path, 'r') as file:
                    timestamps = json.load(file)
                    recent_timestamps = [ts for ts in timestamps if parser.parse(ts['date']) > one_year_ago]
                    all_timestamps.extend(recent_timestamps)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {json_file_path}: {e}")
            except Exception as e:
                print(f"Unexpected error loading {json_file_path}: {e}")
    
    if not all_timestamps:
        print("No recent timestamps were loaded. Please check your repository directories and JSON files.")
    return all_timestamps

def parse_timestamps_to_monthly_counts(timestamps):
    """Parse timestamps to count monthly commits."""
    dates = [parser.parse(commit['date']) for commit in timestamps]
    year_month = [date.strftime('%Y-%m') for date in dates]
    monthly_counts = Counter(year_month)
    return monthly_counts

def plot_commit_activity(monthly_counts, year):
    """Plot the commit activity given monthly commit counts and the year for the title."""
    if not monthly_counts:
        print("No commit data available to plot.")
        return
    
    sorted_months = sorted(monthly_counts.items())
    months, counts = zip(*sorted_months) if sorted_months else ([], [])
    
    plt.figure(figsize=(15, 7))
    ax = plt.gca()

    months = [datetime.strptime(month, '%Y-%m') for month in months] 
    
    ax.plot(months, counts, marker='o')
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Number of Commits')
    plt.title(f'Commit Activity Over Time in {year}')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    year = datetime.now().year  # for current year
    all_timestamps = load_all_commit_timestamps(DOWNLOAD_PATH)
    if all_timestamps:
        monthly_commit_counts = parse_timestamps_to_monthly_counts(all_timestamps)
        plot_commit_activity(monthly_commit_counts, year)
    else:
        print("Analysis aborted due to lack of data.")
