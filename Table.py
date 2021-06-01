
from typing import OrderedDict

class Table:
    '''
    A table is a list of records.  A Table has a set of categories that are valid for
    the fields in each record.
        records<dict> = {primary_key<any>: fields<dict>}
        fields<dict> = {category_1<any>: data_1<any>, category_2<any>: data_2<any>}
            ***categories within the fields MUST correspond with a category in the Table
    '''
    

    def __init__(self, *records: OrderedDict, categories: set = None) -> None:
        # these constants are to improve the readability of the list comprehension when extracting
        # the categories from a record when categories were not explicitly provided
        FIRST_RECORD = 0            # access the first record in the records tuple
        EXTRACT_LIST_CONTENTS = 0   # extract the nested contents from a list

        self.__primary_key_set: set = set()
        self.__categories_set: set = set()
        self.__categories: tuple = tuple()
        self.__records: OrderedDict = OrderedDict()

        # if table categories were explicitly provided...
        if categories:

            # assign them
            self.__categories = categories

        # otherwise, check if at least one record was provided...
        elif records:
            # and assign the categories using the first record as a template
            # Remember: category refers to the key of a field dict, which is, in turn, in the value of a record dict.
            #   records = {primary_key_1: fields_1, primary_key_2: fields_2, ..., primary_key_n: fields_n}
            #       fields = {category_1: data_1, category_2: data_2, ..., category_n: data_n}
            #   therefore, if we extract the keys of the values of the record, we get our set of categories
            #   NOTE: because the OrderedDict.values() method
            category_list = []
            for category in list(records[FIRST_RECORD].values())[EXTRACT_LIST_CONTENTS].keys():
                if category not in self.__categories:
                    self.__categories_set.add(category)
                    category_list.append(category)
                else:
                    raise SyntaxError(f'ERROR: All categories (columns) in a Table object must be unique.\n See "{category}".')
            self.__categories = tuple(category_list)
            
        # otherwise...
        else:

            # raise a syntax error and teach the user how to call the constructor correctly
            raise SyntaxError('ERROR: If no records are provided for the Table object constructor call, then table categories (columns) must be provided explicitly.')

        self.__records = records

    # END __init__()

    def __str__(self):
        
        # store the formatted heading line because we will need it's length to generate a separater line
        heading = '#\t'
        for field in self.__categories:
            heading += str(field)+ '\t'

        body = '\n'
        for primary_key, fields in self.__records[0].items():
            body += f'{primary_key}\t'
            for data in fields.values():
                body += f'{data}\t'
            body += '\n'

        # start a new line and output the heading as a row of text with a row of '=' characters to
        # separate the heading from the records in the table, then add each new record as a new line, 
        # plus an extra blank line at the end
        return f'\n{heading}\n{"=" * len(heading)}\n{body}\n'
    # END __str__()

    def get_categories(self):
        return self.__categories

    def add_records(self, *records):
        '''
        Adds one or more records to the Table.

        Record Syntax:
        -------------
        dict{any unique: dict{any in table-category set: any}}
        {primary_key: {category: data}}
        '''
        
        # check if any of the primary keys in the records being added are already in the Table's primary key set
        if any(primary_key in self.__primary_key_set for primary_key in records.keys()):
            raise KeyError('ERROR: Cannot insert a record into the table if the primary key of that record already exists in the table.')
        
        if not all(field_category in self.__categories for field_category in records.values().keys()):
            raise KeyError('ERROR: Cannot insert a record into the table if the field categories do not match the table categories.')
        pass

    def record_is_valid(self, record_to_check) -> bool:
        pass

#######################################################
#Testing code:
#######################################################
if __name__ == '__main__':
    import datetime

    record_example: OrderedDict = {1: {'Last Name': 'Doe', 'First Name': 'John', 'Major': 'Computer Science', 'Date of Hire': datetime.date(2021,1,12), 'Salary': 45_000}}
    table_example = Table(record_example)
    print(table_example)

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
