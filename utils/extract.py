import requests
from bs4 import BeautifulSoup


def fetch_product_data(url: str) -> list:
    """Mengambil data produk dari halaman koleksi."""

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except requests.exceptions.RequestException as error:
        raise Exception(f"Error mengakses URL {url}: {error}")

    try:
        soup = BeautifulSoup(res.text, 'html.parser')
        product_list = []

        cards = soup.find_all('div', class_='collection-card')
        for card in cards:
            title = card.find('h3', class_='product-title')
            price = card.find('div', class_='price-container')
            rating = card.find('p', string=lambda t: t and 'Rating' in t)
            colors = card.find('p', string=lambda t: t and 'Colors' in t)
            size = card.find('p', string=lambda t: t and 'Size' in t)
            gender = card.find('p', string=lambda t: t and 'Gender' in t)

            product_info = {
                'title': title.text.strip() if title else 'Unknown Title',
                'price': price.text.strip() if price else 'Price Not Available',
                'rating': rating.text.strip() if rating else 'No Rating',
                'colors': colors.text.strip() if colors else 'No Color Info',
                'size': size.text.strip() if size else 'No Size Info',
                'gender': gender.text.strip() if gender else 'No Gender Info',
            }

            product_list.append(product_info)

        return product_list

    except Exception as error:
        raise Exception(f"Error saat parsing HTML: {error}")