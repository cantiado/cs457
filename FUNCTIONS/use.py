# Author: Carl Antiado
# Last Updated: 4/16/2022
# Created 2/10/2022

'''
USE: <db_name>
db_name: <string>
'''

import os

def use(tokens: list[str]) -> str:
    # Check if exactly 1 token
    if len(tokens) == 0:
        print(f'!Failed to select database because of missing arguments.')
        return
    if len(tokens) > 1:
        print(f'!Failed to select database because of too many arguments.')
        return

    # Get and check if database db_name exists.
    db_name = tokens.pop()
    cwd = os.getcwd()
    db_path = os.path.join(cwd,db_name)
    if os.path.isdir(db_path):
        print(f'Using database {db_name}.')
        return db_name
    else:
        print(f'!Failed to select database {db_name} because it does not exist.')
        return 'NULL'