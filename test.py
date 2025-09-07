import pandas as pd

# Load Excel file
file_path = "The_project/SPORTS.xlsx"
df = pd.read_excel(file_path)

# Shuffle the DataFrame rows
shuffled_df = df.sample(frac=1).reset_index(drop=True)

# Get 10 random rows
sample_10 = shuffled_df.head(1)

print(sample_10)
