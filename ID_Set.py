import sys

class ID:
    ''' This class creates an integer with a built-in left zero padding behavior
        for display.  It is otherwise treated as a normal integer.  It is meant
        to be used with the ID_Set class.
    '''
    def __init__(self, input_id: int, padding: int = 0) -> None:
        ''' 
        Constructor for ID objects.

        Parameters
        ----------
        input_id : int
            the integer value of the id
        padding : int
            pad with leading zeros to the left to ensure the number displays with this many digits

        Raises
        ------
        TypeError
            when an attempt is made to compare equality with non-ID and non-integer types
        '''
        self._id: int = input_id
        self._left_pad_zeros: int = padding
    # END __init__()
    
    def __str__(self) -> str:
        # the zfill() method is used for padding a string with leading zeroes up to a desired length
        return str(self._id).zfill(self._left_pad_zeros)
    
    def __eq__(self, other) -> bool:
        # allow equality as an integer
        if type(other) == type(int()):
            return self._id == other

        # do not allow equality as any other non-same type
        elif type(self) != type(other): 
            raise TypeError(f'Cannot compare equality of {type(self)} with {type(other)}.')
        
        # this line will only run when 'other' is an instance of ID too
        return self._id == other._id
    # END __eq__()

    def __lt__(self, other) -> bool:
        if type(other) == type(int()):
            return self._id < other
        elif type(self) != type(other): 
            raise TypeError(f'Cannot compare equality of {type(self)} with {type(other)}.')
        return self._id < other._id
    
    def __gt__(self, other) -> bool:
        if type(other) == type(int()):
            return self._id > other
        elif type(self) != type(other): 
            raise TypeError(f'Cannot compare equality of {type(self)} with {type(other)}.')
        return self._id > other._id

    def __le__(self, other) -> bool:
        return self < other or self == other
    
    def __ge__(self, other) -> bool:
        return self > other or self == other

    def __hash__(self) -> int:
        '''
        Since ID objects are designed to use in a set, we need to make it hashable.
        ID objects are hashed by the integer value of the _id instance variable.
        '''
        # hash by the id variable, treat like an integer
        return hash(self._id)
    
    def set_padding(self, new_padding: int) -> None:
        self._left_pad_zeros = new_padding
    
class IDSetFull(Exception):
    '''
    This error is raised when an ID_Set object attempts to run the generate_new method
    when the set is full, meaning that there are no unique, unused values between the stated
    minimum/maximum values for the ID_Set.
    '''
    def __init__(self) -> None:
        super().__init__('\nERROR: No valid ID could be generated, this ID_Set is full.\nPlease reconsider the minimum and/or maximum valid IDs to accommodate more unique Serial_IDs.')

class FailureToSetLowerMaximum(Exception):
    '''
    This error is raised when an ID_Set object attempts to call the set_maximum_valid_id()
    method to make a new maximum valid id that is lower than a current id in the set.
    '''
    def __init__(self, intended_maximum: int, violation: int) -> None:
        super().__init__(f'\nERROR: At least one existing ID in the ID_Set ({violation}) was > the desired maximum of {intended_maximum}.  The maximum could not be lowered.')

class FailureToSetHigherMinimum(Exception):
    '''
    This error is raised when an ID_Set object attempts to call the set_minimum_valid_id()
    method to make a new minimum valid id that is higher than a current id in the set.
    '''
    def __init__(self, intended_minimum: int, violation: int) -> None:
        super().__init__(f'\nERROR: At least one existing ID in the ID_Set ({violation}) was < the desired minimum of {intended_minimum}.  The minimum could not be raised.')

