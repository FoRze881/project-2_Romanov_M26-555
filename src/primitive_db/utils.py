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
    with open(full_path, 'w') as file:
        json.dump(data, file)
    