from Menu import Menu
from KeySet import KeySet
from KeyTable import KeyTable
import os
import pickle


active_tables = dict()

def main():
    
    main_menu = Menu(
        '''
Basic Asset Management System Functioinality Test
=================================================

Main Menu
---------
1) Create a new Table from the Terminal
2) **Load a Table from a file
3)   Add a record
4)   Display a Table
5) **Save a Table to a file
6) **Update a record
7) **Retrieve a record by its primary key
8) **Generate a report
9)   Exit the program

** = Not implemented yet.
        ''', 
        {
            1: create_table,
            2: not_implemented_yet,
            3: add_record,
            4: display_table,
            5: not_implemented_yet,
            6: not_implemented_yet,
            7: not_implemented_yet,
            9: exit_program
        })
    while True: main_menu.select()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def not_implemented_yet():
    print('\nSorry, this option has not been implemented yet.\nReturning to Main Menu...\n')

def select_table() -> KeyTable:
    return Menu('Which table?', active_tables).select()

# 1) Create a new Table from the Terminal
def create_table():
    print('\nCreating a new Table...\n')
    name = input('\nInput a name for your new Table: ')
    min_key = Menu.collect_int('\nChoose a minimum valid primary key value for your new Table.')
    max_key = Menu.collect_int('\nChoose a maximum valid primary key value for your new Table.')

    categories = list()
    while True: 
        category_name = input('\nEnter a name for your first table category (column).')
        if category_name != '': break
    categories.append(category_name)

    while category_name != '':
        category_name = input('\nEnter another category (column) name for this table.\n [or press ENTER on a blank line when you are done entering column names.')
        if category_name: categories.append(category_name)

    active_tables[name] = KeyTable(categories, KeySet(min_key,max_key))

# 2) **Load a Table from a file
def load_file():
    not_implemented_yet()
    
# 3)   Add a record
def add_record():
    print('\nAdd a record to a table...\n')
    if active_tables:
        active_table = select_table()
        record_to_add = []
        for category in active_table.categories:
            record_to_add.append(input(f"\nEnter a value for this record's {category} category: "))

        print(f'Adding: {tuple(record_to_add)}...')
        active_table.add_records(tuple(record_to_add))

        print(active_table)
    else:
        print('\nThere are no active tables available to accept a new record.  Please create a new table.\nReturning to Main Menu...\n')

# 4)   Display a Table
def display_table():
    if active_tables: print(select_table())
    else:
        print('\nThere are no active tables available to display.  Please create a new table.\nReturning to Main Menu...\n')

# 5) **Save a Table to a file
def save_table():
    not_implemented_yet()

# 6) **Update a record
def update_record():
    not_implemented_yet()

# 7) **Retrieve a record by its primary key
def retrieve_by_key():
    not_implemented_yet()

# 8) **Generate a report
def generate_report():
    not_implemented_yet()

# 9)   Exit the program
def exit_program():
    print('\nExiting program...\n')
    exit()


if __name__ == '__main__':
    main()