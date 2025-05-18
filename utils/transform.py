import pandas as pd
import numpy as np
from datetime import datetime
import warnings

# Menonaktifkan peringatan FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# Mengaktifkan pengaturan baru sesuai peringatan
pd.set_option('future.no_silent_downcasting', True)

def clean_product_data(product_list):
    try:
        data_frame = pd.DataFrame(product_list)
        
        # Validasi kolom penting ada
        required_columns = ['title', 'price', 'rating', 'colors', 'size', 'gender']
        for col in required_columns:
            if col not in data_frame.columns:
                raise KeyError(f"Kolom '{col}' tidak ditemukan dalam data")

        # Langkah pembersihan data
        data_frame = data_frame[data_frame['title'].str.lower() != 'unknown product']

        data_frame['price'] = data_frame['price'].replace(r'[^\d.]', '', regex=True).replace('', np.nan)
        data_frame.dropna(subset=['price'], inplace=True)
        data_frame['price'] = data_frame['price'].astype(float) * 16000

        data_frame['rating'] = data_frame['rating'].replace(r'[^0-9.]', '', regex=True).replace('', np.nan)
        data_frame.dropna(subset=['rating'], inplace=True)
        data_frame['rating'] = data_frame['rating'].astype(float)

        data_frame['colors'] = data_frame['colors'].replace(r'\D', '', regex=True).replace('', np.nan)
        data_frame.dropna(subset=['colors'], inplace=True)
        data_frame['colors'] = data_frame['colors'].astype(int)

        data_frame['size'] = data_frame['size'].replace(r'Size:\s*', '', regex=True)
        data_frame['gender'] = data_frame['gender'].replace(r'Gender:\s*', '', regex=True)

        data_frame.drop_duplicates(inplace=True)
        data_frame.dropna(inplace=True)

        data_frame['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return data_frame

    except Exception as e:
        print(f"Terjadi kesalahan saat membersihkan data: {e}")
        return pd.DataFrame()  # kembalikan dataframe kosong jika gagal