import re
import threading
import time
from typing import List, Optional
from urllib.parse import urlparse

from utils import save_data_to_intermediate_file
from conf import STYLEINFORM_USERNAME, STYLEINFORM_PASSWORD

from .base import ScraperBase


class StyleInForm(ScraperBase):
    DOMAIN = 'styleinform.com'
    BASE_URL = 'https://styleinform.com'
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.username = username if username is not None else STYLEINFORM_USERNAME
        self.password = password if password is not None else STYLEINFORM_PASSWORD

    @property
    def all_products_count(self):
        return len(self.all_products_urls())

    def login(self) -> dict:
        path = '/my-account/'
        sel = self.get(path)

        login_nonce = sel.xpath('//*[@id="woocommerce-login-nonce"]/@value').get()
        if not login_nonce:
            raise Exception('Login nonce input not found')

        payload = {'username': self.username, 'password': self.password, 'woocommerce-login-nonce': login_nonce,
                   '_wp_http_referer': '/my-account/', 'login': 'Log+in'}

        response = self.post(path + '?action=login', payload=payload, allow_redirects=False)
        if not response.cookies:
            print('login method did not work correctly, the request did not return cookies')

        for cookie in response.cookies:
            self.session.cookies.set_cookie(cookie)

        return response.cookies.get_dict()

    def all_products_urls(self) -> List[str]:
        path = '/product-sitemap.xml'
        sel = self.get(path, selector_params={'type': 'xml'})
        sel.remove_namespaces()
        return [i for i in sel.xpath('//loc/text()').getall() if urlparse(i).path.startswith('/product')]

    def parse_product(self, url: str) -> dict:
        sel = self.get(urlparse(url).path)
        data = dict()
        data['product_sku'] = sel.xpath('//div[@class="product_meta"]/span[@class="sku_wrapper"]/span/text()').get()
        inv_texts = sel.xpath('//p[contains(@class, "stock")]/text()').getall()
        other_texts = []
        for text in inv_texts:
            qty = re.findall(r'\d+ left in stock', text)
            if qty:
                data['inventory_qty'] = re.findall(r'\d+', qty[0])[0]
                if 'More stock arriving:' in qty[0]:
                    other_texts.append('More stock arriving:')
            else:
                other_texts.append(text)

        if other_texts:
            data['inventory_text'] = ''.join(other_texts)
        return data

    def parse_all_products(self, slice_range: Optional[int] = None):
        products_urls = self.all_products_urls()
        if products_urls and slice_range and 0 < slice_range < len(products_urls):
            products_urls = products_urls[:slice_range]

        login_data = self.login()
        if not login_data:
            print('Try login again...')
            self.login()

        for url in products_urls:
            product_data = self.parse_product(url)
            if product_data:
                thread = threading.Thread(target=save_data_to_intermediate_file,
                                          daemon=True, args=(product_data,))
                thread.start()
            else:
                print('product url: %s not parsed!'.format(url))
        time.sleep(15)
