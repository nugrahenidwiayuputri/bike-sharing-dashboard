# Proyek Analisis Data: Bike Sharing Dataset 🚲

Dashboard interaktif untuk menganalisis penyewaan sepeda (2011–2012) menggunakan Streamlit.

## Pertanyaan Bisnis

1. Bagaimana pengaruh kondisi cuaca terhadap rata-rata penyewaan sepeda harian, dan pada kondisi cuaca mana penyewaan paling rendah?
2. Pada jam berapa penyewaan memuncak di hari kerja dibandingkan hari libur?

**Analisis lanjutan:** Manual Grouping / Binning (segmen waktu dan kategori suhu).

## Struktur Direktori

```text
submission
├── dashboard
│   ├── main_data.csv
│   └── dashboard.py
├── data
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Setup Environment - Anaconda

```bash
conda create --name main-ds python=3.11
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

```bash
python -m venv venv
```

Aktivasi environment:

```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

Instalasi dependencies:

```bash
pip install -r requirements.txt
```

## Run Streamlit App

```bash
cd dashboard
streamlit run dashboard.py
```

## Dashboard Online

Lihat tautan dashboard pada file `url.txt`."# bike-sharing-dashboard" 
