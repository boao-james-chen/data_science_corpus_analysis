import pandas as pd
from collections import Counter


# csv_path = "/Users/cba/Desktop/github_datascience_code/download_code/sklearn_function_sequence_usage.csv"  
csv_path = "/Users/cba/Desktop/github_datascience_code/download_code/sklearn_function_calls_usageCOUNT.csv"  

df = pd.read_csv(csv_path)

def categorize_function(function_call):
    # Define a detailed mapping for specific function calls
    mapping = {
        # 'StandardScaler(': 'Scaling',
        # 'MinMaxScaler(': 'Scaling',
        # 'MaxAbsScaler(': 'Scaling',
        # 'RobustScaler(': 'Scaling',
        # 'SimpleImputer(': 'Missing Value Imputation',
        # 'KNNImputer(': 'Missing Value Imputation',
        # 'LogisticRegression(': 'Linear Classifier',
        # 'SGDClassifier(': 'Linear Classifier',
        # 'RandomForestClassifier(': 'Ensemble Methods',
        # 'PCA(': 'Dimensionality Reduction',
        # 'SelectKBest(': 'Feature Selection',

        'StandardScaler.fit_transform': 'Scaling',
        'MinMaxScaler.fit_transform': 'Scaling',
        'MaxAbsScaler.fit_transform': 'Scaling',
        'RobustScaler.fit_transform': 'Scaling',
        'SimpleImputer.fit_transform': 'Missing Value Imputation',
        'KNNImputer.fit_transform': 'Missing Value Imputation',
        '.fit_transform(': 'General Transformation', 
        '.fit(': 'General Model Training',
        '.transform(': 'Data Transformation',
        '.predict(': 'Prediction',
        'PCA.fit_transform': 'Dimensionality Reduction',
        'SelectKBest.fit_transform': 'Feature Selection',
        'LogisticRegression.fit': 'Linear Classifier Training',
        'SGDClassifier.fit': 'Linear Classifier Training',
        'RandomForestClassifier.fit': 'Ensemble Methods Training',

    }
    for key, value in mapping.items():
        if key in function_call:
            return value
    return 'Other'



#  categorization 
df['Category'] = df['Function Call'].apply(categorize_function)

# Filter 
df_filtered = df[df['Category'] != 'Other']

# Aggregate sequences 
sequences_by_file = df_filtered.groupby('File Path')['Category'].agg(list)

# identify and count common sequences
common_sequences = Counter()
for sequence in sequences_by_file:

    for i in range(len(sequence) - 1):
        common_sequences[tuple(sequence[i:i+2])] += 1


print("Most Common Sequences:")
for seq, count in common_sequences.most_common():
    print(f"{' -> '.join(seq)}: {count}")
