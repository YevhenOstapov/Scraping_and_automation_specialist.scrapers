import unittest
from urllib.parse import urlparse

from scrapers import StyleInForm
from utils import read_data


class TestStyleInForm(unittest.TestCase):
    def setUp(self) -> None:
        self.scraper = StyleInForm()

    def test_all_products_urls(self):
        products_urls = self.scraper.all_products_urls()

        self.assertIsInstance(products_urls, list, msg='all_products_urls method not returned list')
        self.assertNotEqual(len(products_urls), 0, msg='all_products_urls method return empty list')

        for url in products_urls:
            self.assertIsNotNone(urlparse(url).netloc, msg='not url in list')
            self.assertIsNotNone(urlparse(url).scheme, msg='not url in list')

    def test_login(self):
        cookies = self.scraper.login()
        self.assertIsInstance(cookies, dict, msg='method login must returned dict')
        self.assertNotEqual(len(cookies.keys()), 0, msg='request to login not returned cookies dict')
        self.assertIsNotNone(self.scraper.session.cookies, msg='cookies of session after login cannot be None')

    def test_parse_all_products(self):
        self.scraper.parse_all_products(5)
        data = read_data()
        self.assertNotEqual(data['products_count'], 0, msg='wrong qty in file')
        self.assertIsNotNone(data['products'], msg='not added new data in file')

        for p_data in data['products']:
            self.assertIsInstance(p_data, dict)

            self.assertIn('product_sku', p_data.keys())

            # if p_data.get('inventory_qty') and p_data['inventory_qty'] == 0:
            #     self.assertIn('inventory_text', p_data.keys())


if __name__ == '__main__':
    unittest.main()
