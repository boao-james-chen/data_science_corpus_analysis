#!/bin/bash

REPO_PATH="/Users/cba/Desktop/github_datascience_code/download_code"

# size range
declare -a size_ranges=("0-10240" "10241-20480" "20481-30720" "30721-40960" "40961-51200" "51201-102400" "102401-153600" "153601-204800")
declare -a size_count=(0 0 0 0 0 0 0 0)


categorize_size() {
    local size=$1
    if [ "$size" -le 10240 ]; then
        ((size_count[0]++))
    elif [ "$size" -le 20480 ]; then
        ((size_count[1]++))
    elif [ "$size" -le 30720 ]; then
        ((size_count[2]++))
    elif [ "$size" -le 40960 ]; then
        ((size_count[3]++))
    elif [ "$size" -le 51200 ]; then
        ((size_count[4]++))
    elif [ "$size" -le 102400 ]; then
        ((size_count[5]++))
    elif [ "$size" -le 153600 ]; then
        ((size_count[6]++))
    else
        ((size_count[7]++))
    fi
}

# for all repo
for repo in "$REPO_PATH"/*; do
    if [ -d "$repo" ]; then
        size=$(du -sk "$repo" | cut -f1)
        categorize_size $size
    fi
done


echo "Size Distribution of Repositories (in KB):"
for i in "${!size_ranges[@]}"; do
    echo "${size_ranges[$i]} KB: ${size_count[$i]}"
done
