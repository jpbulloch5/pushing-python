from datetime import date
from KeySet import KeySet
from Table import Table
from typing import OrderedDict

class PrimaryKeyTable(Table):
    def __init__(self, explicit_categories: set, primary_key_set: KeySet = KeySet()) -> None:
        self.__primary_key_set = primary_key_set
        self.__categories_set = set(explicit_categories)
        self.__categories = tuple(explicit_categories)
        self.__records = OrderedDict()
    # END __init__()

    def add_records(self, *records_to_add: tuple):
        '''
        Adds one or more records to the Table.

        Parameter
        ---------
        *records : nested dicts, or tuples
            The records to be added to the table
            Syntax : nested dicts
                {primary_key: {category_1: data_1, category_2: data_2}}
            Syntax : tuples
                (primary_key, data_1, data_2)
                    When using tuples, the categories are extracted from the Table categories and mapped in order
                    
        '''
        
        for record_to_add in records_to_add:
            if len(record_to_add) == len(self.__categories):
                primary_key_to_add = self.__primary_key_set.generate_new()
                fields_to_add: dict = dict()
                for column, data in enumerate(record_to_add):
                        fields_to_add[self.__categories[column-1]] = record_to_add[column]
                record_to_add: OrderedDict = {primary_key_to_add: fields_to_add}
                self.__records[primary_key_to_add] = fields_to_add
            else:
                raise SyntaxError('ERROR: The record you attempted to add does not contain the same categories as the table.  Did you forget to provide a primary key?')


#######################################################
#Testing code:
#######################################################
if __name__ == '__main__':
    import datetime

    class Money(int):
        def __str__(self) -> str:
            return f'${self.__int__():>10,}'
    import datetime


    my_table = PrimaryKeyTable(explicit_categories=('Item Description', 'Serial #', 'Location', 'Purchase Date', 'Purchase Price', 'End of Life'))
    record_to_add = ('HP Laptop', 12597856879, '(remote) Recruiting Office', date(2020, 4, 23), Money(4_000))
    my_table.add_records()
    print(my_table)