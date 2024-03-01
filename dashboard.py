import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image

#baca data
day_df = pd.read_csv("df_bike_sharing.csv")

#menghitung jumlah sewa berdasarkan hari
def daily_rent_df(data):
    daily_rent = data.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return daily_rent
    
#menghitung jumlah sewa berdasarkan bulan
def monthly_rent_df(data):
    monthly_rent = data.groupby(by='mnth').agg({
        'cnt': 'sum'
    })
    ordered_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_rent = monthly_rent.reindex(ordered_months, fill_value=0)
    return monthly_rent

#menghitung jumlah sewa berdasarkan weekday
def weekday_rent_df(data):
    weekday_rent = data.groupby(by='weekday').agg({
        'cnt': 'sum'
    }).reset_index()
    return weekday_rent

#menghitung jumlah sewa berdasarkan workingday
def workingday_rent_df(data):
    workingday_rent = data.groupby(by='workingday').agg({
        'cnt': 'sum'
    }).reset_index()
    return workingday_rent

#menghitung jumlah sewa berdasarkan holiday
def holiday_rent_df(data):
    holiday_rent = data.groupby(by='holiday').agg({
        'cnt': 'sum'
    }).reset_index()
    return holiday_rent

#menghitung jumlah sewa berdasarkan cuaca
def weather_rent_df(data):
    weather_rent = data.groupby(by='weathersit').agg({
        'cnt': 'sum'
    })
    return weather_rent


#membuat komponen filter
min_date = pd.to_datetime(day_df['dteday']).dt.date.min()
max_date = pd.to_datetime(day_df['dteday']).dt.date.max()
 
with st.sidebar:
    st.image('https://github.com/Adkurrr/Proyek-Analisis-Data-Bike-Sharing-Dataset/blob/main/bike-logo.png?raw=True')
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['dteday'] >= str(start_date)) & (day_df['dteday'] <= str(end_date))]

#menyiapkan  dataframe
daily_rent = daily_rent_df(main_df)
monthly_rent = monthly_rent_df(main_df)
weekday_rent = weekday_rent_df(main_df)
workingday_rent = workingday_rent_df(main_df)
holiday_rent = holiday_rent_df(main_df)
weather_rent = weather_rent_df(main_df)


#membuat Dashboard secara
# Membuat judul
st.header('Dashboard Rental Sewa Sepeda')

# Membuat jumlah penyewaan harian
st.subheader('Rental Berdasarkan Rentang Waktu (Harian)')

daily_rent_total = daily_rent['cnt'].sum()
st.metric('Jumlah Penyewa : ', value=daily_rent_total)
columns = st.columns(1)

# Membuat jumlah penyewaan bulanan
st.subheader('Rental berdasarkan Bulanan')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent.index,
    monthly_rent['cnt'],
    marker='o', 
    linewidth=2,
    color='tab:blue'
)

for index, row in enumerate(monthly_rent['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

#jumlah cuaca berdasarkan cuaca
st.subheader('Rental berdasarkan Cuaca')
fig, ax = plt.subplots(figsize=(16, 8))
colors=["tab:orange", "tab:blue", "tab:green"]

sns.barplot(
    x=weather_rent.index,
    y=weather_rent['cnt'],
    palette=colors,
    ax=ax
)

for index, row in enumerate(weather_rent['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Membuat jumlah penyewaan berdasarkan weekday, working dan holiday
st.subheader('Rental Berdasarkan Hari Kerja, Akhir Pekan, dan Hari Libur')
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15,10))
colors1=["tab:orange", "tab:green"]
colors2=["tab:orange", "tab:green"]
colors3=["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]

#berdasarkan workingday
sns.barplot(
    x='workingday',
    y='cnt',
    data=workingday_rent,
    palette=colors1,
    ax=axes[0])

for index, row in enumerate(workingday_rent['cnt']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Jumlah Penyewa Berdasarkan Hari Kerja')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

# Berdasarkan holiday
sns.barplot(
  x='holiday',
  y='cnt',
  data=holiday_rent,
  palette=colors2,
  ax=axes[1])

for index, row in enumerate(holiday_rent['cnt']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Jumlah Penyewa Berdasarkan Hari Libur')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

# Berdasarkan weekday
sns.barplot(
  x='weekday',
  y='cnt',
  data=weekday_rent,
  palette=colors3,
  ax=axes[2])

for index, row in enumerate(weekday_rent['cnt']):
    axes[2].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[2].set_title('JUmlah Penyewa Berdasarkan Akhir Pekan')
axes[2].set_ylabel(None)
axes[2].tick_params(axis='x', labelsize=15)
axes[2].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)

st.caption('Copyright (c) Ade Kurniawan')