class ID_Set:
    def __init__(self, minimum_valid_id: int = 1, maximum_valid_id: int = sys.maxsize) -> None:
        '''
        This class creates an ID_Set object, which defines a set of unique ID objects within 
        a given minimum and maximum value and ensures a uniform behavior of output using
        using leading zeros padded to the left as needed.

        Parameters
        ----------
        minimum_valid_id : int
            the minimum allowed integer to represent an id in this set
            DEFAULT = 1
        maximum_valid_id : int
            the maximum allowed integer to represent an id in this set
            DEFAULT = the largest integer value (via sys.maxsize)
        
        Raises
        ------
        IDSetFullException : Exception
            when an ID_Set object attempts to run the generate_new() method
            when the set is full, meaning that there are no unique, unused 
            values between the stated minimum/maximum values for the ID_Set.
        FailureToSetLowerMaximum: Exception
            when an ID_set object attempts to run the set_maximum_valid_id()
            method with a new maximum value that is less than a current value
            in the ID_Set
        
        '''
        self._minimum_valid_id = minimum_valid_id
        self._maximum_valid_id = maximum_valid_id
        self._id_set = set()
        self._next_id = minimum_valid_id
        self._left_pad_zeros = len(str(maximum_valid_id))
    # END __init__()

    def generate_new(self, start_from = None) -> ID:
        '''
        Generates a new ID object that is garanteed to be unique within this set, and adds the new ID to the set

        Parameters
        ----------
        start_from : int
            the number from which the method seeks to assign a new unique ID
            the default behavior will increment from the previous or minmum (if no previous) assigned ID
        '''

        # If the user wants to override the start_from parameter, and their attempt to override was in-bounds...
        if (start_from != None and start_from >= self._minimum_valid_id and start_from <= self._maximum_valid_id):

            # assign the user's value as self._next_id
            self._next_id: int = self._next_id
            
        # ... otherwise, revert to the default behavior
        else: 

            # We need a non-None value in start_from so that we can use it to prevent an infinite loop below
            start_from = self._next_id

        # Make sure the new id will be the first unique integer after start_from
        while self._next_id in self._id_set:
            
            # increment to find a valid ID
            self._next_id += 1

            # if we pass the maximum valid id, wrap back to the minimum valid id
            if self._next_id > self._maximum_valid_id:
                self._next_id = self._minimum_valid_id
 
            # if we arrive back to our starting point, break the infinite loop and raise
            # an exception to inform the user that the set is full
            if self._next_id == start_from:
                raise IDSetFull()

        # instantiate a new ID object to use in the list
        new_id: ID = ID(self._next_id, self._left_pad_zeros)

        # add the new, unique id to the set
        self._id_set.add(new_id)

        # prepare to give the next sequential integer as the id for the next instantiated Serial_ID object
        self._next_id += 1

        return ID(new_id)
    # END generate_new()

    def __str__(self) -> str:
        # if the set is empty, outupt a string indicating an empty set
        if self._id_set == set(): return "{Ø}"
        # ... otherwise, output the set elements each on their own line
        return str('\n'.join(str(entry) for entry in self._id_set))

    def __set_left_pad_zeros(self, padding: int = None) -> None:
        '''
        This is a private method intended for internal use only.
        This method changes the padding of left zeros for every ID element in the set.

        Parameters
        ----------
        padding : int
            pad with zeros to the left of the IDs in the set to fill out this many digits
            if no override value is provided, the method will ensure that the padding will
            match the length of the maximum valid id for the set
        '''

        # if the user did not provide an override for padding,
        if padding == None:

            # unsure that the padding matches the length of the maximum valid id for the set
            self._left_pad_zeros = len(str(self._maximum_valid_id))

        # ... otherwise,
        else:

            # set the padding to the override value provided
            self._left_pad_zeros = padding

        # iterate through the set and update the padding value of each ID object to ensure uniform padding throughout
        for entry in self._id_set:
            entry.set_padding(padding)

    def set_maximum_valid_id(self, new_maximum_valid_id: int) -> None:
        '''
        This method allows the user to update the maximum valid id for this set.

        Parameters
        ----------
        new_maximum_valid_id : int
            the value you wish to set as the new maximum valid id for the set.

        Raises
        ------
        FailureToSetLowerMaximum : Exception
            when the user attempts to update the new maximum valid id for the set to a value
            that is less than any value in the set
        '''
        if new_maximum_valid_id < any(self._id_set):
            raise FailureToSetLowerMaximum(new_maximum_valid_id, max(self._id_set))
        self._maximum_valid_id = new_maximum_valid_id
        self.__set_left_pad_zeros(len(str(self._maximum_valid_id)))

    def set_minimum_valid_id(self, new_minimum_valid_id: int) -> None:
        '''
        This method allows the user to update the minimum valid id for this set.

        Parameters
        ----------
        new_minimum_valid_id : int
            the value you wish to set as the new minimum valid id for the set.

        Raises
        ------
        FailureToSetHigherMinimum : Exception
            when the user attempts to update the new minimum valid id for the set to a value
            that is greater than any value in the set
        '''
        if new_minimum_valid_id > any(self._id_set):
            raise FailureToSetHigherMinimum(new_minimum_valid_id, min(self._id_set))
        self._minimum_valid_id = new_minimum_valid_id

    def get_id_set(self) -> set:
        '''
        A simple getter-method for the entire set.
        Because the __str__() method is overriden, this can be called to a string, in which case it will
        output as a vertical list of the elements of the set
        '''
        return self._id_set

    def remove_id_from_set(self, *ids_to_remove: int) -> None:
        '''
        This method allows one or more ID objects to be removed from the set
        '''
        for each_id in ids_to_remove:
            if each_id in self._id_set:
                self._id_set.remove(each_id)
                print(f'ID {each_id} was successfully removed from this ID_Set.')
            else:
                print(f'{each_id} could not be removed because it was not a member of this ID_Set.  Set boundaries: [{self._minimum_valid_id}...{self._maximum_valid_id}]')

#######################################################
#Testing code:
#######################################################
if __name__ == '__main__':
    print('\nNew ID_Set object instantiated:')
    entry_ids = ID_Set(110000, 119999)
    print(entry_ids)    # {Ø} - Empty Set

    print('\nID variable set to generate_new() return value:')
    myID: ID = entry_ids.generate_new()
    print(entry_ids)
    print('\nValue of the ID variable:')
    print(myID)
    print('\nAll ID_Set elements:')
    print(entry_ids)

    print('\ngenerate_new() * 10:')
    for x in range(11):
        entry_ids.generate_new()
    print(entry_ids)

    print('\nremove_id_from_set(18):')
    entry_ids.remove_id_from_set(18)
    print(entry_ids)

    print('\nremove_id_from_set(myID):')
    entry_ids.remove_id_from_set(myID)
    print(entry_ids)

    print('\nset_maximum_valid_id(110020):')
    entry_ids.set_maximum_valid_id(110020)
    print(entry_ids)
