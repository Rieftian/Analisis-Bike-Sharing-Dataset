import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

#Import file csv
df = pd.read_csv("dashboard/data_sepeda_bersih.csv")

#Judul Dashboard
st.title("Dashboard Analisis Bike Sharing Dataset Harian")

#Penjelasan Dataset
st.subheader("Tentang Dataset")
st.markdown("""<div style='text-align: justify'>
Dataset ini merupakan data penyewaan sepeda harian yang mencatat jumlah 
pengguna sepeda di suatu kota dalam periode tertentu. Setiap record mencakup
informasi seperti jumlah total pengguna, jumlah pengguna casual dan registered, 
serta berbagai atribut yang memengaruhi penggunaan sepeda, termasuk hari dalam minggu,
bulan, musim, kondisi cuaca, suhu, kelembapan, dan kecepatan angin. Dataset ini memungkinkan
analisis pola penggunaan sepeda berdasarkan waktu, tipe pengguna, dan kondisi lingkungan, 
sehingga dapat digunakan untuk memahami perilaku pengguna, mengidentifikasi tren musiman atau
harian, dan mendukung perencanaan operasional serta strategi promosi layanan sepeda.</div>""",unsafe_allow_html=True)
st.write("\n")
st.write(df.head())

st.subheader("Statistik Utama Pengguna")
#Menambahkan selectbox filter
import streamlit as st
 
filter = st.selectbox(
    label="Filter tanggal",
    options=('Tidak Aktif','Pilih Tanggal')
)
df['dteday'] = pd.to_datetime(df['dteday'])
if filter == 'Pilih Tanggal':
    start_date, end_date = st.date_input("Pilih rentang tanggal",
                                         value=[df['dteday'].min(),df['dteday'].max()],
                                         min_value = df['dteday'].min(),
                                         max_value = df['dteday'].max())
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    df_filtered = df[(df["dteday"] >= start_date) & (df['dteday'] <= end_date)]
else:
    df_filtered = df.copy()

#Memasukkan nilai - nilai kunci

pengguna_harian = df_filtered['cnt'].sum()
rata_rata_pengguna_harian = df_filtered['cnt'].mean()
pengguna_max = df_filtered['cnt'].max()
pengguna_min = df_filtered['cnt'].min()

pengguna_casual = df_filtered['casual'].sum()
rata_rata_casual_harian = df_filtered['casual'].mean()
pengguna_max_casual = df_filtered['casual'].max()
pengguna_min_casual = df_filtered['casual'].min()

pengguna_registered = df_filtered['registered'].sum()
rata_rata_registered_harian = df_filtered['registered'].mean()
pengguna_max_registered = df_filtered['registered'].max()
pengguna_min_registered = df_filtered['registered'].min()


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total pengguna", value=pengguna_harian)
    st.metric(label="Rata-rata pengguna per Hari", value=int(rata_rata_pengguna_harian))
    st.metric(label="Pengguna harian maksimum",value=pengguna_max)
    st.metric(label="Pengguna harian minimum",value=pengguna_min)

with col2:
    st.metric(label="Total pengguna Casual", value=pengguna_casual)
    st.metric(label="Rata-rata pengguna casual", value=int(rata_rata_casual_harian))
    st.metric(label="Pengguna harian maksimum",value=pengguna_max_casual)
    st.metric(label="Pengguna harian minimum",value=pengguna_min_casual)

with col3:
    st.metric(label="Total pengguna Registered", value=pengguna_registered)
    st.metric(label="Rata-rata pengguna registered", value=int(rata_rata_registered_harian))
    st.metric(label="Pengguna harian maksimum",value=pengguna_max_registered)
    st.metric(label="Pengguna harian minimum",value=pengguna_min_registered)

#Menampilkan hasil visualisasi data berdasarkan waktu
st.subheader("Visualisasi Data Berdasarkan Waktu")
formatter = plt.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', '.'))


tab1, tab2, tab3,  tab4 = st.tabs(["Tahun", "Musim", "Bulan","Hari"])

