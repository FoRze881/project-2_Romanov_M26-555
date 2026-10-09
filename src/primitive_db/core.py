'''Здесь будет основная логика работы с таблицами и данными.'''
from primitive_db import utils
from primitive_db import constants, parser

def create_table(metadata, table_name, columns):
    '''Проверяет все условия для создания таблицы и создает ее метаданные, если можно
    в формате {название_таблицы: {столбец_1:тип_столбца ...}}
    Возвращает либо None (если не получилось), либо metadata'''
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return None

    for _, col_type in columns.items():
        if col_type not in constants.ALLOWED_TYPES:
            print(f'Ошибка: неправильный тип данных {col_type}. ' 
                  f'Допустимые значения {constants.ALLOWED_TYPES}')
            return None
        
    metadata = {table_name: {'ID': 'int', **columns}}

    return metadata

def drop_table(metadata, table_name):
    '''Удаляет метаданные таблицы, если она есть
    Возвращает None в противном случае'''
    if table_name not in metadata:
        return None

    _ = metadata.pop(table_name, None)
    return metadata

def insert(metadata, table_name, values):
    '''Добавляет новую запись (в виде словаря) в данные таблицы
    Таблица у нас выглядит вот так: [{столбец_1:значение, столбец_2:значние}
                                      {столбец_1:значние ... }]
    Возвращаем полную таблицу вместе со вставленными данными'''
    if table_name not in metadata:
        print(f'Таблицы {table_name} нет в базе данных')
        return None

    table = metadata[table_name]
    columns = [(name, col_type) for name, col_type in table.items() if name != 'ID']

    if len(values) != len(columns):
        print(f'не все элементы таблицы {table_name} переданы')
        return None

    record = {}
    for value, (column_name, column_type) in zip(values, columns):
        value = parser.parse_value(value)
        if value is None:
            return None
        if type(value).__name__ != column_type:
            print(f'Ошибка: тип {type(value).__name__} не подходит. '
                  f'Требуется {column_type}')
            return None

        record[column_name] = value

    data = utils.load_table_data(table_name)
    new_id = max((row['ID'] for row in data), default=0) + 1
    data.append({'ID': new_id, **record})
    return data

def select(table_data, where_clause=None):
    '''Возвращает заданные данные'''
    if not where_clause:
        return table_data

    return [
        row for row in table_data
        if all(row.get(column) == value for column, value in where_clause.items())
    ]

def update(table_data, set_clause, where_clause):
    '''Обновляет записи по where_clause
    Возвращает измененный список словарей (потому что ссылки)'''
    where_table = select(table_data, where_clause)
    for row in where_table:
        row.update(set_clause)

    return table_data

def delete(table_data, where_clause):
    '''Удаляет записи по where_clause
    Возвращает новый список словарей (то есть новую таблицу)'''
    where_table = select(table_data, where_clause)
    delete_ids = {row['ID'] for row in where_table}
    data = [row for row in table_data if row['ID'] not in delete_ids]

    return data
