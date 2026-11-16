# Proyek Analisis Data: Bike Sharing Dataset 🚲

Dashboard interaktif untuk menganalisis penyewaan sepeda (2011-2012).

**Pertanyaan bisnis**
1. Bagaimana pengaruh kondisi cuaca terhadap rata-rata penyewaan sepeda harian, dan di cuaca mana penyewaan paling rendah?
2. Pada jam berapa penyewaan memuncak di hari kerja dibandingkan hari libur?

Analisis lanjutan: Manual Grouping / Binning (segmen waktu & kategori suhu).

## Struktur Direktori
```
submission
├───dashboard
│   ├───main_data.csv
│   └───dashboard.py
├───data
│   ├───day.csv
│   └───hour.csv
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.11
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run Streamlit App
```
cd dashboard
streamlit run dashboard.py
```

Dashboard online: lihat `url.txt`.
