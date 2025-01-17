# import .streamlit as st
# import pandas as pd
# from PIL import Image
# import unicodedata
# import requests
# from io import BytesIO
# import base64
# import datetime
#
# # =============== UTILITIES =============== #
# def normalize_text(text):
#     """Normalize text to avoid encoding issues."""
#     return unicodedata.normalize("NFKC", text).strip()
#
# def upload_to_github(file_content, file_path, commit_message, token, repo_owner, repo_name):
#     """Upload a file to a GitHub repository."""
#     api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
#     response = requests.get(api_url, headers={"Authorization": f"token {token}"})
#     sha = response.json()["sha"] if response.status_code == 200 else None
#
#     # Encode the file content
#     encoded_content = base64.b64encode(file_content).decode("utf-8")
#
#     # Prepare payload
#     payload = {
#         "message": commit_message,
#         "content": encoded_content,
#         "sha": sha,
#     }
#
#     # Upload the file
#     upload_response = requests.put(api_url, json=payload, headers={"Authorization": f"token {token}"})
#     if upload_response.status_code in [200, 201]:
#         return upload_response.json()["content"]["html_url"]
#     else:
#         st.error(f"Error uploading file to GitHub: {upload_response.json()}")
#         return None
#
# # Hosted design image URLs (replace with actual URLs)
# image_urls = [
#     "https://drive.google.com/uc?id=1QFgXKzYro_YuFeyHQ1rlN0SPWecnhXtF",
#     "https://drive.google.com/uc?id=19WNVp-0ceDcnLgBF75tseF_gmA11hHXW",
#     "https://drive.google.com/uc?id=1YhCGFUwu9dIeH3SuVac8fHM0HMm9XlcN",
#     "https://drive.google.com/uc?id=1bFg3BR860tg9xyMucg3I609X3owo-ALZ",
# ]
#
# # GitHub credentials and repo details
# GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]  # Use Streamlit Secrets
# REPO_OWNER = "GeorgiaChatz"               # Replace with your GitHub username
# REPO_NAME = "AppTest"                     # Replace with your repo name
# CSV_PATH = "data/results.csv"             # Path to save the CSV in the repo
#
# all_names = [
#     "Aspa", "Μαρία Παλλικάρη", "Μαριάννα Στεφανοπούλου", "Θεοδώρα", "Χριστίνα",
#     "Μαρία Κανναβού", "Άννα Κανναβού", "Άννα Μπουργανού", "Μαρία Παπαγεωργίου",
#     "Αριάδνη", "Μαρία Φυτράκη", "Στεφανία", "Έλλη", "Μπρουνίλντα", "Αναστασία",
#     "Μαρία Μητροπούλου", "Μιχαέλα", "Αδερφή νύφης"
# ]
#
# color_options = [
#     "Λαδί", "Γκρι ανοιχτό", "Μαύρο", "Καφέ", "Γκρι σκούρο", "Μωβ", "Φούξια",
#     "Γκρι", "Πράσινο", "Κίτρινο", "Πορτοκαλί", "Κόκκινο", "Μπλε", "Θαλασσί", "Τιρκουάζ"
# ]
#
# all_sizes = {"XS", "S", "M", "L", "XL"}
#
# # =============== PAGE DESIGN =============== #
# st.set_page_config(page_title="Bachelor Party Planner")
#
# st.markdown("""<style> body { background-color: #f7e1d7; color: #4e4e50; } h1, h3 { color: #8e44ad; } </style>""", unsafe_allow_html=True)
#
# st.title("Bachelor Party Planner")
# st.header("Welcome to the Bachelor Party App!")
#
# # =============== FORM =============== #
# with st.form("party_form"):
#     name = st.selectbox("Το όνομά σου:", [""] + all_names)
#     color_choice = st.selectbox("Επίλεξε χρώμα φούτερ:", color_options)
#     sizes = st.selectbox("Επίλεξε μέγεθος:", all_sizes)
#
#     st.subheader("Διάλεξε ένα από αυτά τα 4 σχέδια για να τυπώσεις στο φούτερ:")
#     chosen_design = st.radio("Ποιο σχέδιο θες να βάλουμε;", ["1o", "2o", "3o", "4o"], horizontal=True)
#
#     cols = st.columns(4)
#     for i, (url, label) in enumerate(zip(image_urls, ["1o", "2o", "3o", "4o"])):
#         with cols[i]:
#             response = requests.get(url)
#             img = Image.open(BytesIO(response.content))
#             st.image(img, caption=label, width=120)
#
#     wish = st.text_area("Γράψε μια ευχή για τη νύφη:")
#     story = st.text_area("Πες μας πώς γνωριστήκατε ή μια ιστορία:")
#     uploaded_files = st.file_uploader("Ανέβασε φωτογραφίες (πολλαπλές):", accept_multiple_files=True)
#
#     submitted = st.form_submit_button("Submit")
#
# # =============== FORM SUBMISSION =============== #
# if submitted:
#     if name.strip() == "":
#         st.error("Παρακαλώ διάλεξε το όνομά σου από τη λίστα.")
#     else:
#         timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#         new_data = {
#             "Name": normalize_text(name),
#             "Color Preference": normalize_text(color_choice),
#             "Size": normalize_text(sizes),
#             "Selected Design": normalize_text(chosen_design),
#             "Wish": normalize_text(wish),
#             "Story": normalize_text(story),
#             "Timestamp": timestamp,
#         }
#
#         # Read existing data
#         response = requests.get(f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{CSV_PATH}")
#         if response.status_code == 200:
#             existing_data = pd.read_csv(BytesIO(response.content))
#         else:
#             existing_data = pd.DataFrame()
#
#         # Append new data and save
#         updated_data = pd.concat([existing_data, pd.DataFrame([new_data])], ignore_index=True)
#         csv_content = updated_data.to_csv(index=False).encode("utf-8")
#         csv_url = upload_to_github(csv_content, CSV_PATH, "Append new results", GITHUB_TOKEN, REPO_OWNER, REPO_NAME)
#
#         # Handle uploaded photos
#         photo_urls = []
#         if uploaded_files:
#             for file in uploaded_files:
#                 photo_path = f"photos/{name}_{timestamp}_{file.name}"
#                 photo_url = upload_to_github(file.read(), photo_path, f"Upload photo {file.name}", GITHUB_TOKEN, REPO_OWNER, REPO_NAME)
#                 if photo_url:
#                     photo_urls.append(photo_url)
#
#             st.write("### Uploaded Photos:")
#             for url in photo_urls:
#                 st.markdown(f"- [View Photo]({url})")
#
#         st.success(f"Ευχαριστούμε πολύ, {name}!")
#         if csv_url:
#             st.markdown(f"[View Updated Results CSV]({csv_url})")
import streamlit as st
import pandas as pd
from PIL import Image
import unicodedata
import requests
import base64
import datetime
from io import BytesIO
import smtplib
import yagmail

