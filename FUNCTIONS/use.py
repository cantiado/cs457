# Author: Carl Antiado
# Last Updated: 2/10/2022
# Created 2/10/2022

# USE <db_name>
# db_name: <string>

import os

def use(tokens: list[str]) -> str:
    # fail if not exactly 1 token
    if len(tokens) == 0:
        print(f'!Failed to select database because of missing arguments.')
        return
    if len(tokens) > 1:
        print(f'!Failed to select database because of too many arguments.')
        return

    # only token is database name
    db_name = tokens.pop()
    cwd = os.getcwd()
    db_path = os.path.join(cwd,db_name)
    # fail and return NULL if database does not exist
    # otherwise select database and return selection
    if os.path.isdir(db_path):
        print(f'Using database {db_name}.')
        return db_name
    else:
        print(f'!Failed to select database {db_name} because it does not exist.')
        return 'NULL'