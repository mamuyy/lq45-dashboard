
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Analisis Saham LQ45 - Ten Bagger Radar")

# Upload file Excel
uploaded_file = st.file_uploader("Upload file Excel hasil scraping", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("Data Fundamental Saham")
    st.dataframe(df)

    # Hitung skor sederhana
    df["Skor"] = (
        df["ROE (%)"].fillna(0)/5 +
        df["Revenue Growth (%)"].fillna(0)/10 +
        df["PER"].apply(lambda x: 5 if x < 10 else (3 if x < 20 else 1)) +
        df["PBV"].apply(lambda x: 5 if x < 1.5 else (3 if x < 3 else 1))
    )

    df_sorted = df.sort_values(by="Skor", ascending=False)

    st.subheader("Ranking Saham Potensial Ten Bagger")
    st.dataframe(df_sorted[["Kode Saham", "Nama Emiten", "Skor"]])

    # Radar Chart untuk 1 saham
    st.subheader("Radar Chart per Saham")
    selected = st.selectbox("Pilih saham", df["Kode Saham"])
    saham = df[df["Kode Saham"] == selected].iloc[0]
    radar_data = pd.DataFrame({
        "Kriteria": ["PER", "PBV", "ROE (%)", "Revenue Growth (%)"],
        "Nilai": [saham["PER"], saham["PBV"], saham["ROE (%)"], saham["Revenue Growth (%)"]]
    })

    fig = px.line_polar(radar_data, r='Nilai', theta='Kriteria', line_close=True)
    st.plotly_chart(fig, use_container_width=True)
