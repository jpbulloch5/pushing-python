from KeySet import KeySet, Key
from Table import Table
from typing import OrderedDict

class KeyTable(Table):
    def __init__(self, categories: set, primary_key_set: KeySet = KeySet(0,99999)) -> None:
        
        self.__primary_key_set = primary_key_set
        self.__categories_set = set(categories)
        self.__categories = tuple(categories)
        self.__records = OrderedDict()
        super(KeyTable, self).__init__(categories)
    # END __init__()

    def __add_record(self, record_to_add: tuple):
        '''
        Adds one or more records to the Table.

        Parameter
        ---------
        key_override: int
            The primary key value you would like to use for this record
            If the key already exists, it will assign the next valid, uniqe
            value instead.
        *records : tuple
            The records to be added to the table
            NOTE: do not include the primary key for the record in the tuple
                    
        '''
        
        #if len(record_to_add) == len(self.__categories):
        primary_key_to_add: Key = self.__primary_key_set.generate_new()
        fields_to_add: dict = dict()
        for column, data in enumerate(record_to_add):
                try:
                    fields_to_add[self.__categories[column-1]] = data
                except IndexError:
                    print('IndexError(Handled): Found more fields than table categories, extra fields were truncated.')
        record_to_add: OrderedDict = {primary_key_to_add: fields_to_add}
        self.__records[primary_key_to_add._key] = fields_to_add

    def add_records(self, records_to_add):
        for record_to_add in records_to_add:
            if isinstance(record_to_add, tuple):
                self.__add_record(record_to_add)
            else:
                self.__add_record(records_to_add)
                return

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

    @property
    def primary_key_set(self):
        return self.__primary_key_set

    @primary_key_set.setter
    def primary_key_set(self, new_primary_key_set):
        self.__primary_key_set = new_primary_key_set

#######################################################
#Testing code:
#######################################################
if __name__ == '__main__':
    from datetime import date

    class Money(int):
        def __str__(self) -> str:
            return f'${self.__int__():>10,}'
    import datetime


    my_table = KeyTable(('Item Description', 'Serial #',  'Location',          'Purchase Date',   'Purchase Price', 'End of Life'))
    my_table.add_records(('HP Laptop',       12597856879, 'Recruiting Office', date(2020, 4, 23), Money(4_000),     date(2021,6,1)))
    print(my_table)
    