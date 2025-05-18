import sys
import os

# Menambahkan folder utama 'E:/Fundamental' ke dalam sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from utils.extract import fetch_product_data  # Ganti 'scrape_main' dengan 'fetch_product_data'

class TestExtract(unittest.TestCase):

    @patch('utils.extract.requests.get')
    def test_fetch_product_data_success(self, mock_get):
        """Test untuk fungsi fetch_product_data (berhasil)"""
        # Arrange
        url = "https://fashion-studio.dicoding.dev/"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <div class="collection-card">
                    <h3 class="product-title">Test Product</h3>
                    <div class="price-container">$10</div>
                    <p>Rating: 5 stars</p>
                    <p>Colors: Red, Blue</p>
                    <p>Size: M, L</p>
                    <p>Gender: Unisex</p>
                </div>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        # Act
        result = fetch_product_data(url)

        # Assert
        self.assertIsInstance(result, list)  # Memastikan hasil adalah list
        self.assertGreater(len(result), 0)  # Memastikan ada produk yang ditemukan
        self.assertIn('title', result[0])  # Memastikan ada field 'title' pada produk
        self.assertEqual(result[0]['title'], 'Test Product')  # Memastikan judul produk benar

    @patch('utils.extract.requests.get')
    def test_fetch_product_data_failure(self, mock_get):
        """Test untuk fungsi fetch_product_data (gagal)"""
        # Arrange
        url = "https://fashion-studio.dicoding.dev/"
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Client Error")  # Simulasikan error
        mock_get.return_value = mock_response

        # Act & Assert
        with self.assertRaises(Exception) as context:
            fetch_product_data(url)
        
        # Memastikan pesan error sesuai dengan yang diharapkan
        self.assertEqual(str(context.exception), '404 Client Error')

if __name__ == '__main__':
    unittest.main()