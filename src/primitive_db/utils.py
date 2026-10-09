'''Для вспомогательных функций (например, работа с файлами)'''
import json
import os

FILE_NAME = 'db_meta.json'

def load_metadata(filepath):
    '''загружает данные из json файла'''
    full_path = os.path.join(filepath, FILE_NAME)
    try:
        with open(full_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_metadata(filepath, data):
    '''Сохраняет переданные данные в JSON-файл'''
    full_path = os.path.join(filepath, FILE_NAME)
    with open(full_path, 'w') as f:
        json.dump(data, f)

def load_table_data(table_name):
    '''Возвращает всю таблицу в виде [{столбец_1: значние, столбец_2:значние ...}
                                       {столбец_1: значение, столбец_2:значние}]'''
    full_path = os.path.join('data/', f'{table_name}.json')
    try:
        with open(full_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_table_data(table_name, data):
    '''Сохраняет данные в таблицу'''
    os.makedirs('data', exist_ok=True)
    full_path = os.path.join('data/', f'{table_name}.json')
    with open(full_path, 'w') as f:
        json.dump(data, f)