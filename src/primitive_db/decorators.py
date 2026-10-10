'''Декораторы проекта'''
from functools import wraps
import time


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

def confirm_action(action_name):
    '''Фабрика декораторов: спрашивает подтверждение перед опасной операцией
    Если пользователь ввёл не "y", функция не выполняется и возвращается None'''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(f'Вы уверены, что хотите выполнить "{action_name}"? '
                           '[y/n]: ')
            if answer.strip().lower() != 'y':
                print('Операция отменена')
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

def log_time(func):
    '''Замеряет время работы функции'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        stop_time = time.monotonic()
        elapsed = stop_time - start_time
        print(f'Функция {func.__name__} выполнилась за {elapsed:.3f} секунд')
        return result
    return wrapper