with tab1:
    user_tahun= st.selectbox(
    label="Pilih Jenis Pengguna",
    options=('Seluruh Pengguna','Pengguna Casual','Pengguna Registered'),
    key="user_tahun")

    if user_tahun == 'Seluruh Pengguna':
        user_col_tahun = 'cnt'
    
    elif user_tahun == 'Pengguna Casual':
        user_col_tahun = 'casual'

    else: 
        user_col_tahun = 'registered'

    tot_tahun = df.groupby('yr')[user_col_tahun].sum()
    
    fig, ax = plt.subplots(figsize=(10,5))
    colors = ['skyblue', 'salmon']
    ax.bar(tot_tahun.index.astype(str), tot_tahun.values, color=colors)
    ax.set_title(f"Jumlah {user_tahun} per Tahun")
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Jumlah Pengguna")
    ax.yaxis.set_major_formatter(formatter)
    ax.set_xticks([0,1],("2011","2012"),rotation=0)
    st.pyplot(fig) 

with tab2:
    user_musim = st.selectbox(
    label="Pilih Jenis Pengguna",
    options=('Seluruh Pengguna','Pengguna Casual','Pengguna Registered'),
    key="user_musim") 

    if user_musim == 'Seluruh Pengguna':
        user_col_musim = 'cnt'
    
    elif user_musim == 'Pengguna Casual':
        user_col_musim = 'casual'

    else: 
        user_col_musim = 'registered'

    tot_musim = df.groupby('season')[user_col_musim].sum()
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(tot_musim.index.astype(str), tot_musim.values, color='skyblue')
    ax.set_title(f"Jumlah {user_musim} per Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Pengguna")
    ax.yaxis.set_major_formatter(formatter)
    ax.set_xticks([0,1,2,3],('Springer','Summer','Fall','Winter'),rotation=0)
    st.pyplot(fig)

with tab3:
    user_bulan = st.selectbox(
    label="Pilih Jenis Pengguna",
    options=('Seluruh Pengguna','Pengguna Casual','Pengguna Registered'),
    key="user_bulan") 

    if user_bulan == 'Seluruh Pengguna':
        user_col_bulan = 'cnt'
    
    elif user_bulan == 'Pengguna Casual':
        user_col_bulan = 'casual'

    else: 
        user_col_bulan = 'registered'

    tot_bulan = df.groupby('mnth')[user_col_bulan].sum()
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(tot_bulan.index.astype(str), tot_bulan.values, color='skyblue',marker="o",linewidth=2)
    ax.set_title(f"Jumlah {user_bulan} per Bulan    ")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pengguna")
    ax.yaxis.set_major_formatter(formatter)
    ax.set_xticks(tot_bulan.index,('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'),rotation=0)
    st.pyplot(fig)

with tab4:
    user_hari = st.selectbox(
    label="Pilih Jenis Pengguna",
    options=('Seluruh Pengguna','Pengguna Casual','Pengguna Registered'),
    key="user_hari") 

    if user_hari == 'Seluruh Pengguna':
        user_col_hari = 'cnt'
    
    elif user_hari == 'Pengguna Casual':
        user_col_hari = 'casual'

    else: 
        user_col_hari = 'registered'

    tot_hari = df.groupby('weekday')[user_col_hari].sum()
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(tot_hari.index.astype(str), tot_hari.values, color='skyblue')
    ax.set_title(f"Jumlah {user_hari} per Musim")
    ax.set_xlabel("Hari")
    ax.set_ylabel("Jumlah Pengguna")
    ax.yaxis.set_major_formatter(formatter)
    ax.set_xticks(tot_hari.index,['Minggu','Senin','Selasa','Rabu','Kamis','Jumat','Sabtu'],rotation=0)
    st.pyplot(fig)

#Menampilkan hasil visualisasi data berdasarkan cuaca
st.subheader("Visualisasi Data Berdasarkan Kondisi Lingkungan")
tab5, tab6, tab7, tab8 = st.tabs(["Cuaca","Suhu","Kelembapan","Kecepatan Angin"])

with tab5:
    user_cuaca = st.selectbox(
    label="Pilih Jenis Pengguna",
    options=('Seluruh Pengguna','Pengguna Casual','Pengguna Registered'),
    key="user_cuaca")

    if user_cuaca == 'Seluruh Pengguna':
        user_col_cuaca = 'cnt'
    
    elif user_cuaca == 'Pengguna Casual':
        user_col_cuaca = 'casual'

    else: 
        user_col_cuaca = 'registered'
    
    tot_cuaca = df.groupby('weathersit')[user_col_cuaca].mean()
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(tot_cuaca.index.astype(str), tot_cuaca.values, color='skyblue')
    ax.set_title(f"Rata - Rata {user_cuaca} Berdasarkan Cuaca per Hari")
    ax.set_xlabel("Cuaca")
    ax.set_ylabel("Jumlah Pengguna")
    ax.yaxis.set_major_formatter(formatter)
    ax.set_xticks([0,1,2],['Clear','Mist/Cloudy','Light Rain/Snow'],rotation=0)
    st.pyplot(fig)

