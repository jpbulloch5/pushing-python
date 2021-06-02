from datetime import date
from KeySet import KeySet, Key
from Table import Table
from typing import OrderedDict

class PrimaryKeyTable(Table):
    def __init__(self, explicit_categories: set, primary_key_set: KeySet = KeySet(0,99999)) -> None:
        super().__init__(initial_record=None, explicit_categories=explicit_categories)
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
                primary_key_to_add: Key = self.__primary_key_set.generate_new()
                fields_to_add: dict = dict()
                for column, data in enumerate(record_to_add):
                        fields_to_add[self.__categories[column-1]] = data
                record_to_add: OrderedDict = {primary_key_to_add: fields_to_add}
                self.__records[primary_key_to_add._key] = fields_to_add
            else:
                raise SyntaxError('ERROR: The record you attempted to add does not contain the same categories as the table.')
            print(self.__records)

    def __str__(self):
        '''
        I must not understand something important about inheritance here, because the code below
        is exactly the same code in the superclass, but if I don't overload this method, it does
        not seem to understand any of the instance variables
        '''
        # store the formatted heading line because we will need it's length to generate a separater line
        heading = f'{"Key":5s}\t'
        for field in self.__categories:
            heading += f'{str(field):20s} \t'

        body = ''
        for primary_key, fields in self.__records.items():
            body += f'\n{str(primary_key):5s}\t'
            for data in fields.values():
                body += f'{str(data):20s}\t'

        # start a new line and output the heading as a row of text with a row of '=' characters to
        # separate the heading from the records in the table, then add each new record as a new line, 
        # plus an extra blank line at the end
        return f'\n{heading}\n{"=" * len(self.__categories)*23}{body}\n'
    # END __str__()

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
    record_to_add = ('HP Laptop', 12597856879, 'Recruiting Office', date(2020, 4, 23), Money(4_000), date(2021,6,1))
    my_table.add_records(record_to_add)
    print(my_table.records)
    print(my_table)
    print(my_table.records)
    