def normalize_text(text):
    """Normalize text to avoid encoding issues."""
    return unicodedata.normalize("NFKC", text).strip()

def upload_to_github(file_content, file_path, commit_message, token, repo_owner, repo_name):
    """Upload a file to a GitHub repository."""
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    response = requests.get(api_url, headers={"Authorization": f"token {token}"})
    sha = response.json()["sha"] if response.status_code == 200 else None

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
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]  # Use Streamlit Secrets
REPO_OWNER = "GeorgiaChatz"               # Replace with your GitHub username
REPO_NAME = "AppTest"                     # Replace with your repo name

all_names = [
    "Aspa", "Μαρία Παλλικάρη", "Μαριάννα Στεφανοπούλου", "Θεοδώρα", "Χριστίνα",
    "Μαρία Κανναβού", "Άννα Κανναβού", "Άννα Μπουργανού", "Μαρία Παπαγεωργίου",
    "Αριάδνη", "Μαρία Φυτράκη", "Στεφανία", "Έλλη", "Μπρουνίλντα", "Αναστασία Κουμπάρα",
    "Μαρία Μητροπούλου", "Μιχαέλα", "Αδερφή νύφης"
]

color_options = [
    "Λαδί", "Γκρι ανοιχτό", "Μαύρο", "Καφέ", "Γκρι σκούρο", "Μωβ", "Φούξια",
    "Γκρι", "Πράσινο", "Κίτρινο", "Πορτοκαλί", "Κόκκινο", "Μπλε", "Θαλασσί", "Τιρκουάζ"
]

all_sizes = {"XS", "S", "M", "L", "XL"}

