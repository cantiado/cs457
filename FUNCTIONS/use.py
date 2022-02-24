# Author: Carl Antiado
# Last Updated: 2/10/2022
# Created 2/10/2022

# USE <db_name>
# db_name: <string>

import os

def use(db_name: str) -> str:
    cwd = os.getcwd()
    db_path = os.path.join(cwd,db_name)
    if os.path.isdir(db_path):
        print(f'Using database {db_name}.')
        return db_name
    else:
        print(f'!Failed to select database {db_name} because it does not exist.')
        return 'NULL'