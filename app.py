import streamlit as st
import pandas as pd
from PIL import Image
import unicodedata
import requests
from io import BytesIO
import base64
import os

# =============== UTILITIES =============== #
def normalize_text(text):
    """Normalize text to avoid encoding issues."""
    return unicodedata.normalize("NFKC", text).strip()

def upload_to_github(file_content, file_path, commit_message, token, repo_owner, repo_name):
    """
    Upload a file to a GitHub repository.

    Args:
        file_content (bytes): Content of the file to upload.
        file_path (str): Path in the GitHub repository to save the file.
        commit_message (str): Commit message for the file.
        token (str): GitHub Personal Access Token.
        repo_owner (str): GitHub username or organization name.
        repo_name (str): Name of the repository.

    Returns:
        str: Public URL of the uploaded file.
    """
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    response = requests.get(api_url, headers={"Authorization": f"token {token}"})

    if response.status_code == 200:
        sha = response.json()["sha"]  # File exists, get its SHA
    else:
        sha = None  # File does not exist

    # Encode the file content
    encoded_content = base64.b64encode(file_content).decode("utf-8")

    # Prepare payload
    payload = {
        "message": commit_message,
        "content": encoded_content,
        "sha": sha,
    }

    # Upload the file
    upload_response = requests.put(api_url, json=payload, headers={"Authorization": f"token {token}"})

    if upload_response.status_code in [200, 201]:
        return upload_response.json()["content"]["html_url"]
    else:
        st.error(f"Error uploading file to GitHub: {upload_response.json()}")
        return None

# Hosted design image URLs (replace with actual URLs)
image_urls = [
    "https://drive.google.com/uc?id=1QFgXKzYro_YuFeyHQ1rlN0SPWecnhXtF",
    "https://drive.google.com/uc?id=19WNVp-0ceDcnLgBF75tseF_gmA11hHXW",
    "https://drive.google.com/uc?id=1YhCGFUwu9dIeH3SuVac8fHM0HMm9XlcN",
    "https://drive.google.com/uc?id=1bFg3BR860tg9xyMucg3I609X3owo-ALZ",
]

# GitHub credentials and repo details
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
REPO_OWNER = "GeorgiaChatz"          # Replace with your GitHub username
REPO_NAME = "AppTest"                 # Replace with your repo name
CSV_PATH = "data/results.csv"         # Path to save the CSV in the repo

all_names = [
    "Aspa", "Μαρία Παλλικάρη", "Μαριάννα Στεφανοπούλου", "Θεοδώρα", "Χριστίνα",
    "Μαρία Κανναβού", "Άννα Κανναβού", "Άννα Μπουργανού", "Μαρία Παπαγεωργίου",
    "Αριάδνη", "Μαρία Φυτράκη", "Στεφανία", "Έλλη", "Μπρουνίλντα", "Αναστασία",
    "Μαρία Μητροπούλου", "Μιχαέλα", "Αδερφή νύφης"
]

color_options = [
    "Λαδί", "Γκρι ανοιχτό", "Μαύρο", "Καφέ", "Γκρι σκούρο", "Μωβ", "Φούξια",
    "Γκρι", "Πράσινο", "Κίτρινο", "Πορτοκαλί", "Κόκκινο", "Μπλε", "Θαλασσί", "Τιρκουάζ"
]

all_sizes = {"XS", "S", "M", "L", "XL"}

# =============== PAGE DESIGN =============== #
st.set_page_config(page_title="Bachelor Party Planner")

st.markdown("""<style> body { background-color: #f7e1d7; color: #4e4e50; } h1, h3 { color: #8e44ad; } </style>""", unsafe_allow_html=True)

st.title("Bachelor Party Planner")
st.header("Welcome to the Bachelor Party App!")

# =============== FORM =============== #
with st.form("party_form"):
    name = st.selectbox("Το όνομά σου:", [""] + all_names)
    color_choice = st.selectbox("Επίλεξε χρώμα φούτερ:", color_options)
    sizes = st.selectbox("Επίλεξε μέγεθος:", all_sizes)

    st.subheader("Διάλεξε ένα από αυτά τα 4 σχέδια για να τυπώσεις στο φούτερ:")
    chosen_design = st.radio("Ποιο σχέδιο θες να βάλουμε;", ["1o", "2o", "3o", "4o"], horizontal=True)

    cols = st.columns(4)
    for i, (url, label) in enumerate(zip(image_urls, ["1o", "2o", "3o", "4o"])):
        with cols[i]:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=label, width=120)

    wish = st.text_area("Γράψε μια ευχή για τη νύφη:")
    story = st.text_area("Πες μας πώς γνωριστήκατε ή μια ιστορία:")
    uploaded_files = st.file_uploader("Ανέβασε φωτογραφίες (πολλαπλές):", accept_multiple_files=True)

    submitted = st.form_submit_button("Submit")

# =============== FORM SUBMISSION =============== #
if submitted:
    if name.strip() == "":
        st.error("Παρακαλώ διάλεξε το όνομά σου από τη λίστα.")
    else:
        new_data = {
            "Name": normalize_text(name),
            "Color Preference": normalize_text(color_choice),
            "Size": normalize_text(sizes),
            "Selected Design": normalize_text(chosen_design),
            "Wish": normalize_text(wish),
            "Story": normalize_text(story),
        }

        # Upload the results as a CSV file
        csv_content = pd.DataFrame([new_data]).to_csv(index=False).encode("utf-8")
        csv_url = upload_to_github(csv_content, CSV_PATH, "Update results", GITHUB_TOKEN, REPO_OWNER, REPO_NAME)

        # Handle uploaded photos
        if uploaded_files:
            photo_urls = []
            for file in uploaded_files:
                photo_path = f"photos/{file.name}"
                photo_url = upload_to_github(file.read(), photo_path, f"Upload photo {file.name}", GITHUB_TOKEN, REPO_OWNER, REPO_NAME)
                if photo_url:
                    photo_urls.append(photo_url)

            st.write("### Uploaded Photos:")
            for url in photo_urls:
                st.markdown(f"[View Photo]({url})")

        st.success(f"Ευχαριστούμε πολύ, {name}!")
        if csv_url:
            st.markdown(f"[View Results CSV]({csv_url})")
