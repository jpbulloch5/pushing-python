import os

def win_path_to_bash_path(win_path: str = os.getcwd()) -> str:
    ''' Converts a complete windows path into a proper bash path
        "C:\dir1\dir2" => "/c/dir1/dir2"

        Parameters
        ----------
        win_path: str
            a windows-style path to a directory represented as a string
            DEFAULT = Current working directory (via os.getcwd())
        
        Returns
        -------
        str
            the Bash standard version of the windows-style path supplied
    '''
    # split the windows path into a list of directories with [0] as the drive letter
    dir_list = win_path.split('\\')
    
    # isolate the drive letter (leave off the ':') and add it to the bash path
    bash_path = f'/{dir_list[0][0]}'

    # add each directory from the list to the bash path in proper bash format with '/' as deliminators
    for dir in dir_list[1:]:
        bash_path += f'/{dir}'

    # return the completed path in proper bash format
    return bash_path

    
if __name__ == '__main__':
    print(win_path_to_bash_path())