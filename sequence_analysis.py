import pandas as pd
from collections import Counter


csv_path = "/Users/cba/Desktop/github_datascience_code/download_code/sklearn_function_sequence_usage.csv"  

df = pd.read_csv(csv_path)


def categorize_function(import_statement):
    if pd.isnull(import_statement):
        return 'Other'  #  NaN values as 'Other'
    mapping = {
        'StandardScaler': 'Scaling',
        'MinMaxScaler': 'Scaling',
        'MaxAbsScaler': 'Scaling',
        'RobustScaler': 'Scaling',
        'SimpleImputer': 'Missing Value Imputation',
        'KNNImputer': 'Missing Value Imputation',
        'LogisticRegression': 'Linear Classifier',
        'SGDClassifier': 'Linear Classifier',
 
    }
    for key, value in mapping.items():
        if key in import_statement:
            return value
    return 'Other'

#  categorization 
df['Category'] = df['Import Statement'].apply(categorize_function)

df_filtered = df[df['Category'] != 'Other']

# Group by /aggregate to identify sequences
sequences_by_file = df_filtered.groupby('File Path')['Category'].agg(list)

common_sequences = Counter()
for sequence in sequences_by_file:
    for i in range(len(sequence) - 1):
        common_sequences[(sequence[i], sequence[i + 1])] += 1


print("Most Common Sequences:")
for seq, count in common_sequences.most_common():
    print(f"{seq[0]} -> {seq[1]}: {count}")
