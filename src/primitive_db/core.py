'''Здесь будет основная логика работы с таблицами и данными.'''
def create_table(metadata, table_name, columns):
    '''Проверяет все условия для создания таблицы и создает ее, если можно'''
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    types = ['int', 'str', 'bool']
    for _, col_type in columns.items():
        if col_type not in types:
            print(f'Ошибка: неправильный тип данных {col_type}. Допустимые значения {types}')
            return metadata
    metadata = {table_name: {'ID': 'int', **columns}}

    return metadata

def drop_table(metadata, table_name):
    '''Удаляет таблицу'''
    if table_name not in metadata:
        print(f'Ошибка: таблицы {table_name} не существует, поэтому нельзя удалить')
        return metadata

    _ = metadata.pop(table_name, None)
    return metadata