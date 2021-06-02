class Menu:
    def __init__(self, prompt: str = "Make a selection.", options: dict = None) -> None:
        '''

        '''
        self.__prompt = prompt
        self.__options = options
        
    def select(self):
        while True:
            print(self.__prompt)
            if self.__options:
                for option  in self.__options.keys():
                    print(f'\t{option})')
                selection = None
            
                selection = self.__options.get(input('Your selection: ').lower(), None)
                if selection: return selection()
                else: print(f'\nERROR: Your input was not recoginzed, please review the listed options and try again.\nValid selections are {tuple(self.__options.keys())}.')
            else:
                raise SyntaxError('ERROR: The Menu.select() method can only be run on a Menu with options')
    
    def collect_int(self) -> int:
        while True:
            collected = input(f'{self.__prompt}\nEnter an integer: ')
            if collected.isdecimal():
                return int(collected)
            else:
                print(f'\nERROR: Only integers are accepted as valid input!\n')
    
    def collect_number(self) -> float:
        while True:
            collected = input(f'{self.__prompt}\nEnter a number: ')
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
    choices = {'1': choice_1, '2': choice_2}
    Menu(prompt, choices).select()
    '''