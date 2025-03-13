import streamlit as st
import os
import plotly.express as px
import pandas as pd
from PIL import Image
import gdown
import zipfile

# URL Google Drive (ubah sesuai dengan dataset yang dikompresi jadi ZIP)
GDRIVE_URL = "https://drive.google.com/uc?id=19CSJcfY37bEIhuJE3W3DMFK9CpHxVTvp"
ZIP_FILE = "dataset.zip"
EXTRACT_DIR = "dataset"

# Cek apakah dataset sudah diunduh
if not os.path.exists(EXTRACT_DIR):
    st.info("Downloading dataset from Google Drive...")
    gdown.download(GDRIVE_URL, ZIP_FILE, quiet=False)
    
    # Ekstrak dataset
    with zipfile.ZipFile(ZIP_FILE, "r") as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)

BASE_DIR = os.path.join(EXTRACT_DIR, "Dataset")
TRAIN_DIR = os.path.join(BASE_DIR, "Train")
VAL_DIR = os.path.join(BASE_DIR, "Val")
TEST_DIR = os.path.join(BASE_DIR, "Test")

# Fungsi untuk mengambil jumlah gambar per kategori
def count_images(directory):
    if not os.path.exists(directory):
        return pd.DataFrame({'Class': ['COVID-19', 'Pneumonia', 'Normal'], 'Count': [5000, 15000, 13920]})
    
    categories = os.listdir(directory)
    data = {category: len(os.listdir(os.path.join(directory, category))) for category in categories}
    return pd.DataFrame(list(data.items()), columns=['Class', 'Count'])

# Streamlit UI
st.title("📊 Chest X-ray Dataset Visualization")
st.sidebar.header("⚙️ Settings")

# Pilih dataset (Train, Val, Test)
dataset_option = st.sidebar.selectbox("Select Dataset:", ['Train', 'Validation', 'Test'])

if dataset_option == 'Train':
    data_df = count_images(TRAIN_DIR)
elif dataset_option == 'Validation':
    data_df = count_images(VAL_DIR)
else:
    data_df = count_images(TEST_DIR)

# Plot distribusi data
fig = px.bar(data_df, x='Class', y='Count', title=f"Class Distribution in {dataset_option} Dataset",
             color='Class', text='Count', template='plotly_dark')
st.plotly_chart(fig)

# Preview beberapa gambar
st.subheader("📷 Sample X-ray Images")
num_images = st.slider("Select Number of Images to Display", 1, 10, 5)
selected_class = st.selectbox("Choose Class:", data_df['Class'].tolist())

img_dir = os.path.join(BASE_DIR, dataset_option, selected_class)
if os.path.exists(img_dir):
    image_files = os.listdir(img_dir)[:num_images]
    cols = st.columns(min(5, num_images))
    for idx, img_file in enumerate(image_files):
        img_path = os.path.join(img_dir, img_file)
        image = Image.open(img_path)
        with cols[idx % len(cols)]:
            st.image(image, caption=img_file, use_column_width=True)
else:
    st.warning("Dataset not found. Showing sample data.")
