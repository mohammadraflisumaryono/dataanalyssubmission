import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np

# Load dataset yang sudah dibersihkan
day_clean_df = pd.read_csv("./day_clean.csv")
hour_clean_df = pd.read_csv("./hour_clean.csv")

# Judul Dashboard
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚴", layout="wide")
st.title("🚴 Bike Sharing Dashboard")
st.markdown("""
Dashboard ini menampilkan analisis data Bike Sharing Dataset untuk memahami pola penyewaan sepeda berdasarkan musim, cuaca, dan hari.
""")


# Konfigurasi Sidebar
st.sidebar.title("🚀 Navigasi")
if "page" not in st.session_state:
    st.session_state["page"] = "Overview"


# Buat menu navigasi dengan tombol
st.sidebar.markdown("### **Pilih Analisis**")
if st.sidebar.button("🏠 Overview"):
    st.session_state.page = "Overview"

if st.sidebar.button("🌦️ Pengaruh Musim"):
    st.session_state.page = "Pengaruh Musim"

if st.sidebar.button("☔ Dampak Cuaca"):
    st.session_state.page = "Dampak Cuaca"

if st.sidebar.button("📅 Hari Kerja vs Akhir Pekan"):
    st.session_state.page = "Hari Kerja vs Akhir Pekan"

if st.sidebar.button("📊 Analisis Lanjutan"):
    st.session_state.page = "Analisis Lanjutan"

# Fungsi untuk menampilkan overview
def show_overview():
    st.header("📊 Overview Data Bike Sharing")
    
    
    # Statistik dasar
    st.subheader("Statistik Dasar")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Penyewaan", f"{day_clean_df['cnt'].sum():,}")
    with col2:
        st.metric("Rata-rata Penyewaan Harian", f"{day_clean_df['cnt'].mean():.0f}")
    with col3:
        st.metric("Tahun Analisis", "2011 - 2012")
    
    # Distribusi penyewaan
    st.subheader("Distribusi Jumlah Penyewaan Harian")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(day_clean_df['cnt'], kde=True, color='skyblue', ax=ax)
    ax.set_title('Distribusi Jumlah Penyewaan Sepeda Harian', fontsize=14)
    ax.set_xlabel('Jumlah Penyewaan', fontsize=12)
    ax.set_ylabel('Frekuensi', fontsize=12)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

    # Tampilkan data
    st.subheader("Data Penyewaan Harian")
    st.dataframe(day_clean_df.head(10), use_container_width=True)
    
    
    # Kesimpulan
    st.markdown("""
    **Kesimpulan:**
    - Data menunjukkan distribusi bimodal, yang mengindikasikan adanya dua pola penyewaan yang berbeda (mungkin terkait hari kerja vs akhir pekan).
    - Rata-rata penyewaan harian adalah sekitar 4.500 sepeda.
    """)

