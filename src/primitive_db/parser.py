'''Парсит сложные функции, такие как where и set
Превращает строки вида "age = 28 в словари {age: 28}'''

def split_conditions(texts, separator):
    '''Разделяет составное условие на простые
    На вход принимает список ['столбец', '=', 'значение,', 'столбец', '=', 'значение,']
    И возвращает список ['столбец = значение', 'столбец = значение']'''
    result = [[]]
    for token in texts:
        if token.lower() == separator:
            result.append([])
        elif separator == ',' and token.endswith(','):
            result[-1].append(token[:-1])
            result.append([])
        else:
            result[-1].append(token)

    return [' '.join(condition) for condition in result]

def parse_clause(texts):
    '''Переделывает список условий в словарь
    ['age = 28', 'name = "Anna"'] -> {'age': 28, 'name': 'Anna'}
    Возвращает словарь или None при ошибке'''
    result = {}
    for text in texts:
        if '=' not in text:
            print(f'Ошибка: в условии "{text}" нет знака =')
            return None

        key, value = text.split('=', 1)
        key, value = key.strip(), value.strip()
        if not key or not value:
            print(f'Ошибка: условие "{text}" записано неправильно')
            return None
        if key in result:
            print(f'Ошибка: столбец {key} указан дважды')
            return None

        value = parse_value(value)
        if value is None:
            return None
        result[key] = value

    return result

def parse_value(raw):
    '''Превращает значение из команды в значение нужного типа
    '"Sergei"' -> 'Sergei', '28' -> 28, 'true' -> True
    Возвращает None, если значение не распознано'''
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in '"\'':
        return raw[1:-1]
    if raw.lower() in ['true', 'false']:
        return raw.lower() == 'true'
    try:
        return int(raw)
    except ValueError:
        print(f'Ошибка: значение {raw} не распознано (строки пишите в кавычках)')
        return None

def parse_comp_func(tokens):
    '''Принимает список слов после имени таблицы, например
    ['set', 'age', '=', '29,', 'name', '=', '"Anna"', 'where', 'ID', '=', '2']
    Возвращает {'set': {'age': 29, 'name': 'Anna'}, 'where': {'ID': 2}},
    отсутствующая часть равна None. При ошибке возвращает None'''

    parts = {'set': None, 'where': None}
    current = None
    for token in tokens:
        word = token.lower()
        if word in parts:
            if parts[word] is not None:
                print(f'Ошибка: {word} указан дважды')
                return None
            current = word
            parts[current] = []
        elif current is None:
            print(f'Ошибка: ожидалось set или where, а получено {token}')
            return None
        else:
            parts[current].append(token)

    separators = {'set': ',', 'where': 'and'}
    result = {'set': None, 'where': None}
    for key, part in parts.items():
        if part is None:
            continue
        if not part:
            print(f'Ошибка: после {key} нет условия')
            return None

        clause = parse_clause(split_conditions(part, separators[key]))
        if clause is None:
            return None
        result[key] = clause

    return result