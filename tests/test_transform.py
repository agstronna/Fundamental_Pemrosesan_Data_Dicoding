import sys
import os
import unittest
import pandas as pd

# Menambahkan folder utama 'E:/Fundamental' ke dalam sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.transform import clean_product_data  # Pastikan fungsi ini benar-benar ada

class TestTransform(unittest.TestCase):
    """Unit test untuk fungsi clean_product_data di utils/transform.py"""

    def test_clean_product_data(self):
        """Test: Membersihkan dan mentransformasi data produk dengan benar."""
        # Data dummy produk
        products = [
            {'title': 'Product 1', 'price': '10000', 'rating': '4.5', 'colors': '3', 'size': 'M', 'gender': 'Men'},
            {'title': 'Product 2', 'price': '20000', 'rating': '5.0', 'colors': '3', 'size': 'L', 'gender': 'Women'}
        ]
        
        # Panggil fungsi yang akan diuji
        cleaned_df = clean_product_data(products)
        
        # Validasi jumlah baris
        self.assertEqual(len(cleaned_df), 2)
        
        # Validasi kolom-kolom penting ada
        expected_columns = ['price', 'rating', 'timestamp']
        for col in expected_columns:
            self.assertIn(col, cleaned_df.columns)
        
        # Validasi isi data
        self.assertTrue((cleaned_df['price'] > 0).all())
        self.assertTrue((cleaned_df['rating'] > 0).all())

    def test_unknown_product(self):
        """Test: Produk dengan price tidak valid harus dibuang."""
        products = [
            {'title': 'Unknown Product', 'price': 'unknown', 'rating': '4.5', 'colors': '5', 'size': 'M', 'gender': 'Men'}
        ]
        
        cleaned_df = clean_product_data(products)
        
        # Karena price invalid, data harus kosong
        self.assertEqual(len(cleaned_df), 0)

if __name__ == '__main__':
    unittest.main()