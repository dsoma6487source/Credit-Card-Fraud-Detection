
import pandas as pd

data = pd.read_csv("dataset/creditcard.csv")

print("Dataset Loaded Successfully!")

print("\nFirst 5 Transactions:")
print(data.head())

print("\nDataset Shape:")
print(data.shape)

print("\nFraud Distribution:")
print(data["Class"].value_counts())
