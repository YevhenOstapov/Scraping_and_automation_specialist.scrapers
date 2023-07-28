import json
import os
from json import JSONDecodeError

from conf import INTERMEDIATE_FILE


def clear_intermediate_file():
    with open(INTERMEDIATE_FILE, 'w'):
        pass


def create_if_not_exists():
    if not os.path.exists(INTERMEDIATE_FILE):
        file = open(INTERMEDIATE_FILE, 'w+')
        file.close()


def read_data() -> dict:
    create_if_not_exists()
    with open(INTERMEDIATE_FILE) as json_file:
        try:
            return json.load(json_file)
        except JSONDecodeError:
            return {'products': [], 'products_count': 0}


def save_data_to_intermediate_file(product_data: dict) -> None:
    json_data = read_data()
    with open(INTERMEDIATE_FILE, 'w') as json_file:
        json_data['products'].append(product_data)
        json_data['products_count'] += 1
        json.dump(json_data, json_file, indent=4)

