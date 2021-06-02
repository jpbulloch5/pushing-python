import sys

class Key:
    ''' This class creates an integer with a built-in left zero padding behavior
        for display.  It is otherwise treated as a normal integer.  It is meant
        to be used with the KeySet class.
    '''
    def __init__(self, input_key: int, pad_to: int = 0) -> None:
        ''' 
        Constructor for Key objects.

        Parameters
        ----------
        input_key : int
            the integer value of the key
        pad_to : int
            pad with leading zeros to the left to ensure the number displays with this many digits

        Raises
        ------
        TypeError
            when an attempt is made to compare equality with non-Key and non-integer types
        '''
        self._key: int = input_key
        self._pad_to: int = pad_to
    # END __init__()
    
    def __str__(self) -> str:
        # the zfill() method is used for padding a string with leading zeroes up to a desired length
        return str(self._key).zfill(self._pad_to)
    
    def __eq__(self, other) -> bool:
        # allow equality as an integer
        if type(other) == type(int()):
            return self._key == other

        # do not allow equality as any other non-same type
        elif type(self) != type(other): 
            raise TypeError(f'Cannot compare equality of {type(self)} with {type(other)}.')
        
        # this line will only run when 'other' is an instance of Keye too
        return self._key == other._key
    # END __eq__()

    def __lt__(self, other) -> bool:
        if isinstance(other, int):
            return self._key < other
        elif isinstance(other, Key): 
            return self._key < other._key
        raise TypeError(f'Cannot compare equality of {type(self)} with {type(other)}.')
    
    def __gt__(self, other) -> bool:
        if isinstance(other, int):
            return self._key > other
        elif isinstance(other, Key):
            return self._key > other._key 
        raise TypeError(f'Cannot compare equality of {type(self)} with {type(other)}.')

    def __le__(self, other) -> bool:
        return self < other or self == other
    
    def __ge__(self, other) -> bool:
        return self > other or self == other

    def __hash__(self) -> int:
        '''
        Since Key objects are designed to use in a set, we need to make it hashable.
        Key objects are hashed by the integer value of the _key instance variable.
        '''
        # hash by the integer value of the key variable; treat like an integer
        return hash(self._key)
    
    @property
    def pad_to(self, new_padding: int) -> None:
        self._left_pad_zeros = new_padding
    
class KeySetFull(Exception):
    '''
    This error is raised when an KeySet object attempts to run the generate_new method
    when the set is full, meaning that there are no unique, unused values between the stated
    minimum/maximum values for the KeySet.
    '''
    def __init__(self) -> None:
        super().__init__('\nERROR: No valid Key could be generated, this KeySet is full.\nPlease reconsider the minimum and/or maximum valid Keys to accommodate more unique Keys.')

class FailureToLowerMaximum(Exception):
    '''
    This error is raised when an KeySet object attempts to change _maximum_valid_key
    to a new maximum that is lower than a current key in the set.
    '''
    def __init__(self, intended_maximum: int, violation: int) -> None:
        super().__init__(f'\nERROR: At least one existing Key in the KeySet ({violation}) was > the desired maximum of {intended_maximum}.  The maximum could not be lowered.')

class FailureToRaiseMinimum(Exception):
    '''
    This error is raised when an KeySet object attempts to change set_minimum_valid_key
     to a new minimum that is higher than a current key in the set.
    '''
    def __init__(self, intended_minimum: int, violation: int) -> None:
        super().__init__(f'\nERROR: At least one existing Key in the KeySet ({violation}) was < the desired minimum of {intended_minimum}.  The minimum could not be raised.')

