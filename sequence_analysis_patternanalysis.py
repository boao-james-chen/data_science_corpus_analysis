#!/usr/bin/env python3

import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt

CSV_PATH = "/Users/cba/Desktop/github_datascience_code/download_code/sklearn_function_calls_usageCOUNT.csv"
OUTPUT_FILE = "/Users/cba/Desktop/github_datascience_code/sequence_analysis_results_cleaned.txt"

SKLEARN_CLASSES = {
    r"\bStandardScaler\b": "Scaling",
    r"\bMinMaxScaler\b": "Scaling",
    r"\bRobustScaler\b": "Scaling",
    r"\bSimpleImputer\b": "Missing Value Imputation",
    r"\bKNNImputer\b": "Missing Value Imputation",
    r"\bPCA\b": "Dimensionality Reduction",
    r"\bTruncatedSVD\b": "Dimensionality Reduction",
    r"\bSelectKBest\b": "Feature Selection",
    r"\bSelectFromModel\b": "Feature Selection",
    r"\bPolynomialFeatures\b": "Feature Engineering",
    r"\bColumnTransformer\b": "Data Transformation Pipeline",
    r"\bPipeline\b": "Pipeline/Workflow",
    r"\bGridSearchCV\b": "Hyperparameter Tuning",
    r"\bRandomizedSearchCV\b": "Hyperparameter Tuning",
    r"\bLogisticRegression\b": "Linear Classifier Training",
    r"\bRidgeClassifier\b": "Linear Classifier Training",
    r"\bSGDClassifier\b": "Linear Classifier Training",
    r"\bSVC\b": "SVM Classifier Training",
    r"\bLinearSVC\b": "SVM Classifier Training",
    r"\bRandomForestClassifier\b": "Tree-Based Model Training",
    r"\bDecisionTreeClassifier\b": "Tree-Based Model Training",
    r"\bGradientBoostingClassifier\b": "Tree-Based Model Training",
    r"\bExtraTreesClassifier\b": "Tree-Based Model Training",
    r"\bLinearRegression\b": "Linear Regression",
    r"\bRidge\b": "Regularized Linear Regression",
    r"\bLasso\b": "Regularized Linear Regression",
    r"\bElasticNet\b": "Regularized Linear Regression",
    r"\bRandomForestRegressor\b": "Tree-Based Model Training (Regressor)",
    r"\bDecisionTreeRegressor\b": "Tree-Based Model Training (Regressor)",
    r"\bGradientBoostingRegressor\b": "Tree-Based Model Training (Regressor)",
    r"\bExtraTreesRegressor\b": "Tree-Based Model Training (Regressor)",
    r"\bKMeans\b": "Clustering",
    r"\bDBSCAN\b": "Clustering",
    r"\bAgglomerativeClustering\b": "Clustering"
}

SKLEARN_METHODS = {
    r"\.fit_transform\s*\(": "fit_transform",
    r"\.fit_predict\s*\(": "fit_predict",
    r"\.fit_resample\s*\(": "fit_resample",
    r"\.fit\s*\(": "fit",
    r"\.partial_fit\s*\(": "partial_fit",
    r"\.transform\s*\(": "transform",
    r"\.predict_proba\s*\(": "predict_proba",
    r"\.predict\s*\(": "predict",
    r"\.score\s*\(": "score",
    r"\.decision_function\s*\(": "decision_function",
    r"\.inverse_transform\s*\(": "inverse_transform",
    r"\bcross_val_score\s*\(": "Cross Validation (cross_val_score)",
    r"\bcross_val_predict\s*\(": "Cross Validation (cross_val_predict)",
    r"\btrain_test_split\s*\(": "Data Splitting (train_test_split)",
    r"\.set_params\s*\(": "set_params",
    r"\.get_params\s*\(": "get_params",
    r"\.named_steps\s*\[": "Pipeline Step Access"
}

df = pd.read_csv(CSV_PATH)

def detect_classes(line):
    return [label for pattern, label in SKLEARN_CLASSES.items() if re.search(pattern, line)]

def detect_methods(line):
    return [label for pattern, label in SKLEARN_METHODS.items() if re.search(pattern, line)]

def categorize(line):
    c = detect_classes(line)
    m = detect_methods(line)

    if c and m:
        return "; ".join(f"{x} + {y}" for x in c for y in m)
    if c:
        return "; ".join(f"{x} + Class Declaration" for x in c)
    if m:
        out = []
        for x in m:
            if x == "fit":
                out.append("General Model Training (.fit())")
            elif x == "partial_fit":
                out.append("Partial Training (.partial_fit())")
            elif x == "predict":
                out.append("Prediction (.predict())")
            elif x == "predict_proba":
                out.append("Prediction Probability (.predict_proba())")
            elif x == "fit_transform":
                out.append("General Transformation (.fit_transform())")
            elif x == "transform":
                out.append("Data Transformation (.transform())")
            elif x == "fit_predict":
                out.append("General Transformation (.fit_predict())")
            elif x == "fit_resample":
                out.append("Resampling (.fit_resample())")
            elif x == "score":
                out.append("Model Scoring (.score())")
            elif x == "decision_function":
                out.append("Decision Function (.decision_function())")
            elif x == "inverse_transform":
                out.append("Inverse Transform (.inverse_transform())")
            elif x.startswith("Cross Validation") or x.startswith("Data Splitting"):
                out.append(x)
            elif x in ["set_params", "get_params", "Pipeline Step Access"]:
                out.append(f"Pipeline/Model Utility ({x})")
            else:
                out.append(f"General {x}")
        return "; ".join(out)
    return "Other"

df["Category"] = df["Function Call"].apply(categorize)
df = df[df["Category"] != "Other"].copy()
df.sort_values(by=["File Path", "Line Number"], inplace=True)

def drop_dupes(seq):
    result = [seq[0]] if seq else []
    for i in range(1, len(seq)):
        if seq[i] != seq[i - 1]:
            result.append(seq[i])
    return result

def all_ngrams(seq):
    ngrams = []
    for n in range(2, len(seq) + 1):
        for i in range(len(seq) - n + 1):
            ngrams.append(tuple(seq[i:i + n]))
    return ngrams

counter = Counter()

for path, group in df.groupby("File Path"):
    cats = list(group["Category"])
    cleaned = drop_dupes(cats)
    for ngram in all_ngrams(cleaned):
        counter[ngram] += 1

top_20 = counter.most_common(20)
for seq, count in top_20:
    print(f"{' -> '.join(seq)}: {count} times")

with open(OUTPUT_FILE, "w") as f:
    f.write("Most Common Sequences:\n")
    for seq, count in top_20:
        f.write(f"{' -> '.join(seq)}: {count} times\n")

top_10 = counter.most_common(10)
if top_10:
    labels = [" -> ".join(x) for x, _ in top_10]
    counts = [y for _, y in top_10]

    plt.figure(figsize=(12, 8))
    plt.barh(labels, counts)
    plt.xlabel("Frequency")
    plt.ylabel("Scikit-learn Sequences")
    plt.title("Top 10 Most Common Scikit-learn Sequences (Per File)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
else:
    print("No sequences found to plot.")
