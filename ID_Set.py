import sys

class ID:
    ''' This class creates an integer with a built-in left zero padding behavior
        for display.  It is otherwise treated as a normal integer.  It is meant
        to be used with the ID_Set class.
    '''
    def __init__(self, input_id: int, padding = len(str(sys.maxsize))) -> None:
        ''' 
        Constructor for ID objects.

        Parameters
        ----------
        input_id : int
            the integer value of the id
        padding : int
            the number of zeros to pad to the left of the input_id

        Raises
        ------
        TypeError
            when an attempt is made to compare equality with non-ID and non-integer types
        '''
        self._id: int = input_id
        self._left_pad_zeros: int = padding
    # END __init__()
    
    def __str__(self) -> str:
        return format(self._id, f'0{self._left_pad_zeros}d')
    
    def __eq__(self, other) -> bool:
        # allow equality as an integer
        print(f'checking {self} == {other}')
        if type(other) == type(int()):
            return self._id == other

        # do not allow equality as any other non-same type
        elif type(self) != type(other): 
            raise TypeError(f'Cannot compare equality of {type(self)} with {type(other)}.')
        
        # this line will only run when 'other' is an instance of ID too
        return self._id == other._id
    # END __eq__()

    def __lt__(self, other) -> bool:
        print(f'checking {self} < {other}')
        if type(other) == type(int()):
            return self._id < other
        elif type(self) != type(other): 
            raise TypeError(f'Cannot compare equality of {type(self)} with {type(other)}.')
        return self._id < other._id
    
    def __gt__(self, other) -> bool:
        print(f'checking {self} > {other}')
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
        Generates a new ID object that is garanteed to be unique within this set

        Parameters
        ----------
        start_from : int
            the number from which the method seeks to assign a new unique ID
        '''

        if (start_from == None 
          or start_from < self._minimum_valid_id 
          or start_from > self._maximum_valid_id):
            new_id: int = self._next_id
        else: 
            new_id: int = start_from

        # Make sure the new id will be the first unique integer after start_from
        while new_id in self._id_set:
            new_id += 1

            # if we reach the maximum valid id, wrap back to the minimum valid id
            if new_id > self._maximum_valid_id:
                new_id = self._minimum_valid_id
 
            # if we arrive back to our starting point, break the infinite loop and raise
            # an exception to inform the user that the set is full
            if new_id == start_from:
                raise IDSetFull()
    
        self._next_id = new_id

        # add the new, unique id to the set
        self._id_set.add(ID(new_id, self._left_pad_zeros))

        # prepare to give the next integer as the id for the next instantiated Serial_ID object
        self._next_id += 1

        return ID(new_id, self._left_pad_zeros)
    # END generate_new()

    def __str__(self) -> str:
        return str('\n'.join(str(entry) for entry in self._id_set))

    def __set_left_pad_zeros(self, padding: int = 0) -> None:
        self._left_pad_zeros = padding
        for entry in self._id_set:
            entry.set_padding(padding)

    def set_maximum_valid_id(self, new_maximum_valid_id: int) -> None:
        if new_maximum_valid_id > any(self._id_set):
            raise FailureToSetLowerMaximum(new_maximum_valid_id, max(self._id_set))
        self._maximum_valid_id = new_maximum_valid_id
        self.__set_left_pad_zeros(self, len(str(self._maximum_valid_id)))

    def set_minimum_valid_id(self, new_minimum_valid_id: int) -> None:
        if new_minimum_valid_id < any(self._id_set):
            raise FailureToSetHigherMinimum(new_minimum_valid_id, min(self._id_set))
        self._minimum_valid_id = new_minimum_valid_id

    def get_id_set(self) -> set:
        return self._id_set

    def remove_id_from_set(self, *ids_to_remove: int) -> None:
        for each_id in ids_to_remove:
            if each_id in self._id_set:
                self._id_set.remove(each_id)

#######################################################
#Testing code:
#######################################################
if __name__ == '__main__':
    entry_ids = ID_Set(maximum_valid_id=20)
    myID: ID = entry_ids.generate_new()
    print(myID)

    print('\ngenerate_new() * 10:')
    for x in range(11):
        entry_ids.generate_new()
    print(entry_ids)

    print('\nremove_id_from_set(18):')
    entry_ids.remove_id_from_set(18)
    print(entry_ids)

    print('\nremove_id_from_set(1):')
    entry_ids.remove_id_from_set(1)
    print(entry_ids)

    print('\nset_minimum_valid_id(5):')
    entry_ids.set_minimum_valid_id(5)
    print(entry_ids)