class KeySet:
    def __init__(self, minimum_valid_key: int = 1, maximum_valid_key: int = sys.maxsize) -> None:
        '''
        This class creates an KeySet object, which defines a set of unique Key objects within 
        a given minimum and maximum value and ensures a uniform behavior of output using
        using leading zeros padded to the left as needed.

        Parameters
        ----------
        minimum_valid_key : int
            the minimum allowed integer to represent a key in this set
            DEFAULT = 1

        maximum_valid_key : int
            the maximum allowed integer to represent a key in this set
            DEFAULT = the largest integer value (via sys.maxsize)
        
        Raises
        ------
        KeySetFull : Exception
            when an KeySet object attempts to run the generate_new() method
            when the set is full, meaning that there are no unique, unused 
            values between the stated minimum/maximum values for the Key.
        FailureToLowerMaximum: Exception
            when an KeySet object attempts to update _maximum_valid_key to
            a new maximum value that is less than a current Key in the KeySet
        
        '''
        self._minimum_valid_key = minimum_valid_key
        self._maximum_valid_key = maximum_valid_key
        self._key_set = set()
        self._next_key = minimum_valid_key
        self._pad_to = len(str(maximum_valid_key))
    # END __init__()

    def generate_new(self, start_from = None) -> Key:
        '''
        Generates a new Key object that is garanteed to be unique within this set, and adds the new Key to the set
        Parameters
        ----------
        start_from : int
            the number from which the method seeks to assign a new unique Key
            the default behavior will increment from the previous or minmum (if no previous) assigned Key
        '''

        # If the user wants to override the start_from parameter, and their attempt to override was in-bounds...
        if (start_from != None and start_from >= self._minimum_valid_key and start_from <= self._maximum_valid_key):

            # assign the user's value as self._next_key
            self._next_key: int = self._next_key
            
        # ... otherwise, revert to the default behavior
        else: 

            # We need a non-None value in start_from so that we can use it to prevent an infinite loop below
            start_from = self._next_key

        # Make sure the new key will be the first unique integer after start_from
        while self._next_key in self._key_set:
            
            # increment to find a valid Key
            self._next_key += 1

            # if we pass the maximum valid key, wrap back to the minimum valid key
            if self._next_key > self._maximum_valid_key:
                self._next_key = self._minimum_valid_key
 
            # if we arrive back to our starting point, break the infinite loop and raise
            # an exception to inform the user that the set is full
            if self._next_key == start_from:
                raise KeySetFull()

        # instantiate a new Key object to use in the list
        new_key: Key = Key(self._next_key, self._pad_to)

        # add the new, unique key to the set
        self._key_set.add(new_key)

        # prepare to give the next sequential integer as the key for the next instantiated Key object
        self._next_key+= 1

        return Key(new_key, self._pad_to)
    # END generate_new()

    def __str__(self) -> str:
        # if the set is empty, outupt a string indicating an empty set
        if self._key_set == set(): return "{Ø}"
        # ... otherwise, output the set elements each on their own line
        return str('\n'.join(str(entry) for entry in self._key_set))

    @property
    def pad_to(self):
        return self._pad_to

    @pad_to.setter
    def pad_to(self, pad_to: int = None) -> None:
        '''
        This is a private method intended for internal use only.
        This method changes the padding of left zeros for every Key element in the set.
        Parameters)
        ----------
        padding : int
            pad with zeros to the left of the Keys in the set to fill out this many digits
            if no override value is provided, the method will ensure that the padding will
            match the length of the maximum valid key for the set
        '''

        # if the user did not provide an override for padding,
        if pad_to == None:

            # unsure that the padding matches the length of the maximum valid key for the set
            self._pad_to = len(str(self._maximum_valid_key))

        # ... otherwise,
        else:

            # set the padding to the override value provided
            self._pad_to = pad_to

        # iterate through the set and update the pad_to value of each Key object to ensure uniform padding throughout
        for entry in self._key_set:
            entry._pad_to = pad_to

    def set_maximum_valid_key(self, new_maximum_valid_key: int) -> None:
        '''
        This method allows the user to update the maximum valid key for this set.
        Parameters
        ----------
        new_maximum_valid_key : int
            the value you wish to set as the new maximum valid key for the set.
        Raises
        ------
        FailureToSetLowerMaximum : Exception
            when the user attempts to update the new maximum valid key for the set to a value
            that is less than any value in the set
        '''
        if new_maximum_valid_key < any(self._key_set):
            raise FailureToLowerMaximum(new_maximum_valid_key, max(self._key_set))
        self._maximum_valid_key = new_maximum_valid_key
        self.pad_to = len(str(self._maximum_valid_key))

    def set_minimum_valid_key(self, new_minimum_valid_key: int) -> None:
        '''
        This method allows the user to update the minimum valid key for this set.
        Parameters
        ----------
        new_minimum_valid_key : int
            the value you wish to set as the new minimum valid key for the set.
        Raises
        ------
        FailureToSetHigherMinimum : Exception
            when the user attempts to update the new minimum valid key for the set to a value
            that is greater than any value in the set
        '''
        if new_minimum_valid_key > any(self._key_set):
            raise FailureToRaiseMinimum(new_minimum_valid_key, min(self._key_set))
        self._minimum_valid_key = new_minimum_valid_key

    def get_key_set(self) -> set:
        '''
        A simple getter-method for the entire set.
        Because the __str__() method is overriden, this can be called to a string, in which case it will
        output as a vertical list of the elements of the set
        '''
        return self._id_set

    def remove_key(self, *keys_to_remove: int) -> None:
        '''
        This method allows one or more Key objects to be removed from the set
        '''
        for key_to_remove in keys_to_remove:
            if key_to_remove in self._key_set:
                self._key_set.remove(key_to_remove)
                print(f'Key [{key_to_remove}] was successfully removed from this KeySet.')
            else:
                print(f'{key_to_remove} could not be removed because it was not a member of this KeySet.  Set boundaries: [{self._minimum_valid_key}...{self._maximum_valid_key}]')

#######################################################
#Testing code:
#######################################################
if __name__ == '__main__':
    print('\nNew KeySet object instantiated:')
    my_key_set = KeySet(0, 119999)
    print(my_key_set)    # {Ø} - Empty Set

    print('\nID variable set to generate_new() return value:')
    my_key: Key = my_key_set.generate_new()
    print(my_key_set)
    print('\nValue of the Key variable:')
    print(my_key)
    print('\nAll KeySet elements:')
    print(my_key_set)

    print('\ngenerate_new() * 10:')
    for x in range(11):
        my_key_set.generate_new()
    print(my_key_set)

    print('\nremove_key(18):')
    my_key_set.remove_key(18)
    print(my_key_set)

    print('\nremove_key(my_key):')
    my_key_set.remove_key(my_key)
    print(my_key_set)

    print('\nset_maximum_valid_key(110020):')
    my_key_set.set_maximum_valid_key(110020)
    print(my_key_set)