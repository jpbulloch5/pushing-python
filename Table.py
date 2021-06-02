from typing import OrderedDict
import KeySet

class Table:
    '''
    A table is a list of records.  A Table has a set of categories that are valid for
    the fields in each record.
        records<tuple> = 
    '''

    def __init__(self, categories: tuple) -> None:
        # these constants are to improve the readability of the list comprehension when extracting
        # the categories from a record when categories were not explicitly provided
        self.__categories_set: set = set(categories)
        self.__categories: tuple = tuple(categories)
        self.__records: tuple = tuple()
    # END __init__()

    def __str__(self):
        
        # store the formatted heading line because we will need it's length to generate a separater line
        heading = ''
        body = ''
        for name in self.__categories:
            heading += f'{str(name):20s} \t'

        body = ''
        for record in self.__records:
            body +='\n'
            for field in record.values():
                body += f'{str(field):20s}\t'

        # start a new line and output the heading as a row of text with a row of '=' characters to
        # separate the heading from the records in the table, then add each new record as a new line, 
        # plus an extra blank line at the end
        return f'\n{heading}\n{"=" * len(self.__categories)*23}{body}\n'
    # END __str__()

    @property
    def categories(self):
        return self.__categories

    @categories.setter
    def categories(self, new_categories):
        self.__categories = tuple(new_categories)
        self.__categories_set = set(new_categories)

    @property
    def categories_set(self):
        return self.__categories_set

    @property
    def records(self):
        return self.__records

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
                fields_to_add: OrderedDict = dict()
                for column, heading in enumerate(self.categories):
                        fields_to_add[heading] = record_to_add[column]
                self.__records += tuple([fields_to_add])
            else:
                raise SyntaxError('ERROR: The record you attempted to add does not contain the same categories as the table.')
    
    def subtable(self, *columns):
        for column in columns:
            pass
        pass

#######################################################
#Testing code:
#######################################################
if __name__ == '__main__':
    import datetime
    
    class Money(int):
        def __str__(self) -> str:
            return f'${self.__int__():>10,}'
    
    categories_1 =     ('Last Name', 'First Name', 'Major',              'Date of Hire',              'Salary')
    record_example_1 = ('Doe',       'John',       'Computer Science',   datetime.date(2021,1,12),    Money(45_000))
    record_example_2 = ('Lee',       'Bruce',      'Physical Education', datetime.date(1980,10,15),   Money(2_800_000))
    record_example_3 = ('Musk',      'Elon',       '-No Degree-',        datetime.date(2020, 12, 25), Money(20_000))
    table_example = Table(categories_1)
    table_example.add_records(record_example_1)
    table_example.add_records(record_example_2)
    table_example.add_records(record_example_3)
    print(table_example)

    table_example_2 = Table(categories=('Thing 1', 'Thing 2', 'Thing 3'))
    table_2_record: tuple = (1,2,3)
    table_example_2.add_records(table_2_record)
    print(table_example_2)
    '''
    #Some stuff the verify how any() and all() work
    positive_integers_less_than_10 = set()
    positive_integers_less_than_10 = (1, 2, 3, 4, 5, 6, 7, 8, 9)

    positive_even_integers_less_than_10 = set()
    positive_even_integers_less_than_10 = (2, 4, 6, 8)

    print("Check if all even integers less than 10 are in the integers less than 10 set:")                  
    print(all(member in positive_integers_less_than_10 for member in positive_even_integers_less_than_10))  # <--True
    print("Check if all integers less than 10 are in the even integers less than 10 set:")
    print(all(member in positive_even_integers_less_than_10 for member in positive_integers_less_than_10))  # <--False
    print("Check if any integer less than 10 is in the even integers less than 10 set:")
    print(any(member in positive_even_integers_less_than_10 for member in positive_integers_less_than_10))  # <--True
    '''
