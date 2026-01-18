import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ==================================================
# CONFIG
# ==================================================
st.set_page_config(page_title="Telehealth App", layout="wide")
HISTORY_FILE = "patient_history.csv"

# ==================================================
# HIDE SIDEBAR
# ==================================================
st.markdown(
    "<style>[data-testid='stSidebar']{display:none;}</style>",
    unsafe_allow_html=True
)

# ==================================================
# LOAD KAGGLE DATASETS
# ==================================================
BASE_PATH = os.path.join("dataset", "Disease symptom prediction")

try:
    symptom_df = pd.read_csv(os.path.join(BASE_PATH, "dataset.csv"))
    desc_df = pd.read_csv(os.path.join(BASE_PATH, "symptom_Description.csv"))
    prec_df = pd.read_csv(os.path.join(BASE_PATH, "symptom_precaution.csv"))
    severity_df = pd.read_csv(os.path.join(BASE_PATH, "Symptom-severity.csv"))
except FileNotFoundError as e:
    st.error(f"Dataset file missing: {e.filename}")
    st.stop()

# ==================================================
# PREPARE DATA
# ==================================================
all_diseases = sorted(symptom_df["Disease"].unique())
severity_map = dict(zip(severity_df["Symptom"], severity_df["weight"]))

# ==================================================
# HELPER FUNCTIONS
# ==================================================
def get_symptoms(disease):
    row = symptom_df[symptom_df["Disease"] == disease]
    if row.empty:
        return []
    return row.iloc[0, 1:].dropna().tolist()


def get_description(disease):
    row = desc_df[desc_df["Disease"] == disease]
    return row.iloc[0]["Description"] if not row.empty else "No description available."


def get_precautions(disease):
    row = prec_df[prec_df["Disease"] == disease]
    if row.empty:
        return []
    return row.iloc[0, 1:].dropna().tolist()


def get_severity(symptom):
    score = severity_map.get(symptom, 0)
    if score >= 7:
        return "Severe 🔴"
    elif score >= 4:
        return "Moderate 🟠"
    return "Mild 🟢"


def save_history(disease, symptom_count):
    record = {"disease": disease, "symptom_count": symptom_count}
    if os.path.exists(HISTORY_FILE):
        h = pd.read_csv(HISTORY_FILE)
        h = pd.concat([h, pd.DataFrame([record])], ignore_index=True)
    else:
        h = pd.DataFrame([record])
    h.to_csv(HISTORY_FILE, index=False)


# ==================================================
# APP TITLE
# ==================================================
st.title("🩺 Telehealth Disease–Symptom System")

# ==================================================
# TABS
# ==================================================
tab1, tab2, tab3 = st.tabs(["🩺 Disease Lookup", "📊 Analytics", "📁 History"])

# ==================================================
# TAB 1 — DISEASE LOOKUP
# ==================================================
with tab1:
    st.subheader("🔍 Search Disease")
    query = st.text_input("Type disease name")
    matches = [d for d in all_diseases if query.lower() in d.lower()] if query else []
    selected_disease = st.selectbox("Results", matches)

    if selected_disease:
        symptoms = get_symptoms(selected_disease)
        emergency_flag = False

        st.markdown(f"## Symptoms of **{selected_disease}**")
        color_map = {"Severe 🔴": "red", "Moderate 🟠": "orange", "Mild 🟢": "green"}

        for s in symptoms:
            sev = get_severity(s)
            st.markdown(f"<span style='color:{color_map[sev]}'>{s} — {sev}</span>", unsafe_allow_html=True)
            if sev.startswith("Severe"):
                emergency_flag = True

        if emergency_flag:
            st.error("🚨 Severe symptoms detected. Seek immediate medical help.")

        st.markdown("### 📘 Disease Description")
        st.write(get_description(selected_disease))

        st.markdown("### 🛡️ Prevention / Precautions")
        for p in get_precautions(selected_disease):
            st.write(f"• {p}")

        st.warning("⚠️ Educational use only. Do not self-medicate.")

        # SAVE HISTORY
        if st.button("Save to History"):
            save_history(selected_disease, len(symptoms))
            st.success("Saved to patient history")

# ==================================================
# TAB 2 — ANALYTICS
# ==================================================
with tab2:
    st.subheader("📊 Disease Analytics")

    if os.path.exists(HISTORY_FILE):
        hist = pd.read_csv(HISTORY_FILE)
        if not hist.empty:
            counts = hist["disease"].value_counts()
            fig, ax = plt.subplots()
            ax.bar(counts.index, counts.values, color="skyblue")
            ax.set_xlabel("Disease")
            ax.set_ylabel("Search Count")
            ax.set_title("Disease Lookup Frequency")
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig)
        else:
            st.info("No data to analyze yet.")
    else:
        st.info("No history available.")

# ==================================================
# TAB 3 — HISTORY
# ==================================================
with tab3:
    st.subheader("📁 Patient History")
    if os.path.exists(HISTORY_FILE):
        hist = pd.read_csv(HISTORY_FILE)
        if not hist.empty:
            st.dataframe(hist)
            csv = hist.to_csv(index=False)
            st.download_button("Download History", csv, file_name="history.csv")
        else:
            st.info("No history found.")
    else:
        st.info("No history found.")

# ==================================================
# FOOTER
# ==================================================
st.caption("Educational Telehealth Application — Kaggle Dataset Based")

