from typing import OrderedDict
import KeySet

class Table:
    '''
    A table is a list of records.  A Table has a set of categories that are valid for
    the fields in each record.
        records<dict> = {primary_key<any>: fields<dict>}
        fields<dict> = {category_1<any>: data_1<any>, category_2<any>: data_2<any>}
            ***categories within the fields MUST correspond with a category in the Table
    '''

    def __init__(self, initial_record: dict = None, explicit_categories: set = None) -> None:
        # these constants are to improve the readability of the list comprehension when extracting
        # the categories from a record when categories were not explicitly provided
        
        FIRST_RECORD = 0            # access the first record in the records tuple
        EXTRACT_LIST_CONTENTS = 0   # extract the nested contents from a list

        self.__primary_key_set = set()
        self.__categories_set: set = set()
        self.__categories: tuple = tuple()
        self.__records: OrderedDict = OrderedDict()

        # if table categories were explicitly provided...
        if explicit_categories:

            # assign them
            self.__categories = explicit_categories
            
        # otherwise, if an initial record was provided...
        elif initial_record:
            # and assign the categories using the first record as a template
            # Remember: category refers to the key of a field dict, which is, in turn, in the value of a record dict.
            #   records = {primary_key_1: fields_1, primary_key_2: fields_2, ..., primary_key_n: fields_n}
            #       fields = {category_1: data_1, category_2: data_2, ..., category_n: data_n}
            #   therefore, if we extract the keys of the values of the record, we get our set of categories
            #   NOTE: because the OrderedDict.values() method
            category_list = []
            for category in list(initial_record.values())[EXTRACT_LIST_CONTENTS].keys():
                if category not in self.__categories:
                    self.__categories_set.add(category)
                    category_list.append(category)
                else:
                    raise SyntaxError(f'ERROR: All categories (columns) in a Table object must be unique.\n See "{category}".')
            self.__categories = tuple(category_list)
            initial_primary_key = list(initial_record.keys())[EXTRACT_LIST_CONTENTS]
            initial_fields = list(initial_record.values())[EXTRACT_LIST_CONTENTS]
            self.__records[initial_primary_key] = initial_fields
            self.__primary_key_set.add(initial_primary_key)
        else:
            raise SyntaxError('ERROR: Instantiating a Table object requires either an initial record or the table categories (columns) must be provided explicitly')
    # END __init__()

    def __str__(self):
        
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
    def primary_key_set(self):
        return self.__primary_key_set

    @primary_key_set.setter
    def primary_key_set(self, new_primary_key_set):
        self.__primary_key_set = new_primary_key_set

    @property
    def records(self):
        return self.__records

    def add_records(self, *records_to_add: dict or tuple):
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
        EXTRACT_LIST_CONTENTS = 0
        PRIMARY_KEY_FROM_TUPLE = 0
        
        for record_to_add in records_to_add:

            # if the user passed a dict as input
            if isinstance(record_to_add, dict):
                primary_key_to_add = list(record_to_add.keys())[EXTRACT_LIST_CONTENTS]
                fields_to_add = list(record_to_add.values())[EXTRACT_LIST_CONTENTS]

                if primary_key_to_add not in self.__primary_key_set:
                    if all([category in self.__categories for category in list(fields_to_add.keys())]):
                        self.__records[primary_key_to_add] = fields_to_add
                    else:
                        raise SyntaxError('ERROR: The record you attempted to add does not contain the same categories as the table.')
                else:
                    raise SyntaxError('ERROR: The record you attempted to add does not have a uniqe primary key.')

            # if the user passed a tuple
            elif isinstance(record_to_add, tuple):
                if len(record_to_add) == len(self.__categories) + 1:
                    fields_to_add: dict = dict()
                    for column, data in enumerate(record_to_add):
                        if column == PRIMARY_KEY_FROM_TUPLE:
                            primary_key_to_add = data
                        else:
                            fields_to_add[self.__categories[column-1]] = data
                    record_to_add: OrderedDict = {primary_key_to_add: fields_to_add}
                    self.__records[primary_key_to_add] = fields_to_add
                else:
                    raise SyntaxError('ERROR: The record you attempted to add does not contain the same categories as the table.  Did you forget to provide a primary key?')
            else:
                raise TypeError("ERROR: Record to add to the table must be an dict or tuple type.")

#######################################################
#Testing code:
#######################################################
if __name__ == '__main__':
    import datetime
    
    class Money(int):
        def __str__(self) -> str:
            return f'${self.__int__():>10,}'
    
    
    record_example_1: dict = {1: {'Last Name': 'Doe', 'First Name': 'John', 'Major': 'Computer Science', 'Date of Hire': datetime.date(2021,1,12), 'Salary': Money(45_000)}}
    record_example_2: dict = {2: {'Last Name': 'Lee', 'First Name': 'Bruce', 'Major': 'Physical Education', 'Date of Hire': datetime.date(1980,10,15), 'Salary': Money(2_800_000)}}
    tuple_record_example: tuple = (3, 'Musk', 'Elon', '-No Degree-', datetime.date(2020, 12, 25), Money(20_000))
    table_example = Table(record_example_1)
    table_example.add_records(record_example_2)
    table_example.add_records(tuple_record_example)
    print(table_example)

    table_example_2 = Table(explicit_categories=('Thing 1', 'Thing 2', 'Thing 3'))
    another_tuple_record: tuple = ('key',1,2,3)
    table_example_2.add_records(another_tuple_record)
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
