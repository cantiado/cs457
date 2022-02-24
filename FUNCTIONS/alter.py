# Author: Carl Antiado
# Last Updated: 2/22/2022
# Created 2/22/2022

# ALTER TABLE <tb_name> ADD <column> <datatype>
# tb_name: <string>
# column: <string>
# datatype: int | float | char(<int>) | varchar(<int>)

import os
import errno

def alter(args: str, db = 'NULL'):
    if 'TABLE' not in args.upper():
        print('!Failed to perform command because it is missing keyword TABLE.')
        return
    if 'ADD' not in args.upper():
        print('!Failed to perform command because it is missing keyword ADD.')
        return
    if db == 'NULL':
        print(f'!Failed to query table {tb_name} because a database was not selected.')
        return
    args = args[args.upper().index('TABLE') + 5:].strip()
    tb_name = args[:args.upper().index('ADD')].strip()
    column, datatype = args[args.upper().index('ADD') + 3:].split(maxsplit=1)
    column = column.strip()
    datatype = datatype.strip()
    cwd = os.getcwd()
    db_path = os.path.join(cwd,db)
    if not os.path.isdir(db_path):
        print(f'!Failed to query table {tb_name} because database {db} does not exist.')
        return
    tb_path = os.path.join(db_path,tb_name)
    try:
        line = ''
        with open(tb_path, 'r', newline='') as table:
            # only reading in first line for now
            line = table.readline()
        line += f',{column} {datatype}'
        with open(tb_path, 'w', newline='') as table:
            table.write(line)
        print(f'Table {tb_name} modified.')
    except OSError as error:
        if error.errno == errno.ENOENT:
            print(f'!Failed to query table {tb_name} because it does not exist.')
        else:
            print(error.errno, error)
        return

def main():
    alter('TABLE tb1 ADD a3 float', 'db1')

if __name__ == '__main__':
    main()