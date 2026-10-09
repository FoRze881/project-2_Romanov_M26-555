'''Декораторы проекта'''
from functools import wraps


def handle_db_errors(func):
    '''Перехватывает ошибки при работе с данными, чтобы программа не падала
    При ошибке выводит сообщение и возвращает None'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            print(f'Ошибка: таблица или столбец {e} не найдены')
        except FileNotFoundError as e:
            print(f'Ошибка: файл {e.filename} не найден')
        except ValueError as e:
            print(f'Ошибка валидации: {e}')
        return None
    return wrapper