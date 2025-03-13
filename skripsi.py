import streamlit as st
import plotly.express as px
import pandas as pd
import random
from PIL import Image, ImageDraw
import io

# Custom Streamlit Theme (Gen Z Vibes)
st.markdown("""
    <style>
        body {
            background-color: #FFC0CB;
            color: #800080;
        }
        .stApp {
            background-color: #FF69B4;
        }
        .stSidebar {
            background-color: #FFB6C1;
        }
        .css-1d391kg {
            color: #FF1493 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Dummy data untuk jumlah gambar per kelas
CLASS_DISTRIBUTION = {
    "COVID-19": 5000,
    "Pneumonia": 15000,
    "Normal": 13920
}

def generate_dummy_image(class_name):
    """Buat gambar dummy berdasarkan kelas dengan warna Gen Z vibes."""
    colors = {"COVID-19": "#FF1493", "Pneumonia": "#FFD700", "Normal": "#32CD32"}
    img = Image.new("RGB", (200, 200), colors.get(class_name, "gray"))
    draw = ImageDraw.Draw(img)
    draw.text((50, 90), class_name, fill="white")
    return img

# Streamlit UI
st.title("🌈✨ Chest X-ray Dataset✨🌈")
st.sidebar.header("⚙️ Settings")

# Visualisasi distribusi data
data_df = pd.DataFrame(list(CLASS_DISTRIBUTION.items()), columns=['Class', 'Count'])
fig = px.bar(data_df, x='Class', y='Count', title="🔥 Class Distribution in Dataset 🔥",
             color='Class', text='Count', template='plotly_dark')
st.plotly_chart(fig)

# Pilihan kelas gambar
st.subheader("💖 Sample X-ray Images 💖")
selected_class = st.selectbox("🎀 Choose Class:", list(CLASS_DISTRIBUTION.keys()))
num_images = st.slider("💎 Select Number of Images to Display", 1, 10, 5)

# Tampilkan gambar dummy
cols = st.columns(min(5, num_images))
for i in range(num_images):
    with cols[i % len(cols)]:
        img = generate_dummy_image(selected_class)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        st.image(img_bytes.getvalue(), caption=f"✨ {selected_class} {i+1} ✨", use_column_width=True)
