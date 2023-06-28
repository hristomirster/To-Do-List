import os
import time
import sqlite3
from datetime import datetime


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Проверка на операционната система и избор на подходяща команда за изчистване на екрана
def clear_console():
    if os.name == 'nt':  # за Windows
        os.system('cls')
    else:  # за Unix/Linux/Mac
        os.system('clear')


# Създаване на функций за базата sqlite3
def create_tasks_table(connection):
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks 
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    task TEXT, 
    last_update TEXT, 
    due_date_is TEXT, 
    comment TEXT)
    ''')
    connection.commit()


def add_task(connection, task):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    connection.commit()


def get_tasks(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return tasks


def update_task(connection, task_id, new_task):
    cursor = connection.cursor()
    cursor.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))
    connection.commit()


def update_last_update(connection, task_id, last_update):
    cursor = connection.cursor()
    cursor.execute("UPDATE tasks SET last_update = ? WHERE id = ?", (last_update, task_id))
    connection.commit()


def update_due_date_is(connection, task_id, due_date_is):
    cursor = connection.cursor()
    cursor.execute("UPDATE tasks SET due_date_is = ? WHERE id = ?", (due_date_is, task_id))
    connection.commit()


def update_comment(connection, task_id, comment):
    cursor = connection.cursor()
    cursor.execute("UPDATE tasks SET comment = ? WHERE id = ?", (comment, task_id))
    connection.commit()


def delete_task(connection, task_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    connection.commit()


def delete_database(connection):
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS tasks")
    connection.commit()


# Създаване на базата данни и таблицата, ако все още не съществува
db_connection = sqlite3.connect("tasks_to_do_list.db")
create_tasks_table(db_connection)


# Принтиране на листа със ТЕКУЩИ задачи:
def list_tasks():
    tasks = get_tasks(db_connection)

    #   Oтстояние в колоните
    task_index_1_len_of_string = 0
    for task in tasks:
        if len(task[1]) > task_index_1_len_of_string:
            task_index_1_len_of_string = len(task[1])

    print(f"\n{bcolors.WARNING}Списък със задачи:{bcolors.ENDC} \n")
    print(f"Id Task{' ' * (task_index_1_len_of_string - 3)}last_update due_date_is comment")
    print(f"-- {'-' * task_index_1_len_of_string} ----------- ----------- -------")
    for task in tasks:
        if task[4] != "завършен":
            print(f"{task[0]}. {task[1]}{' ' * (task_index_1_len_of_string - len(task[1]))} {task[2]}{' ' * 2}{task[3]}{' ' * 1} {task[4]}")


# Принтиране на листа със ЗАВЪРШЕНИ задачи:
def list_tasks_completed():
    tasks = get_tasks(db_connection)

    #   Oтстояние в колоните
    task_index_1_len_of_string = 0
    for task in tasks:
        if len(task[1]) > task_index_1_len_of_string:
            task_index_1_len_of_string = len(task[1])

    print(f"\n{bcolors.WARNING}Списък със ЗАВЪРШЕНИ задачи:{bcolors.ENDC} \n")
    print(f"Id Task{' ' * (task_index_1_len_of_string - 3)}last_update due_date_is comment")
    print(f"-- {'-' * task_index_1_len_of_string} ----------- ----------- -------")
    for task in tasks:
        if task[4] == "завършен":
            print(f"{task[0]}. {task[1]}{' ' * (task_index_1_len_of_string - len(task[1]))} {task[2]}{' ' * 2}{task[3]}{' ' * 1} {task[4]}")


# Тази част нах безсрамно си я откраднах от тук:
# https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters

def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


# A List of Items
items = list(range(0, 57))
l = len(items)

# Стартиране на приложението

clear_console()

print("\n   Зареждане на конзолно приложение за задачи (To-Do list) \n")
printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
for i, item in enumerate(items):
    # Do stuff...
    time.sleep(0.01)
    # Update Progress Bar
    printProgressBar(i + 1, l, prefix=' Loading:', suffix='Complete', length=50)

clear_console()
#########################################################################

task_list = []

# Основен цикъл на приложението
while True:
    # Изчистване на конзолата
    clear_console()

    # datetime object containing current date and time
    now = datetime.now()
    # print("now =", now)

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    # Принтиране на основното меню
    print(f"    Дата: {dt_string}")
    print("     \n Това е конзолно приложение за задачи.\n")
    print("     Основно меню:\n")
    print("     1. Добави задача")
    print("     1.1 Промени задача(редактиране)")
    print("     1.2 Промени кога е ъпдеитната задача(last_update)")
    print("     1.3 Промени срока за изпълнение на задача(редактиране)")
    print("     1.4 Промени коментар на задача(редактиране)")
    print("     2. Премахни задача")
    print("     3. Покажи списъка със ЗАВЪРШЕНИ задачи")
    print("     4. Изтриване на текущата база данни със задачи!")
    print("     5. Изход")

    if len(get_tasks(db_connection)) == 0:
        print("\n Списъка със задачи е празен.")
    else:
        list_tasks()  # Принтиране на текущите задачи

    choise = input(f"\n      {bcolors.BOLD}Очакваме Вашия избор (1-5):{bcolors.ENDC} ")

    if choise == "1":
        # list_tasks() #  Принтиране на текущите задачи

        new_task = input("\n Въведете нова задача (или 'exit' за връщане към основното меню): ")

        if new_task.lower() == "exit":
            print("\n Връщане към основното меню...")
            time.sleep(2)
            continue

        print("\n Задачата е добавена успешно. Връщане към основното меню...")

        # Добавяне на новата задача в базата данни
        add_task(db_connection, new_task)

        time.sleep(2)

    elif choise == "1.1":  # Промяна на името(редактиране) на текуща задача

        # list_tasks()  # Принтиране на текущите задачи

        # Въвеждане на номер на задача за модификация
        task_id = input(
            "\n Въведете номер на задачата, която искате да модифицирате(или 'exit' за връщане към основното меню): ")

        if task_id.lower() == "exit":
            print("\n Връщане към основното меню...")
            time.sleep(2)
            continue
        new_task = input("\n Въведете новото съдържание на задачата: ")
        update_task(db_connection, task_id, new_task)
        print("\n Задачата е модифицирана успешно. Връщане към основното меню...")

        time.sleep(3)

    elif choise == "1.2":  # Промяна дата последна модификация ->  update_last_update()
        # list_tasks()  # Принтиране на текущите задачи

        task_id = input(
            "\n Въведете номер на задачата, която искате да модифицирате(или 'exit' за връщане към основното меню): ")
        if task_id.lower() == "exit":
            print("\n Връщане към основното меню...")
            time.sleep(2)
            continue
        new_task = input("\n Въведете новото съдържание за последна модификация: ")
        update_last_update(db_connection, task_id, new_task)
        print("\n Задачата е модифицирана успешно. Връщане към основното меню...")

        time.sleep(3)

    elif choise == "1.3":  # Промяна срока за изпълнение на задача ->  update_due_date_is()
        # list_tasks()  # Принтиране на текущите задачи

        task_id = input(
            "\n Въведете номер на задачата, която искате да модифицирате(или 'exit' за връщане към основното меню): ")
        if task_id.lower() == "exit":
            print("\n Връщане към основното меню...")
            time.sleep(2)
            continue
        new_task = input("\n Въведете новото съдържание за краен срок на изпълнение: ")
        update_due_date_is(db_connection, task_id, new_task)
        print("\n Задачата е модифицирана успешно. Връщане към основното меню...")

        time.sleep(3)

    elif choise == "1.4":  # Промяна коментар на задача ->  update_comment()
        # list_tasks()  # Принтиране на текущите задачи

        task_id = input(
            "\n Въведете номер на задачата, която искате да коментирате(или 'exit' за връщане към основното меню): ")
        if task_id.lower() == "exit":
            print("\n Връщане към основното меню...")
            time.sleep(2)
            continue
        new_task = input("\n Въведете новото съдържание за коментар: ")
        update_comment(db_connection, task_id, new_task)
        print("\n Задачата е модифицирана успешно. Връщане към основното меню...")

        time.sleep(3)


    elif choise == "2":  # Премахване на задача от базата
        # list_tasks()  # Принтиране на текущите задачи

        # Въвеждане на команда за изтриване на задача
        command = input(
            "\n Въведете номер(Id) на задачата, която искате да изтриете (или 'exit' за връщане към основното меню): ")
        if command.lower() == "exit":
            continue

        try:
            task_id = int(command)
            delete_task(db_connection, task_id)
            print("\nЗадачата е изтрита успешно. Връщанре в основното меню...")
        except ValueError:
            # print("Невалиден номер на задача. Моля, опитайте отново.")
            input("\n Невалиден номер на задача. Натиснете 'Enter' за да се върнете в основното меню: ")

        # Забавяне между циклите
        time.sleep(2)


    elif choise == "3":  # Показване на задачите
        if len(get_tasks(db_connection)) == 0:
            print("\n Списъка със задачи е празен.")
        else:
            list_tasks_completed()  # Принтиране на текущите задачи

        print("\n Натисни 'Enter' за да се върнеш към основното меню")
        input()

    elif choise == "4":  # Изтриване на текyщата база данни
        print()
        print(f"     {bcolors.FAIL}####################################################{bcolors.ENDC}")
        print(f"     {bcolors.FAIL}############### !!! ВНИМАНИЕ !!! ###################{bcolors.ENDC}")
        print(f"     {bcolors.FAIL}####################################################{bcolors.ENDC}")
        print()
        # Изтриване на базата данни
        confirm = input(f"Сигурни ли сте, че искате да изтриете базата данни? {bcolors.FAIL}yes(y){bcolors.ENDC}/{bcolors.OKGREEN}no(n){bcolors.ENDC}: ")
        if confirm.lower() == "yes" or confirm.lower() == "y":
            print()
            printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
            for i, item in enumerate(items):
                # Do stuff...
                time.sleep(0.05)
                # Update Progress Bar
                printProgressBar(i + 1, l, prefix='Dleteting DB:', suffix='Complete', length=50)

            delete_database(db_connection)
            # print("\n Базата данни е изтрита успешно, връшане към основното меню...")
            print("За да създадете нова таблица в базата данни трябва да рестартирате приложениео.")

            # Очакваме Вашия избор (1-5):
            clear_console()
            timer = 10
            while timer > 0:
                print(f"Приложението ще се изключи автоматично след: {timer} ...")
                timer -= 1
                time.sleep(1)
                clear_console()
            exit()


    elif choise == "5":
        clear_console()
        exit()

    # elif choise == "6": #  restart the program


    else:
        print("Невалиден избор, натиснете 'Enter' за да се върнете в основното меню...")
        input()

# Създаване на exe
# "C:\Users\vasilev\AppData\Roaming\Python\Python311\Scripts\pyinstaller.exe" --onefile "G:\My Drive\GitHub\To-Do-List\console_to_do_list.py" --icon="G:\My Drive\GitHub\To-Do-List\console_to_do_list_app\Untitled.ico"

# cd "G:\My Drive\GitHub\To-Do-List_Prod\"
# pyinstaller.exe --onefile "G:\My Drive\GitHub\To-Do-List_Prod\console_to_do_list.py" --icon="Untitled.ico"
