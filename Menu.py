import types

class Menu:
    def __init__(self, prompt: str = "Make a selection.", options: dict = None) -> None:
        '''
        A menu object facilitates allowing a user to select an option from a provided list.
        
        Parameters
        ----------
        prompt : str
            a string explaining the purpose of the input request
        
        options: dict
            the keys  in this dict are the items the user can enter as input to select
            the corresponding value.
        '''
        self.__prompt = prompt
        self.__options = dict()
        for key, value in options.items():
            self.__options[str(key)] = value
        
    def select(self):
        '''
        This method prompts the user to make a selection from the associated menu.
        If the menu's options are function references, then the function will be run
        as a result of the selection, otherwise, the value associated with the key
        selected by the user will be returned.
        The method detects incorrect input and reintroduces the prompt until valid
        input is provided
        '''

        # this constant is used to extract content from view type objects after converting them to a list
        EXTRACT_CONTENT = 0

        while True:
            print(self.__prompt)
            if self.__options:
                print(f'Options: {[option for option in self.__options.keys()]}\n')

                selection = self.__options.get(input('Your selection: ').lower(), None)
                if isinstance(selection, types.FunctionType): return selection()
                elif isinstance(selection, type(list(self.__options.values())[EXTRACT_CONTENT])): return selection
                else: print(f'\nERROR: Your input was not recoginzed, please review the listed options and try again.\nValid selections are {tuple(self.__options.keys())}.')
            else:
                raise SyntaxError('ERROR: The Menu.select() method can only be run on a Menu with options')
    
    def key_select(self):
        while True:
            print(self.__prompt)
            if self.__options:
                print(f'Options: {[(option, result) for (option, result) in self.__options.items()]}\n')

                selection = self.__options.get(input('Your selection: ').lower(), None)
                if selection: return selection
                else: print(f'\nERROR: Your input was not recoginzed, please review the listed options and try again.\nValid selections are {tuple(self.__options.keys())}.')
            else:
                raise SyntaxError('ERROR: The Menu.select() method can only be run on a Menu with options')

    def collect_int(prompt) -> int:
        while True:
            collected = input(f'{prompt}\nEnter an integer: ')
            if collected.isdecimal():
                return int(collected)
            else:
                print(f'\nERROR: Only integers are accepted as valid input!\n')
    
    def collect_number(prompt) -> float:
        while True:
            collected = input(f'{prompt}\nEnter a number: ')
            if collected.isdecimal():
                return int(collected)
            elif collected.count('.') == 1 and all(substring.isdecimal() for substring in collected.split('.')):
                return float(collected)
            else:
                print(f'\nERROR: Only numbers are accepted as valid input!  Note: comas are not supported.\n')


#######################################################
#Testing code:
#######################################################
if __name__ == '__main__':

    '''
    # Testing Menu().collect_number
    user_number = Menu('Some prompt.').collect_number()
    print(f'\nYou entered a {user_number}, which is a {type(user_number)}.')

    '''
    # Testing Menu().select()
    def choice_1():
        print('(((1)))')

    def choice_2():
        print('<<<2>>>')
    
    test_1 = lambda: choice_1()
    prompt = 'Make a selection:'
    choices = {1: choice_1, 2: choice_2}
    Menu(prompt, choices).select()

    choice_menu = Menu('choose an option: ', {1: 'first one', 2: 'second one'})
    print(f'You picked the {choice_menu.select()}')
    ''' #'''