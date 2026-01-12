import pandas as pd
import os
import sys

# ----------------------------
# CSV file path
# ----------------------------
csv_path = r"C:\Users\ACER\OneDrive\Desktop\telehealth_streamlit\dataset\Disease_Symptom_Associations.csv"

# ----------------------------
# Check if file exists
# ----------------------------
if not os.path.exists(csv_path):
    print(f"Error: File not found at:\n{csv_path}")
    sys.exit(1)

# ----------------------------
# Load CSV
# ----------------------------
try:
    df = pd.read_csv(csv_path)
except Exception as e:
    print(f"Error reading CSV file:\n{e}")
    sys.exit(1)

# ----------------------------
# Inspect columns
# ----------------------------
print("Columns in CSV:", list(df.columns))

# ----------------------------
# Check for disease column
# ----------------------------
if 'diseases' not in df.columns:
    print("Error: Expected 'diseases' column not found in CSV")
    sys.exit(1)

disease_col = 'diseases'

# ----------------------------
# Convert wide → long format
# ----------------------------
df_long = df.melt(id_vars=[disease_col],
                  var_name='symptom_name',
                  value_name='has_symptom')

# Keep only rows where the symptom exists (assume 1 means symptom present)
df_long = df_long[df_long['has_symptom'] == 1]

# Keep only disease_name and symptom_name
df_long = df_long[[disease_col, 'symptom_name']]

# Rename disease column
df_long = df_long.rename(columns={disease_col: 'disease_name'})

# ----------------------------
# Preview preprocessed data
# ----------------------------
print("Preview of preprocessed dataset:")
print(df_long.head())

# ----------------------------
# Save preprocessed CSV
# ----------------------------
preprocessed_path = os.path.join(os.path.dirname(csv_path), "preprocessed_dataset.csv")
df_long.to_csv(preprocessed_path, index=False)
print(f"Preprocessed dataset saved at: {preprocessed_path}")
