# Author: Carl Antiado
# Last Updated: 2/10/2022
# Created 2/10/2022

# DROP <object_type> <object_name>
# object_type: DATABASE | TABLE
# object_name: <string>

import os
import errno

def drop(args: str, db = 'NULL'):
    try:
        object_type, object_name = args.split(' ', 1)
    except ValueError as error:
        print('!Failed to perform command because it is missing arguments.')
        return
    if object_type.upper() == 'DATABASE':
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
    if object_type.upper() == 'TABLE':
        if db == 'NULL':
            print(f'!Failed to delete table {object_name} because a database was not selected.')
            return
        else:
            cwd = os.getcwd()
            db_path = os.path.join(cwd,db)
            tb_path = os.path.join(db_path,object_name)
            try:
                os.remove(tb_path)
                print(f'Table {object_name} deleted.')
            except OSError as error:
                if error.errno == errno.ENOENT:
                    print(f'!Failed to delete table {object_name} because it does not exist.')
                else:
                    print(error.errno, error)


def main():
    tb = 'table tb1'
    drop(tb, 'db1')
    db = 'database db1'
    drop(db)

if __name__ == '__main__':
    main()