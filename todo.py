import os, re
import sqlite3
import fire
import sys
from datetime import datetime
from tabulate import tabulate
from termcolor import colored

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')
conn = sqlite3.connect(DEFAULT_PATH)
cur = conn.cursor()

sql = """
  CREATE TABLE IF NOT EXISTS todos(
    id INTEGER PRIMARY KEY,
    body TEXT NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT DEFAULT "incomplete"
  )
"""



cur.execute(sql)
conn.commit()



def show_help_menu():
  os.system('cls' if os.name == 'nt' else 'clear')
  print(colored('Todo List Options:', 'green'))
  print(colored('*' * 50, 'green'))
  print(colored('1. List all todos:', 'green'))
  print(colored('\t python3 todos.py list', 'white'))
  print(colored('2. Add a new todo:', 'green'))
  print(colored('\t python3 todos.py add "My Todo Body"', 'white'))
  print(colored('3. Delete a todo:', 'green'))
  print(colored('\t python3 todos.py delete 1', 'white'))
  print(colored('4. Mark a todo complete:', 'green'))
  print(colored('\t python3 todos.py do 1', 'white'))
  print(colored('5. Mark a todo uncomplete:', 'green'))
  print(colored('\t python3 todos.py undo 1', 'white'))
  print(colored('-' * 100, 'green'))



def add():
  print(colored('what would you like to add?', 'magenta'))
  body = input()
  print(colored('Adding Todo:', 'green'), body)
  sql = """
    INSERT INTO todos (body, due_date) VALUES (?,?)
  """
  cur.execute(sql, (body, datetime.now()))
  conn.commit()


def do():
#   print(colored('Adding Todo:', 'green'), body)
  print('Id: ', end='')
  id = input()
  sql = """
    UPDATE todos
    SET status = 'completed'
    Where id = (?)
  """
  cur.execute(sql, (id,))
  conn.commit()  
  


def undo():
  # print(colored('Adding Todo:', 'green'), body)
  print('Id: ', end='')
  id = input()
  sql = """
    UPDATE todos
    SET status = 'incomplete'
    Where id = (?)
  """
  cur.execute(sql, (id,))
  conn.commit()   



def delete():
  # print(colored('Adding Todo:', 'green'), body)
  print('Id: ')
  id = input()
  sql = """
    DELETE FROM todos
    WHERE id = (?);
  """
  cur.execute(sql, (id,))
  conn.commit()  

# def change_title(body):
#   sql = """
#     UPDATE todos
#     SET body = (?)
#     Where id = (?)
#   """
#   cur.execute(sql, (id,), body,)
#   conn.commit()  


def show_list(status = None):
  if status == None:
    sql = """
      SELECT * FROM todos
      ORDER BY status DESC
    """
    cur.execute(sql)
    results = cur.fetchall()



  if status == "done":
    sql = """
      SELECT * FROM todos
      WHERE status LIKE ?
    """
    cur.execute(sql, ("completed",))
    results = cur.fetchall()
    
  if status == "undone":
    sql = """
      SELECT * FROM todos
      WHERE status LIKE ?
    """
    cur.execute(sql, ("incomplete",))
    results = cur.fetchall()



  print(colored('Todo List:', 'green'), len(results), 'todos')
  data_table = []
  for row in results:
    data_table = (*data_table,row)
  print(colored(tabulate(data_table, ['id', 'task', 'date', 'status'], tablefmt='fancy_grid'),'magenta'))


if __name__  == '__main__':
  try:

    # arg1 = sys.argv[1]
    # if arg1 == '--help':
    #     show_help_menu()
    # else:
    #     fire.Fire({
    #       'do': do,
    #       'add': add,
    #       'undo': undo,
    #       'delete': delete,
    #       'list': show_list,
    #       # 'change': change_title,
    #   })
    while True:
      print('What do you want to do?')
      i_want_to = input()
      if i_want_to == 'help' or i_want_to =='h':
        show_help_menu()
      elif i_want_to == 'list' or i_want_to =='l':
        show_list()
      elif i_want_to == 'do' or i_want_to =='d':
        do()
      elif i_want_to == 'undo' or i_want_to =='u':
        undo()  
      elif i_want_to == 'add' or i_want_to =='a':
        add()  
      elif i_want_to == 'delete' or i_want_to =='de':
        delete()  
          
      
      elif i_want_to == 'quit' or i_want_to =='q':
        break

  except IndexError:
      show_help_menu()
      sys.exit(1)