# Fungsi untuk menampilkan analisis pengaruh musim
def show_season_analysis():
    st.header("🍂 Pengaruh Musim terhadap Jumlah Penyewaan Sepeda")
    
    # Rata-rata penyewaan berdasarkan musim
    season_rentals = day_clean_df.groupby('season_desc')['cnt'].mean()
    
    # Visualisasi menggunakan pie chart
    st.subheader("Proporsi Penyewaan Berdasarkan Musim")
    fig = px.pie(season_rentals, values=season_rentals.values, names=season_rentals.index, 
                 color_discrete_sequence=px.colors.sequential.Teal, hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
    
    # Visualisasi menggunakan bar chart
    st.subheader("Rata-rata Penyewaan Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(10, 6))
    season_rentals.plot(kind='bar', color='teal', alpha=0.7, ax=ax)
    ax.set_title('Rata-rata Penyewaan Sepeda berdasarkan Musim', fontsize=14)
    ax.set_xlabel('Musim', fontsize=12)
    ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_xticklabels(season_rentals.index, rotation=0)
    
    # Menambahkan label nilai
    for i, v in enumerate(season_rentals):
        ax.text(i, v + 100, f'{v:.0f}', ha='center', fontsize=10)
    
    st.pyplot(fig)
    
    # Kesimpulan
    st.markdown("""
    **Kesimpulan:**
    - Musim Fall (Gugur) memiliki rata-rata penyewaan tertinggi (~5.600 penyewaan/hari).
    - Musim Spring (Semi) memiliki rata-rata penyewaan terendah (~3.600 penyewaan/hari).
    - Penyewaan pada tahun 2012 lebih tinggi dibandingkan tahun 2011 untuk semua musim.
    """)

# Fungsi untuk menampilkan analisis dampak cuaca
def show_weather_analysis():
    st.header("🌤️ Dampak Cuaca terhadap Jumlah Penyewaan Sepeda")
    
    # Scatter plot suhu vs penyewaan
    st.subheader("Hubungan Temperatur dengan Jumlah Penyewaan")
    fig = px.scatter(day_clean_df, x='temp_actual', y='cnt', color='season_desc', 
                     labels={'temp_actual': 'Temperatur (°C)', 'cnt': 'Jumlah Penyewaan'},
                     title='Hubungan Temperatur dengan Jumlah Penyewaan Sepeda')
    st.plotly_chart(fig, use_container_width=True)
    
    # Scatter plot kelembaban vs penyewaan
    st.subheader("Hubungan Kelembaban dengan Jumlah Penyewaan")
    fig = px.scatter(day_clean_df, x='hum_actual', y='cnt', color='weather_desc', 
                     labels={'hum_actual': 'Kelembaban (%)', 'cnt': 'Jumlah Penyewaan'},
                     title='Hubungan Kelembaban dengan Jumlah Penyewaan Sepeda')
    st.plotly_chart(fig, use_container_width=True)
    
    # Kesimpulan
    st.markdown("""
    **Kesimpulan:**
    - Temperatur optimal untuk penyewaan sepeda adalah sekitar 25-30°C.
    - Kelembaban tinggi (>80%) mengurangi minat penyewaan.
    - Kondisi cuaca cerah (Clear/Few clouds) menghasilkan penyewaan tertinggi.
    """)

# Fungsi untuk menampilkan analisis hari kerja vs akhir pekan
def show_day_type_analysis():
    st.header("📅 Perbandingan Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
    
    # Pastikan kolom 'workingday_desc' ada di DataFrame
    if 'workingday_desc' not in day_clean_df.columns:
        st.error("Kolom 'workingday_desc' tidak ditemukan di DataFrame. Pastikan kolom ini sudah dibuat.")
        return
    
    # Rata-rata penyewaan berdasarkan tipe hari
    day_type_rentals = day_clean_df.groupby('workingday_desc')['cnt'].mean()
    
    # Visualisasi menggunakan pie chart
    st.subheader("Proporsi Penyewaan Berdasarkan Tipe Hari")
    fig = px.pie(day_type_rentals, values=day_type_rentals.values, names=day_type_rentals.index, 
                 color_discrete_sequence=px.colors.sequential.Purples, hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
    
    # Visualisasi menggunakan bar chart
    st.subheader("Rata-rata Penyewaan Berdasarkan Tipe Hari")
    fig, ax = plt.subplots(figsize=(10, 6))
    day_type_rentals.plot(kind='bar', color=['#ff9999', '#66b3ff'], alpha=0.7, ax=ax)
    ax.set_title('Rata-rata Penyewaan Sepeda: Hari Kerja vs Akhir Pekan/Libur', fontsize=14)
    ax.set_xlabel('Tipe Hari', fontsize=12)
    ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_xticklabels(day_type_rentals.index, rotation=0)
    
    # Menambahkan label nilai
    for i, v in enumerate(day_type_rentals):
        ax.text(i, v + 100, f'{v:.0f}', ha='center')
    
    st.pyplot(fig)
    
    # Kesimpulan
    st.markdown("""
    **Kesimpulan:**
    - Hari kerja memiliki rata-rata penyewaan yang sedikit lebih tinggi (~4.600 penyewaan/hari) dibandingkan akhir pekan/libur (~4.300 penyewaan/hari).
    - Pengguna registered mendominasi pada hari kerja, sementara pengguna casual lebih banyak pada akhir pekan.
    """)


# Fungsi untuk menampilkan analisis lanjutan
def show_advanced_analysis():
    st.header("🔍 Analisis Lanjutan")
    
    # Korelasi antara variabel cuaca dan penyewaan
    st.subheader("Korelasi antara Variabel Cuaca dan Penyewaan Sepeda")
    correlation_matrix = day_clean_df[['temp_actual', 'hum_actual', 'windspeed_actual', 'cnt']].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
    ax.set_title('Korelasi antara Variabel Cuaca dan Jumlah Penyewaan Sepeda', fontsize=14)
    st.pyplot(fig)
    
    # Tren penyewaan per jam
    st.subheader("Tren Penyewaan Sepeda per Jam")
    hourly_rentals = hour_clean_df.groupby('hr')['cnt'].mean()
    fig = px.line(hourly_rentals, x=hourly_rentals.index, y=hourly_rentals.values, 
                  labels={'x': 'Jam', 'y': 'Rata-rata Penyewaan'},
                  title='Rata-rata Penyewaan Sepeda per Jam')
    st.plotly_chart(fig, use_container_width=True)
    
    # Kesimpulan
    st.markdown("""
    **Kesimpulan:**
    - Suhu memiliki korelasi positif yang kuat dengan jumlah penyewaan (0.63).
    - Kelembaban memiliki korelasi negatif yang moderat (-0.32).
    - Tren penyewaan per jam menunjukkan dua puncak: pagi hari (7-9) dan sore hari (17-19).
    """)


if st.session_state.page == "Overview":
    show_overview()
elif st.session_state.page == "Pengaruh Musim":
    show_season_analysis()
elif st.session_state.page == "Dampak Cuaca":
    show_weather_analysis()
elif st.session_state.page == "Hari Kerja vs Akhir Pekan":
    show_day_type_analysis()
elif st.session_state.page == "Analisis Lanjutan":
    show_advanced_analysis()

# Tambahkan Copyright
st.markdown("---")
st.markdown("© 2025 Dashboard Data Analysis | All Rights Reserved")