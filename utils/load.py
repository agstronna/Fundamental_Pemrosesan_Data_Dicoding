import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine

def save_to_csv(data_frame, filename="products.csv"):
    """Menyimpan DataFrame ke file CSV."""
    data_frame.to_csv(filename, index=False)
    print(f"Data berhasil disimpan ke {filename}.")

def save_to_google_sheets(data_frame, spreadsheet_id, range_name):
    """Menyimpan DataFrame ke Google Sheets."""
    try:
        # Mengautentikasi menggunakan kredensial dari file JSON
        creds = Credentials.from_service_account_file('google-sheets-api.json')
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        # Mengonversi DataFrame ke list untuk input ke Google Sheets
        values = data_frame.values.tolist()
        body = {'values': values}
        
        # Mengirim data ke Google Sheets
        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        print(f"Data berhasil disimpan ke Google Sheets pada range {range_name}.")

    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan ke Google Sheets: {e}")

def load_to_postgresql(data_frame, table_name='products'):
    """Menyimpan DataFrame ke PostgreSQL database."""
    try:
        # Ganti info berikut dengan konfigurasi PostgreSQL yang sesuai
        username = 'developer'
        password = '123452025'
        host = 'localhost'
        port = '5432'
        database = 'etl_db'

        # Buat koneksi engine SQLAlchemy
        engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

        # Menyimpan DataFrame ke dalam tabel PostgreSQL (mengganti jika tabel sudah ada)
        data_frame.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data berhasil disimpan ke tabel PostgreSQL '{table_name}'.")

    except Exception as e:
        print(f"Gagal menyimpan data ke PostgreSQL: {e}")