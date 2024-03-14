import requests
import os

#change to your github personal token
GITHUB_TOKEN = ""
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
#change to your local/server path
DOWNLOAD_PATH = "/Users/cba/Desktop/github_datascience_code/download_code"

# Define size range in KB
SIZE_MIN_KB = 0
SIZE_MAX_KB = 204800  

def check_rate_limit():
    rate_limit_url = "https://api.github.com/rate_limit"
    response = requests.get(rate_limit_url, headers=HEADERS)
    if response.status_code == 200:
        rate_limit_data = response.json()
        print(f"Rate Limit: {rate_limit_data['resources']['core']['remaining']} of {rate_limit_data['resources']['core']['limit']}")
        return rate_limit_data['resources']['core']['remaining']
    else:
        print(f"Failed to retrieve rate limit. Status Code: {response.status_code}, Response: {response.text}")
        return -1

def search_and_clone_repositories(topic, stars_min, stars_max, language="python", size_min_kb=SIZE_MIN_KB, size_max_kb=SIZE_MAX_KB):
    page = 1
    while page <= 10:  # GitHub API allows up to 10 pages for a search query.
        if check_rate_limit() > 0:
            query = f"{topic} language:{language} stars:{stars_min}..{stars_max} fork:false"
            search_url = "https://api.github.com/search/repositories"
            params = {"q": query, "sort": "stars", "order": "desc", "per_page": 100, "page": page}
            response = requests.get(search_url, headers=HEADERS, params=params)
            if response.status_code == 200 and response.json()["items"]:
                repos = response.json()["items"]
                for repo in repos:
                    if size_min_kb <= repo['size'] <= size_max_kb:
                        repo_name = repo["full_name"].replace("/", "_")
                        clone_url = repo["clone_url"]
                        repo_download_path = os.path.join(DOWNLOAD_PATH, repo_name)
                        if not os.path.exists(repo_download_path):
                            print(f"Cloning {repo_name} into {repo_download_path}")
                            os.system(f"git clone {clone_url} '{repo_download_path}'")
                        else:
                            print(f"Repository {repo_name} already exists. Skipping.")
                    else:
                        print(f"Repository {repo_name} skipped due to size outside of range.")
                page += 1
            else:
                break  # No more items to process or error occurred
        else:
            print("Rate limit exceeded, please try again later.")
            break

if __name__ == "__main__":
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)
    #uncomment and run each one separately to avoid reaching API rate limit
    # search_and_clone_repositories("data science", 1001, 2000)
    # search_and_clone_repositories("data science", 501, 1000)
    # search_and_clone_repositories("data science", 201, 500)
    # search_and_clone_repositories("data science", 101, 200)
    # search_and_clone_repositories("data science", 51, 100)
    search_and_clone_repositories("data science", 0, 50)
