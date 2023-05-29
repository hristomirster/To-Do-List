import os
import time
import sqlite3



def clear_console():
    # Проверка на операционната система и избор на подходяща команда за изчистване на екрана
    if os.name == 'nt':  # за Windows
        os.system('cls')
    else:  # за Unix/Linux/Mac
        os.system('clear')

# Създаване на функция за базата sqlite3
def create_tasks_table(connection):
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)''')
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

def delete_task(connection, task_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    connection.commit()

def delete_database(connection):
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS tasks")
    connection.commit()

# Създаване на базата данни и таблицата, ако все още не съществуват
db_connection = sqlite3.connect("tasks_to_do_list.db")
create_tasks_table(db_connection)


#############
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
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
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

# A List of Items
items = list(range(0, 57))
l = len(items)

#####################

#########################################################################
clear_console()

print("\n   Зареждане на конзолно приложение за задачи (To-Do list) \n")
printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
for i, item in enumerate(items):
    # Do stuff...
    time.sleep(0.07)
    # Update Progress Bar
    printProgressBar(i + 1, l, prefix = ' Loading:', suffix = 'Complete', length = 50)

clear_console()
#########################################################################


task_list = []

# Основен цикъл на приложението
while True:
    # Изчистване на конзолата
    clear_console()

    # Принтиране на основното меню
    print("     Това е конзолно приложение за задачи.\n")
    print("     1. Добави задача")
    print("     2. Премахни задача")
    print("     3. Покажи списъка със задачите")
    print("     4. Изтриване на текущата база данни със задачи!")
    print("     5. Изход")

    choise = input("\n      Очакваме Вашия избор (1-5): ")

    if choise == "1":
        # Принтиране на текущите задачи
        tasks = get_tasks(db_connection)

        print("\nСписък със задачи до този момент: \n")
        print("Id Task")
        print("-- ----")
        for task in tasks:
            print(f"{task[0]}. {task[1]}")

        new_task = input("\n Въведете нова задача (или 'exit' за връщане към основното меню): ")

        if new_task.lower() == "exit":
            print("\n Връщане към основното меню...")
            time.sleep(2)
            continue

        print("\n Задачата е добавена успешно. Връщане към основното меню...")


        # Добавяне на новата задача в базата данни
        add_task(db_connection, new_task)

        time.sleep(2)

    elif choise == "2": # Премахване на задача от базата
        # Принтиране на текущите задачи
        tasks = get_tasks(db_connection)

        print("\nСписък със задачи: \n")
        print("Id Task")
        print("-- ----")
        for task in tasks:
            print(f"{task[0]}. {task[1]}")

        # Въвеждане на команда за изтриване на задача
        command = input("\n Въведете номер(Id) на задачата, която искате да изтриете (или 'exit' за връщане към основното меню): ")
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


    elif choise == "3": # Показване на задачите
        if len(get_tasks(db_connection)) == 0:
            print("\n Списъка със задачи е празен.")
        else:
            tasks = get_tasks(db_connection)

            # Извеждане на текущите задачи
            print("\nСписък със задачи: \n")
            print("Id Task")
            print("-- ----")
            for task in tasks:
                print(f"{task[0]}. {task[1]}")

        print("\n Натисни 'Enter' за да се върнеш към основното меню")
        input()

    elif choise == "4": #Изтриване на текyщата база данни
        print()
        print("     ####################################################")
        print("     ############### !!! ВНИМАНИЕ !!! ###################")
        print("     ####################################################")
        print()
        # Изтриване на базата данни
        confirm = input("Сигурни ли сте, че искате да изтриете базата данни? yes(y)/no(n): ")
        if confirm.lower() == "yes" or confirm.lower() == "y":
            print()
            printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
            for i, item in enumerate(items):
                # Do stuff...
                time.sleep(0.1)
                # Update Progress Bar
                printProgressBar(i + 1, l, prefix='Dleteting DB:', suffix='Complete', length=50)

            delete_database(db_connection)
            print("\n Базата данни е изтрита успешно, връшане към основното меню...")

            # Забавяне между циклите
            time.sleep(3)
        #input()

    elif choise == "5":
        clear_console()
        exit()

    else:
        print("Невалиден избор, натиснете 'Enter' за да се върнете в основното меню...")
        input()
