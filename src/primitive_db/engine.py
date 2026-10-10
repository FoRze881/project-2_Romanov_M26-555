'''Этот файл будет отвечать за запуск, игровой цикл и парсинг команд.'''

import shlex

import prettytable
import prompt

from primitive_db import core, parser, utils


def print_help():
   """Prints the help message for the current mode."""
   
   print("\n***Процесс работы с таблицей***")
   print("Функции:")
   print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
   print("<command> list_tables - показать список всех таблиц")
   print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
   print("\nОбщие команды:")
   print("<command> exit - выход из программы")
   print("<command> help - справочная информация\n") 

   print('***Операции с данными***')

   print('Функции:')
   print('<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...)'
   ' - создать запись.')
   print('<command> select from <имя_таблицы> where <столбец> = <значение> - ' \
   'прочитать записи по условию.')
   print('<command> select from <имя_таблицы> - прочитать все записи.')
   print('<command> update <имя_таблицы> set <столбец1> = <новое_значение1> ' \
   'where <столбец_условия> = <значение_условия> - обновить запись.')
   print('<command> delete from <имя_таблицы> where <столбец> = <значение> - ' \
   'удалить запись.')
   print('<command> info <имя_таблицы> - вывести информацию о таблице.')
   print('<command> exit - выход из программы')
   print('<command> help- справочная информация')

def check_clause(metadata, table_name, clause):
   '''Проверяет, что столбцы из clause есть в таблице и типы значений совпадают
   Возвращает True/False для проверки в if'''
   meta = metadata.get(table_name, None)
   if meta is None:
      return False

   for column, value in clause.items():
      if column not in meta:
         print(f'Ошибка: столбца {column} нет в таблице {table_name}')
         return False
      if type(value).__name__ != meta[column]:
         print(f'Ошибка: значение {value} для {column} должно быть {meta[column]}')
         return False
   return True

def print_table(rows, columns):
   '''Выводит список словарей в виде таблицы
   columns - порядок столбцов, например ['ID', 'age', 'name']'''
   view = prettytable.PrettyTable()
   view.field_names = columns
   for row in rows:
      view.add_row([row[column] for column in columns])
   print(view)


def run():
   print_help()

   while True:
      meta = utils.load_metadata('./')
      user_input = prompt.string('Введите команду: ')
      args = shlex.split(user_input, posix=False)

      if not args:
         continue

      comand = args[0].lower()

      match comand:
         case 'create_table':
            if len(args) < 2:
               print('Команда введена неправильно')
               continue

            table_name = args[1]
            columns = {}
            for col in args[2:]:
               col_name, col_type = col.split(':')
               columns[col_name] = col_type

            new_meta = core.create_table(metadata=meta, 
                                         table_name=table_name, 
                                         columns=columns)
            if new_meta is not None:
               meta.update(new_meta)
               utils.save_metadata('.', meta)
               print(f'Таблица {table_name} создана')

            else:
               print(f'Таблица {table_name} не создана')

         case 'list_tables':
            print(meta)

         case 'drop_table':
            if len(args) != 2:
               print('Команда введена неправильно')
               continue
            table_name = args[1]
            if table_name not in meta:
               print(f'Ошибка: таблицы {table_name} нет в базе данных')
               continue
            new_meta = core.drop_table(meta, table_name=table_name)
            if new_meta is None:
               print(f'Ошибка: таблицы {table_name} не существует, '
                     f'поэтому нельзя удалить')
            else:
               meta.update(new_meta)
               utils.save_metadata('.', meta)
               print(f'Таблица {table_name} удалена')

         case 'insert':
            if len(args) <= 4:
               print('Ошибка: неправильный синтаксис команды')
               continue
            table = args[2]

            text = ' '.join(args[4:])
            if not (text.startswith('(') and text.endswith(')')):
               print('Ошибка: значения должны быть в скобках: values (...)')
               continue
            inner = shlex.split(text[1:-1], posix=False)
            values = parser.split_conditions(inner, ',')

            data = core.insert(meta, table, values)
            if data is None:
               continue

            utils.save_table_data(table, data)

         case 'select':
            if len(args) < 3:
               print('Ошибка: неправильный вызов функции')
               continue

            table = args[2]
            if table not in meta:
               print(f'Ошибка: таблицы {table} нет в базе данных')
               continue

            if len(args) > 3:
               where_clause = args[3:]
               parsed_clause = parser.parse_comp_func(where_clause)
               if parsed_clause is None:
                  continue

               if not check_clause(meta, table, parsed_clause['where']):
                  print(f'Ошибка: в таблице {table} нет таких столбцов')
                  continue
               new_data = core.select(utils.load_table_data(table), 
                                      parsed_clause['where'])

            else:
               new_data = core.select(utils.load_table_data(table))

            if new_data is None:
               continue

            print_table(new_data, list(meta[table].keys()))

         case 'update':
            if len(args) < 3:
               print('Ошибка: неправильный формат вызова функции')
               continue

            table_name, clause = args[1], args[2:]
            if table_name not in meta:
               print(f'Таблицы {table_name} нет в базе данных')
               continue

            parsed_clause = parser.parse_comp_func(clause)
            if parsed_clause is None:
               continue
            set_clause, where_clause = parsed_clause['set'], parsed_clause['where']

            if set_clause is None:
               print('Ошибка: не указано, что изменить (set)')
               continue
            if 'ID' in set_clause:
               print('Ошибка: нельзя изменять ID напрямую')
               continue
            if not check_clause(meta, table_name, set_clause):
               continue
            if where_clause is not None:
               if not check_clause(meta, table_name, where_clause):
                  continue

            table_data = utils.load_table_data(table_name)
            count = len(core.select(table_data, where_clause))
            new_table_data = core.update(table_data, set_clause, where_clause)
            if new_table_data is None:
               continue
            utils.save_table_data(table_name, new_table_data)
            print(f'Обновлено записей: {count}')

         case 'delete':
            if len(args) < 3 or args[1].lower() != 'from':
               print('Ошибка: неправильный формат вызова функции')
               continue

            table_name = args[2]
            if table_name not in meta:
               print(f'Таблицы {table_name} нет в базе данных')
               continue

            where_clause = None
            if len(args) > 3:
               parsed_clause = parser.parse_comp_func(args[3:])
               if parsed_clause is None:
                  continue
               if parsed_clause['set'] is not None:
                  print('Ошибка: нельзя передавать set в delete')
                  continue
               where_clause = parsed_clause['where']
               if not check_clause(meta, table_name, where_clause):
                  continue

            table_data = utils.load_table_data(table_name)
            new_table_data = core.delete(table_data, where_clause)
            if new_table_data is None:
               continue
            utils.save_table_data(table_name, new_table_data)
            print(f'Удалено записей: {len(table_data) - len(new_table_data)}')

         case 'info':
            if len(args) != 2:
               print('Ошибка: неправильный вызов команды')
               continue

            table_name = args[1]
            if table_name not in meta:
               print(f'Таблицы {table_name} нет в базе данных')
               continue
            table_meta = meta.get(table_name)
            print(f'Таблица: {table_name}')
            print(f'Столбцы: {", ".join(f"{k}:{v}" for k, v in table_meta.items())}')
            print(f'Количество записей: {len(utils.load_table_data(table_name))}')

         case 'help':
            print_help()

         case 'exit':
            break
         case _:
            print(f'Функции "{comand}" нет. Попробуйте снова.')