drive_links = {
    "Aspa": "https://drive.google.com/drive/folders/1IoAw9ST8qsI_E1rp-p81s6w0ED7rEZXb?usp=drive_link",
    "Μαρία Παλλικάρη": "https://drive.google.com/drive/folders/1IoAw9ST8qsI_E1rp-p81s6w0ED7rEZXb?usp=drive_link",
    "Μαριάννα Στεφανοπούλου": "https://drive.google.com/drive/folders/1IoAw9ST8qsI_E1rp-p81s6w0ED7rEZXb?usp=drive_link",
    "Θεοδώρα": "https://drive.google.com/drive/folders/1IoAw9ST8qsI_E1rp-p81s6w0ED7rEZXb?usp=drive_link",
    "Χριστίνα": "https://drive.google.com/drive/folders/1IoAw9ST8qsI_E1rp-p81s6w0ED7rEZXb?usp=drive_link",
    "Μαρία Κανναβού": "https://drive.google.com/drive/folders/1mL6_Gmo92sjqaWuusX5CkG4VMWeRERM-?usp=drive_link",
    "Άννα Κανναβού": "https://drive.google.com/drive/folders/1mL6_Gmo92sjqaWuusX5CkG4VMWeRERM-?usp=drive_link",
    "Μαρία Παπαγεωργίου": "https://drive.google.com/drive/folders/1mL6_Gmo92sjqaWuusX5CkG4VMWeRERM-?usp=drive_link",
    "Άννα Μπουργανού": "https://drive.google.com/drive/folders/1--7s-6NwMYSp4C0jApconJkuE8-Rx6v7?usp=drive_link",
    "Στεφανία": "https://drive.google.com/drive/folders/1pJgVjoWIWV07_ygCyOadGHDhG9ZL22vz?usp=drive_link",
    "Έλλη": "https://drive.google.com/drive/folders/1pJgVjoWIWV07_ygCyOadGHDhG9ZL22vz?usp=drive_link",
    "Μπρουνίλντα": "https://drive.google.com/drive/folders/1pJgVjoWIWV07_ygCyOadGHDhG9ZL22vz?usp=drive_link",
    "Αναστασία": "https://drive.google.com/drive/folders/1pJgVjoWIWV07_ygCyOadGHDhG9ZL22vz?usp=drive_link",
    "Μαρία Μητροπούλου": "https://drive.google.com/drive/folders/1pJgVjoWIWV07_ygCyOadGHDhG9ZL22vz?usp=drive_link",
    "Αριάδνη": "https://drive.google.com/drive/folders/1ndrBXu0JsgXRwT1yvQcBr0RUsqJ2PU7Y?usp=drive_link",
    "Μαρία Φυτράκη": "https://drive.google.com/drive/folders/1ndrBXu0JsgXRwT1yvQcBr0RUsqJ2PU7Y?usp=drive_link",
    "Μιχαέλα": "https://drive.google.com/drive/folders/1pJgVjoWIWV07_ygCyOadGHDhG9ZL22vz?usp=drive_link",
    "Αδερφή νύφης": "https://drive.google.com/drive/folders/1nq3sgxVaypdPJpk59ivic-Keipv9GWVq?usp=drive_link"
}

# =============== PAGE DESIGN =============== #
st.set_page_config(page_title="Bachelor Party Planner")

def set_background(image_url):
    """Set a background image using HTML and CSS for Streamlit Cloud."""
    st.markdown(
        f'''
        <style>
        .stApp {{
            background: url("{image_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        ''',
        unsafe_allow_html=True
    )

# Example image URL
background_image_url = "https://images.pexels.com/photos/255379/pexels-photo-255379.jpeg"
set_background(background_image_url)

# =============== TITLE & INTRO =============== #
st.title("Bachelor Party Planner")
st.header("Καλωσήρθατε στο Bachelor Party App!")
st.subheader("Παρακάτω είναι τα βήματα για να μην μπερδευτείς!📑")
st.write("1) **Διάλεξε το όνομά σου** από τη λίστα παρακάτω")
st.write("2) **Δες το φούτερ** που θα φορέσουμε: ➜ [Φούτερ & Διαθέσιμα χρώματα](https://www.livardas.gr/el/fouter/2077-17147-sols-slam-13251.html)")
st.write("3) **Διάλεξε ένα από τα 4 σχέδια** που θέλεις να τυπώσουμε στο φούτερ σου 🖋")
st.write("4) **Γράψε μια ευχή** για την Αννούλα και τη νέα της αρχή 💝")
st.write("5) **Γράψε πώς γνωριστήκατε** ή μια ιστορία που θέλεις να μοιραστείς👭")
st.write("6) **Ανέβασε προσωπικές σας φωτογραφίες!** Έχεις δύο επιλογές: \n\n ✔️  Ανέβασε τες εδώ στη πλατφόρμα \n\n ✔️  Στο τέλος της καταχώρισης θα σου εμφανιστεί ένα link, κάντο copy και ανέβασε τες εκεί με την ησυχία σου 📸")
st.write("6) **Πρότεινε μας ιδέες!** Θα σταλεί στο email σου το πρόγραμμα με λεπτομέρειες & το link για τις φωτογραφίες.Αν δεν έχεις email, μην ανησυχείς, το app έχει φροντίσει για σένα! 🎀")


