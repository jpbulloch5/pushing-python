from Menu import Menu
from KeySet import KeySet
from KeyTable import KeyTable

def main():
    main_menu = Menu(
        '''
        Basic Asset Management System Functioinality Test
        Main Menu
        1) Create a new Table
        2) Add a record
        3) Display the Table
        4) Exit the program
        ''',{
            1: create_table,
            2: add_record,
            3: display_table,
            4: exit()
        })

    main_menu.select()

active_tables = dict()

def create_table():
    print('\nCreating a new Table...\n')
    name = input('Input a name for your new Table: ')
    min_key = Menu('Choose a minimum valid primary key value for your new Table.').collect_int()
    max_key = Menu('Choose a maximum valid primary key value for your new Table.').collect_int()

    categories = list()
    while True: 
        category_name = input('Enter a name for your first table category (column).')
        if category_name != '': break
    categories.append(category_name)

    while category_name != '':
        category_name = input('Enter another category (column) name for this table.\n [or press ENTER on a blank line when you are done entering column names.')
        categories.append(category_name)

    active_tables[name] = KeyTable(categories, KeySet(min_key,max_key))

def add_record():
    pass

def display_table():
    pass

if __name__ == '__main__':
    main()