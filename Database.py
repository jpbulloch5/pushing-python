class Table:
    '''
    A table is a list of records.  A Table has a set of categories that are valid for
    the fields in each record.
    '''
    def __init__(self, categories: tuple, records: list, primary_key_type: type = int) -> None:
        super(self)
        self.__primary_key_type = primary_key_type
        self.__primary_key_set: set = set()
        self.__records: list = []
        for record in records:
            if record.get_primary_key() not in self.__primary_key_set:
                self.__primary_key_set.add(record.get_primary_key())
                self.__records.append(record)
            
        self.__categories: set = categories

    def __str__(self):
        
        # store the formatted heading line because we will need it's lenght to generate a separater line
        heading_string = '\t'.join(self.__categories)

        # start a new line and output the heading as a row of text with a row of '=' characters to
        # separate the heading from the records in the table
        output_string = f'\n{heading_string}\n{"=" * len(heading_string)}'

        # add each new record as a new line, plus an extra blank line at the end
        output_string += f'{"\n".join(self.__records)}\n'
        
        return output_string
    
    def get_categories(self):
        return self.__categories

    def add_record(self, new_record):
        pass

class Record:
    '''
    A record is a row of fields in a table that is uniquely identified by 
    some primary key.
    '''
    def __init__(self, associated_table: Table, primary_key, fields: dict) -> None:
        self.__primary_key = primary_key
        self.__fields = fields
        self.__associated_table = associated_table
    
    def all_fields_valid(self) -> bool:
        for category in self.__fields.keys():
            if category not in self.__associated_table.get_headings():
                return False
        return True
    
    def get_primary_key(self):
        return self.__primary_key

    def get_fields(self):
        return self.__fields
        