# =============== FORM =============== #
with st.form("party_form"):
    name = st.selectbox("**Το όνομά σου:**", [""] + all_names)
    color_choice = st.selectbox("**Επίλεξε χρώμα φούτερ:**", color_options)
    sizes = st.selectbox("**Επίλεξε μέγεθος:**", all_sizes)
    email = st.text_input("**Συμπλήρωσε το email σου**")

    # st.subheader("Διάλεξε ένα από αυτά τα 4 σχέδια για να τυπώσεις στο φούτερ:")
    chosen_design = st.radio("**Επίλεξε σχέδιο:**", ["1o", "2o", "3o", "4o"], horizontal=True)
    

    cols = st.columns(4)
    for i, (url, label) in enumerate(zip(image_urls, ["1o", "2o", "3o", "4o"])):
        with cols[i]:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=label, width=120)

    wish = st.text_area("**Γράψε μας μια ευχή για τη νύφη:**")
    story = st.text_area("**Πες μας πώς γνωριστήκατε ή μια ιστορία:**")
    uploaded_files = st.file_uploader("**Ανέβασε φωτογραφίες αλλιώς πάρε το link:**", accept_multiple_files=True)

    submitted = st.form_submit_button("Φύγαμε 🍻")

# =============== FORM SUBMISSION =============== #
if submitted:
    if name.strip() == "":
        st.error("Παρακαλώ διάλεξε το όνομά σου από τη λίστα.")
    else:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        new_data = {
            "Name": normalize_text(name),
            "Color Preference": normalize_text(color_choice),
            "Size": normalize_text(sizes),
            "Selected Design": normalize_text(chosen_design),
            "Wish": normalize_text(wish),
            "Story": normalize_text(story),
            "Timestamp": timestamp,  # Unique identifier
        }

        # Save the data as a new file
        csv_name = f"submissions/{name}_{timestamp}.csv"
        csv_content = pd.DataFrame([new_data]).to_csv(index=False).encode("utf-8")
        csv_url = upload_to_github(csv_content, csv_name, "Add new submission", GITHUB_TOKEN, REPO_OWNER, REPO_NAME)

        # Handle uploaded photos
        photo_urls = []
        if uploaded_files:
            for file in uploaded_files:
                photo_path = f"photos/{name}_{timestamp}_{file.name}"
                photo_url = upload_to_github(file.read(), photo_path, f"Upload photo {file.name}", GITHUB_TOKEN, REPO_OWNER, REPO_NAME)
                if photo_url:
                    photo_urls.append(photo_url)
                    
        drive_link = drive_links[name]
        st.markdown(f"[Αυτό είναι το google drive link σου]({drive_link})")

        if email.strip() != "": 
           # Send the PDF via email with yagmail
            yag = yagmail.SMTP('georgiachatzilygeroudi@gmail.com', 'jdqofplsgxnadwnb', host='smtp.gmail.com', port=587, smtp_starttls=True, smtp_ssl=False)
    
            subject = "Anna's Bachelor"
    
            # Enclose the PDF
            yag.send(
            to=email,
            subject=subject,
            contents=f"Καλησπέρα {name},\n\n Σου έχω επισυνάψει το πρόγραμμα και τις λεπτομέρειες στο αρχείο pdf και εδώ είναι το Google Drive link για να ανεβάσεις ότι φωτογραφία θέλεις:\n\n{drive_link}\n\nΜε αγάπη,\nΤζο",
            attachments="Bachelorette.pdf"
            )
            
            # Close SMTP connection
            yag.close()
        else:
            st.warning("Δεν δόθηκε email. Μπορείτε να κατεβάσετε το PDF από εδώ:")
            with open("Bachelorette.pdf", "rb") as pdf_file:  # Update the path
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label="Κατεβάστε το PDF",
                    data=pdf_bytes,
                    file_name="Bachelorette.pdf",
                    mime="application/pdf"
                )

        # email = st.text_input("Δώσε μας το email σου για να σου στείλουμε το link:")
        # send_email(email, drive_link)
        # st.markdown(
        #             "<h3 style='color:green;'>🎉 Experiment completed successfully!</h3>",
        #             unsafe_allow_html=True
        #         )
        st.success(f"Ευχαριστούμε πολύ, {name} , ανυπομονούμε για την ημέρα εκείνη! 🎉")
        # st.write("### Η συμμετοχή σου έχει ως εξής:")
        # st.write(pd.DataFrame([new_data]))

        # if csv_url:
        #     st.markdown(f"[View Your Submission]({csv_url})")
