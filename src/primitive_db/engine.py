'''Этот файл будет отвечать за запуск, игровой цикл и парсинг команд.'''

import prompt
from primitive_db import utils, core
import shlex


def welcome():
    print("""<command> exit - выйти из программы
<command> help - справочная информация""")
    comand = prompt.string("Введите команду: ")
    return shlex.split(comand)

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

def run():
   print_help()

   while True:
      meta = utils.load_metadata('./')
      user_input = prompt.string('Введите команду: ')
      args = shlex.split(user_input)

      if not args:
         continue

      comand = args[0].lower()

      match comand:
         case 'create_table':
            if len(args) < 2:
               print(f'Команда введена неправильно')
               continue

            table_name = args[1]
            columns = {}
            for col in args[2:]:
               col_name, col_type = col.split(':')
               columns[col_name] = col_type

            new_meta = core.create_table(metadata=meta, table_name=table_name, columns=columns)
            meta.update(new_meta)
            utils.save_metadata('.', meta)

            if new_meta:
               print(f'Таблица {table_name} создана')
            else:
               print(f'Таблица {table_name} не создана')

         case 'list_tables':
            print(meta)

         case 'drop_table':
            if len(args) != 2:
               print(f'Команда введена неправильно')
               continue
            table_name = args[1]
            meta.update(core.drop_table(meta, table_name=table_name))
            utils.save_metadata('.', meta)
            print(f'Таблица {table_name} удалена')

         case 'help':
            print_help()
         case 'exit':
            break
         case _:
            print(f'Функции "{comand}" нет. Попробуйте снова.')