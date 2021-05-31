class Table:
    '''
    A table is a list of records.  A Table has a set of categories that are valid for
    the fields in each record.
        record<dict> = {primary_key<any unique>: fields<dict>}
        field<dict> = {category<any unique>: value<any>}
    '''
    def __init__(self, categories: tuple, *records: dict) -> None:
        
        self.__categories = categories
        self.__primary_key_set: set = set()
        self.__records: dict = dict()

        record_primary_keys: int = records.keys()
        record_fields: dict = records.values()

        field_categories: str = record_fields.keys()    # alias = records.values().keys()
        field_values = record_fields.values()           # alias = records.values().values()
        
        for record_primary_key, record_field in records:
            if (record_primary_key not in self.__primary_key_set    # if the record has a unique primary key
            and record_field.keys() in self.__categories):          # and the field category is also a table category
                

        self.__categories: set = categories
    # END __init__()

    def __str__(self):
        
        # store the formatted heading line because we will need it's length to generate a separater line
        heading = '\t'.join(self.__categories)

        # start a new line and output the heading as a row of text with a row of '=' characters to
        # separate the heading from the records in the table, then add each new record as a new line, 
        # plus an extra blank line at the end
        return f'\n{heading}\n{"=" * len(heading)}' + f'{"\n".join(self.__records)}\n'
    # END __str__()

    def get_categories(self):
        return self.__categories

    def add_record(self, primary_key, fields: dict):
        pass

    def record_is_valid(self, record_to_check) -> bool:
        pass

        