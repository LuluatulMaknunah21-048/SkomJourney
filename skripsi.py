import streamlit as st
import plotly.express as px
import pandas as pd

# Contoh Data
df = pd.DataFrame({
    "Kategori": ["A", "B", "C", "D"],
    "Nilai": [10, 20, 15, 25]
})

# Buat Bar Chart Interaktif
fig = px.bar(df, x="Kategori", y="Nilai", title="Contoh Plotly di Streamlit")

# Tampilkan di Streamlit
st.plotly_chart(fig)

