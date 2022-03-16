# Author: Carl Antiado
# Last Updated: 2/10/2022
# Created 2/10/2022

# DROP <object_type> <object_name>
# object_type: DATABASE | TABLE
# object_name: <string>

import os
import errno

def drop(tokens: list[str], db = 'NULL') -> None:
    # fail if not exactly 2 tokens
    if len(tokens) < 2:
        print('!Failed to perform command because of missing arguments.')
        return
    if len(tokens) > 2:
        print('!Failed to perform command because of too many arguments.')
        return
    
    # determine object_type from first token,
    # object_name from last token
    object_type = tokens.pop(0)
    object_name = tokens.pop()
    if object_type.upper() == 'DATABASE':
        # fail if database does not exist or is not empty
        # otherwise delete database
        cwd = os.getcwd()
        db_path = os.path.join(cwd,object_name)
        try:
            os.rmdir(db_path)
            print(f'Database {object_name} deleted.')
        except OSError as error:
            if error.errno == errno.ENOENT:
                print(f'!Failed to delete database {object_name} because it does not exist.')
            elif error.errno == errno.ENOTEMPTY:
                print(f'!Failed to delete database {object_name} because it is not empty.')
            else:
                print(error.errno, error)

    elif object_type.upper() == 'TABLE':
        # fail if no database selected or if table does not exist
        # otherwise delete table
        if db == 'NULL':
            print(f'!Failed to delete table {object_name} because a database was not selected.')
            return
        cwd = os.getcwd()
        tb_path = os.path.join(cwd,db,object_name)
        try:
            os.remove(tb_path)
            print(f'Table {object_name} deleted.')
        except OSError as error:
            if error.errno == errno.ENOENT:
                print(f'!Failed to delete table {object_name} because it does not exist.')
            else:
                print(error.errno, error)

# test script

def main():
    tb = 'table tb1'
    drop(tb.split(), 'db1')
    db = 'database db1'
    drop(db.split())

if __name__ == '__main__':
    main()