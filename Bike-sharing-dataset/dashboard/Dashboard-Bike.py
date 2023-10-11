import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Fungsi ini mengelompokkan data berdasarkan hari libur (holiday) dan menghitung jumlah unik 'instant'.
# Itu akan digunakan untuk menghasilkan plot tentang jumlah sepeda pada hari kerja vs. hari libur.
def holiday(df):
    holiday_day_data = df.groupby(by="holiday").instant.nunique().reset_index()
    holiday_day_data.rename(columns={ "instant": "sum"}, inplace=True)
    return holiday_day_data
# Fungsi ini mengembalikan subset dari data jam (hour_bike) yang hanya berisi data pada hari libur.
def hrdd(df):
    hrd  = df[df['holiday']=='Holiday']
    return hrd
# Fungsi ini mengelompokkan data berdasarkan musim (season) dan menghitung jumlah unik 'instant'.
# Ini akan digunakan untuk menghasilkan plot tentang jumlah sepeda berdasarkan musim.
def seasond(df):
    season_data = df.groupby(by="season").instant.nunique().reset_index()
    season_data.rename(columns={"instant": "sum"}, inplace=True)
    
    return season_data

# Fungsi sidebar untuk mengatur rentang waktu dengan bantuan widget 'date_input' dari Streamlit.
def sidebar(df):
    df["dteday"] = pd.to_datetime(df["dteday"])
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()
    with st.sidebar:

        def on_change():
            st.session_state.date = date

        date = st.date_input(
            label="Rentang Waktu",
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date],
            on_change=on_change
        )

    return date

# Membaca data dari file CSV dan mengatur rentang waktu sesuai dengan yang dipilih oleh pengguna.
day_bike = pd.read_csv("cleandataday.csv")
hour_bike = pd.read_csv("cleanhourdata.csv")

date = sidebar(day_bike)
if len(date) == 2:
    main_df = day_bike[(day_bike["dteday"] >= str(date[0])) & (day_bike["dteday"] <= str(date[1]))]
    h_df = hour_bike[(hour_bike["dteday"] >= str(date[0])) & (hour_bike["dteday"] <= str(date[1]))]
else:
    main_df = day_bike[ (day_bike["dteday"] >= str(st.session_state.date[0])) & (day_bike["dteday"] <= str(st.session_state.date[1]))]
    h_df = hour_bike[ (hour_bike["dteday"] >= str(st.session_state.date[0])) & (hour_bike["dteday"] <= str(st.session_state.date[1]))]

# Memanggil fungsi-fungsi yang telah didefinisikan untuk menghasilkan data yang akan digunakan dalam plot.
holiday = holiday(main_df)
hrdd = hrdd(h_df)
seasond = seasond(h_df)

# Mulai membuat dan menampilkan plot dengan menggunakan Seaborn.
# Setiap subheader berisi judul untuk setiap plot.

# Plot jumlah sepeda pada hari kerja vs. hari libur.

st.header("Bike Share Monitoring Dashboard :")
st.subheader("Workday")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="sum",
    x="holiday",
    data=holiday.sort_values(by="holiday", ascending=False),
    ax=ax
)
ax.set_title("Number of Bicycles on Workdays", loc="center", fontsize=50)
ax.set_ylabel("Number of Users")
ax.set_xlabel("Workdays")
ax.tick_params(axis="x", labelsize=30)
ax.tick_params(axis="y", labelsize=20)
st.pyplot(fig)

# Plot jumlah sepeda berdasarkan jam.
st.subheader("Hour Day")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="cnt",
    x="hr",
    data=hrdd.sort_values(by="hr", ascending=False),
)
ax.set_title("Number of Bike Sharing by Hour", loc="center", fontsize=50)
ax.set_ylabel("Number of Users")
ax.set_xlabel("Hour")
ax.tick_params(axis="x", labelsize=30)
ax.tick_params(axis="y", labelsize=20)
st.pyplot(fig)

# Plot jumlah sepeda berdasarkan waktu hari.
st.subheader("Time Of Day")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="cnt",
    x="time_of_day",
    data=hrdd.sort_values(by="time_of_day", ascending=False),
)
ax.set_title("Number of Bike Sharing by Time Of Day", loc="center", fontsize=50)
ax.set_ylabel("Number of Users")
ax.set_xlabel("Time Of Day")
ax.tick_params(axis="x", labelsize=30)
ax.tick_params(axis="y", labelsize=20)
st.pyplot(fig)

# Plot jumlah sepeda berdasarkan musim.
st.subheader("Season")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="sum",
    x="season",
    data=seasond.sort_values(by="season", ascending=False),
)
ax.set_title("Number of Bike Sharing by Season", loc="center", fontsize=50)
ax.set_ylabel("Number of Users")
ax.set_xlabel("Season")
ax.tick_params(axis="x", labelsize=30)
ax.tick_params(axis="y", labelsize=20)
st.pyplot(fig)

if __name__ == "__main__":
    # Menambahkan keterangan hak cipta di bawah dashboard.
    copyright = "Copyright © " + "2023 | Bike Sharing Dashboard | All Rights Reserved | " + "Made by: [@FaqihSuryana](https://www.linkedin.com/in/faqihsuryana/)"
    st.caption(copyright)
