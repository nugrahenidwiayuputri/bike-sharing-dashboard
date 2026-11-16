import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from pathlib import Path

#  Konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

GREY, RED, BLUE, ORANGE, GREEN = "#B0B0B0", "#D9534F", "#1F77B4", "#FF7F0E", "#4C9F70"
WEATHER_ORDER = ["Cerah", "Berkabut", "Hujan/Salju Ringan"]
SEGMENT_LABELS = ["Dini Hari (00-05)", "Pagi (06-10)", "Siang (11-15)", "Sore (16-19)", "Malam (20-23)"]
TEMP_LABELS = ["Dingin (<10°C)", "Sejuk (10-20°C)", "Hangat (20-30°C)", "Panas (>30°C)"]


#  Load data 
@st.cache_data
def load_data():
    path = Path(__file__).parent / "main_data.csv"
    df = pd.read_csv(path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df


def style_axes(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_axisbelow(True)


def highlight_bar(ax, labels, values, highlight_idx, color, xlabel, ylabel, title):
    colors = [GREY] * len(values)
    colors[highlight_idx] = color
    bars = ax.bar(labels, values, color=colors)
    ax.bar_label(bars, fmt="%.0f", padding=3)
    ax.set_ylim(0, max(values) * 1.15)
    ax.set_title(title, pad=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    style_axes(ax)


main_df = load_data()

#  Sidebar (filter) 
st.sidebar.header("Filter Data")
min_date, max_date = main_df["dteday"].min().date(), main_df["dteday"].max().date()
date_range = st.sidebar.date_input(
    "Rentang tanggal", value=(min_date, max_date), min_value=min_date, max_value=max_date
)
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

day_types = st.sidebar.multiselect(
    "Jenis hari", options=["Hari Kerja", "Libur"], default=["Hari Kerja", "Libur"]
)

df = main_df[
    (main_df["dteday"].dt.date >= start_date)
    & (main_df["dteday"].dt.date <= end_date)
    & (main_df["day_type"].isin(day_types))
]

st.title("🚲 Bike Sharing Dashboard")
st.caption("Analisis penyewaan sepeda 2011-2012 · Dataset: Bike Sharing (Capital Bikeshare)")

if df.empty:
    st.warning("Tidak ada data untuk filter yang dipilih. Ubah rentang tanggal atau jenis hari.")
    st.stop()

# Data harian (satu baris per tanggal) untuk analisis cuaca & suhu
daily_df = df.drop_duplicates("dteday")[["dteday", "weather_daily", "temp_celsius_daily", "cnt_daily"]]

#  Ringkasan 
hourly_avg = df.groupby("hr")["cnt"].mean()
c1, c2, c3 = st.columns(3)
c1.metric("Total Penyewaan", f"{df['cnt'].sum():,.0f}")
c2.metric("Rata-rata per Hari", f"{daily_df['cnt_daily'].mean():,.0f}")
c3.metric("Jam Tersibuk", f"{hourly_avg.idxmax():02d}:00")

#  Tab 
tab1, tab2, tab3 = st.tabs(["Pengaruh Cuaca", "Pola Per Jam", "Analisis Lanjutan (Binning)"])

# Pertanyaan 1 
with tab1:
    st.subheader("Bagaimana pengaruh cuaca terhadap penyewaan harian?")
    avg_weather = (
        daily_df.groupby("weather_daily")["cnt_daily"].mean().reindex(WEATHER_ORDER).dropna()
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    highlight_bar(
        ax, avg_weather.index, avg_weather.values, avg_weather.values.argmin(), RED,
        "Kondisi Cuaca", "Rata-rata Penyewaan per Hari",
        "Rata-rata Penyewaan Sepeda Harian Berdasarkan Kondisi Cuaca",
    )
    st.pyplot(fig)
    if len(avg_weather) > 1:
        drop = (1 - avg_weather.min() / avg_weather.max()) * 100
        st.info(
            f"Penyewaan terendah terjadi saat **{avg_weather.idxmin()}** "
            f"({avg_weather.min():,.0f} sepeda/hari), sekitar **{drop:.0f}%** lebih rendah "
            f"dari kondisi **{avg_weather.idxmax()}**."
        )
    st.caption("Catatan: kategori Hujan/Salju Ringan hanya mencakup sedikit hari (21 hari pada data penuh), "
               "sehingga perlu ditafsirkan dengan hati-hati.")

# Pertanyaan 2
with tab2:
    st.subheader("Pada jam berapa penyewaan memuncak?")
    hour_pivot = df.groupby(["hr", "day_type"])["cnt"].mean().unstack()
    fig, ax = plt.subplots(figsize=(11, 5))
    for col, color in (("Hari Kerja", BLUE), ("Libur", ORANGE)):
        if col in hour_pivot.columns:
            series = hour_pivot[col].dropna()
            ax.plot(series.index, series.values, marker="o", color=color, label=col)
            peak = series.idxmax()
            ax.annotate(
                f"Puncak {peak}:00 ({series.max():.0f})",
                xy=(peak, series.max()), xytext=(peak + 1, series.max() + 40),
                arrowprops=dict(arrowstyle="->", color=color), color=color,
            )
    ax.set_xticks(range(0, 24))
    ax.set_ylim(0, hour_pivot.max().max() * 1.25)
    ax.set_title("Rata-rata Penyewaan Sepeda per Jam: Hari Kerja vs Libur")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.legend()
    style_axes(ax)
    st.pyplot(fig)
    st.info("Hari kerja memiliki dua puncak (jam berangkat ~08.00 dan pulang 17.00-18.00), "
            "sedangkan hari libur memuncak di siang hari dengan pola lebih landai.")

# Analisis lanjutan
with tab3:
    st.subheader("Manual Grouping / Binning")
    col_a, col_b = st.columns(2)

    with col_a:
        seg = pd.cut(df["hr"], bins=[-1, 5, 10, 15, 19, 23], labels=SEGMENT_LABELS)
        segment_avg = df.groupby(seg, observed=True)["cnt"].mean()
        fig, ax = plt.subplots(figsize=(8, 5))
        highlight_bar(
            ax, segment_avg.index.astype(str), segment_avg.values, segment_avg.values.argmax(), BLUE,
            "Segmen Waktu", "Rata-rata Penyewaan per Jam", "Penyewaan per Segmen Waktu",
        )
        plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
        st.pyplot(fig)

    with col_b:
        temp_cat = pd.cut(daily_df["temp_celsius_daily"], bins=[-10, 10, 20, 30, 40], labels=TEMP_LABELS)
        temp_avg = daily_df.groupby(temp_cat, observed=True)["cnt_daily"].mean()
        fig, ax = plt.subplots(figsize=(8, 5))
        highlight_bar(
            ax, temp_avg.index.astype(str), temp_avg.values, temp_avg.values.argmax(), GREEN,
            "Kategori Suhu", "Rata-rata Penyewaan per Hari", "Penyewaan per Kategori Suhu",
        )
        plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
        st.pyplot(fig)

    st.info("Sore hari (16-19) adalah segmen tersibuk, dan suhu hangat (20-30°C) menghasilkan penyewaan "
            "harian tertinggi. Kategori Panas (>30°C) hanya mencakup sedikit hari, jadi interpretasikan hati-hati.")

st.caption("Dibuat oleh Nugraheni Dwi Ayu Putri")
