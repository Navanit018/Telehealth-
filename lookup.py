import pandas as pd

# Load preprocessed dataset
df = pd.read_csv("dataset/preprocessed_dataset_clean.csv")

# ----------------------------
# Create lookup dictionaries
# ----------------------------
# Disease → List of Symptoms
disease_to_symptoms = df.groupby('disease_name')['symptom_name'].apply(list).to_dict()

# Symptom → List of Diseases
symptom_to_diseases = df.groupby('symptom_name')['disease_name'].apply(list).to_dict()

# ----------------------------
# Functions
# ----------------------------

def get_symptoms(disease):
    """Return symptoms for a given disease"""
    return disease_to_symptoms.get(disease, [])

def get_possible_diseases(symptoms):
    """Return diseases matching any of the input symptoms"""
    possible_diseases = set()
    for symptom in symptoms:
        diseases = symptom_to_diseases.get(symptom, [])
        possible_diseases.update(diseases)
    return list(possible_diseases)

# ----------------------------
# Example Usage
# ----------------------------
print("Symptoms of 'panic disorder':")
print(get_symptoms('panic disorder'))

print("\nDiseases for symptoms ['headache', 'nausea']:")
print(get_possible_diseases(['headache', 'nausea']))
