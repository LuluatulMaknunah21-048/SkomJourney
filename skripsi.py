import streamlit as st
import os
import plotly.express as px
import pandas as pd
from PIL import Image
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import json
import random

# Load Google Drive API credentials
CREDENTIALS_PATH = "service_account.json"
if not os.path.exists(CREDENTIALS_PATH):
    st.error("Service account credentials not found! Upload 'service_account.json' to proceed.")
    st.stop()

# Autentikasi menggunakan Service Account
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
gauth = GoogleAuth()
gauth.credentials = creds
drive = GoogleDrive(gauth)

# ID Folder Google Drive tempat dataset disimpan
FOLDER_ID = "19CSJcfY37bEIhuJE3W3DMFK9CpHxVTvp"

# Fungsi untuk mendapatkan daftar file dalam folder
def get_file_list(folder_id):
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    return {file['title']: file['id'] for file in file_list}

file_dict = get_file_list(FOLDER_ID)

# Streamlit UI
st.title("📊 Chest X-ray Dataset Visualization")
st.sidebar.header("⚙️ Settings")

# Dummy dataset jika gagal load
dummy_data = pd.DataFrame({'Class': ['COVID-19', 'Pneumonia', 'Normal'], 'Count': [5000, 15000, 13920]})

# Pilih dataset
dataset_option = st.sidebar.selectbox("Select Dataset:", ['Train', 'Validation', 'Test'])

# Simulasi jumlah gambar per kategori (fallback jika tidak bisa akses GDrive)
data_df = dummy_data

fig = px.bar(data_df, x='Class', y='Count', title=f"Class Distribution in {dataset_option} Dataset",
             color='Class', text='Count', template='plotly_dark')
st.plotly_chart(fig)

# Preview beberapa gambar
st.subheader("📷 Sample X-ray Images")
num_images = st.slider("Select Number of Images to Display", 1, 10, 5)
selected_class = st.selectbox("Choose Class:", data_df['Class'].tolist())

# Ambil beberapa gambar dari Google Drive
if file_dict:
    selected_images = random.sample(list(file_dict.keys()), min(num_images, len(file_dict)))
    cols = st.columns(min(5, num_images))
    for idx, img_name in enumerate(selected_images):
        img_id = file_dict[img_name]
        img_url = f"https://drive.google.com/uc?id={img_id}"
        with cols[idx % len(cols)]:
            st.image(img_url, caption=img_name, use_column_width=True)
else:
    st.warning("Dataset not accessible. Showing sample data.")