with tab6:
    user_suhu = st.selectbox(
    label="Pilih Jenis Pengguna",
    options=('Seluruh Pengguna','Pengguna Casual','Pengguna Registered'),
    key="user_suhu")

    if user_suhu == 'Seluruh Pengguna':
        user_col_suhu = 'cnt'
    
    elif user_suhu == 'Pengguna Casual':
        user_col_suhu = 'casual'

    else: 
        user_col_suhu = 'registered'
    
    tot_suhu = df.groupby('temp_bin')[user_col_suhu].mean()
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(tot_suhu.index.astype(str), tot_suhu.values, color='skyblue')
    ax.set_title(f"Rata - Rata {user_suhu} Berdasarkan Suhu per Hari")
    ax.set_xlabel("Kategori Suhu")
    ax.set_ylabel("Jumlah Pengguna")
    ax.yaxis.set_major_formatter(formatter)
    st.pyplot(fig)

with tab7:
    user_kelembapan = st.selectbox(
    label="Pilih Jenis Pengguna",
    options=('Seluruh Pengguna','Pengguna Casual','Pengguna Registered'),
    key="user_kelembapan")

    if user_kelembapan == 'Seluruh Pengguna':
        user_col_kelembapan = 'cnt'
    
    elif user_kelembapan == 'Pengguna Casual':
        user_col_kelembapan = 'casual'

    else: 
        user_col_kelembapan = 'registered'
    
    tot_kelembapan = df.groupby('hum_bin')[user_col_kelembapan].mean()
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(tot_kelembapan.index.astype(str), tot_kelembapan.values, color='skyblue')
    ax.set_title(f"Rata - Rata {user_kelembapan} Berdasarkan Kelembapan per Hari")
    ax.set_xlabel("Kategori Kelembapan")
    ax.set_ylabel("Jumlah Pengguna")
    ax.yaxis.set_major_formatter(formatter)
    st.pyplot(fig)

with tab8:
    user_kecepatan_angin = st.selectbox(
    label="Pilih Jenis Pengguna",
    options=('Seluruh Pengguna','Pengguna Casual','Pengguna Registered'),
    key="user_kecepatan_angin")

    if user_kecepatan_angin == 'Seluruh Pengguna':
        user_col_kecepatan_angin = 'cnt'
    
    elif user_kecepatan_angin == 'Pengguna Casual':
        user_col_kecepatan_angin = 'casual'

    else: 
        user_col_kecepatan_angin = 'registered'
    
    tot_kecepatan_angin = df.groupby('windspeed_bin')[user_col_kecepatan_angin].mean()
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(tot_kecepatan_angin.index.astype(str), tot_kecepatan_angin.values, color='skyblue')
    ax.set_title(f"Rata - Rata {user_kecepatan_angin} Berdasarkan Kecepatan Angin per Hari")
    ax.set_xlabel("Kategori Kecepatan Angin")
    ax.set_ylabel("Jumlah Pengguna")
    ax.yaxis.set_major_formatter(formatter)
    st.pyplot(fig)

#Menambahkan Sidebar
  
st.sidebar.title("Tentang Dashboard")
st.sidebar.markdown("""
**Dashboard Bike Sharing**  
<div style='text-align: justify'>Menampilkan jumlah pengguna sepeda harian, tren per tahun, bulan, musim, dan kategori cuaca.  
Periode data: 1 Januari 2011 – 31 Desember 2012.  
\nTipe pengguna: Seluruh Pengguna / Casual / Registered.</div>""",unsafe_allow_html=True)

st.sidebar.download_button(
    label="Download Dataset",
    data=df.to_csv(index=False),
    file_name="bike_sharing.csv",
    mime="text/csv"
)

st.caption('Copyright (c) Rieftian Havil Syawalludy')
