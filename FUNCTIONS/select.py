# Author: Carl Antiado
# Last Updated: 2/12/2022
# Created 2/12/2022

# SELECT <col_list> FROM <tb_name>
# col_list: <column> <datatype> | <column> <datatype> <col_list>
# column: <string>
# datatype: int | float | char(<int>) | varchar(<int>)
# tb_name: <string>

from hashlib import new
import os
import errno

def select(args: str, db = 'NULL'):
    if 'FROM' not in args.upper():
        print('!Failed to perform command because it is missing keyword FROM.')
        return
    col_list = args[:args.upper().index('FROM')]
    tb_name = args[args.upper().index('FROM') + 4:]
    #col_list, tb_name = args.split('FROM',1)
    col_list = col_list.strip()
    tb_name = tb_name.strip()
    if col_list == '' or tb_name == '':
        print('!Failed to perform command because it is missing arguments.')
        return
    if db == 'NULL':
        print(f'!Failed to query table {tb_name} because a database was not selected.')
        return
    cwd = os.getcwd()
    db_path = os.path.join(cwd,db)
    if not os.path.isdir(db_path):
        print(f'!Failed to query table {tb_name} because database {db} does not exist.')
        return
    
    tb_path = os.path.join(db_path,tb_name)
    if col_list == '*':
        try:
            with open(tb_path, 'r', newline='') as table:
                for row in table:
                    print(row.replace(',', ' | '))
        except OSError as error:
            if error.errno == errno.ENOENT:
                print(f'!Failed to query table {tb_name} because it does not exist.')
            else:
                print(error.errno, error)
            return
    else:
        col_list = col_list.split(',')
        for entry in col_list:
            column, datatype = entry.strip().split(maxsplit=1)
            x = column + ' ' + datatype.replace(' ','')
            col_list[col_list.index(entry)] = x
        #print(col_list)
        tb_matrix = list()
        try:
            with open(tb_path, 'r', newline='') as table:
                for row in table:
                    tb_matrix.append(row.split(','))
        except OSError as error:
            if error.errno == errno.ENOENT:
                print(f'!Failed to query table {tb_name} because it does not exist.')
            else:
                print(error.errno, error)
            return
        #print(tb_matrix)
        col_index = list()
        for col in col_list:
            if col in tb_matrix[0]:
                col_index.append(tb_matrix[0].index(col))
        if len(col_index) == 0:
            print(f'!Failed to query table {tb_name} because no valid columns were given.')
            return
        if len(col_index) == 1:
            for row in tb_matrix:
                print(row[col_index[0]])
        else:
            for row in tb_matrix:
                s = ''
                for i in col_index:
                    s += row[i] + ' | '
                print(s.removesuffix(' | '))


def main():
    select('* from tb1', 'db1')
    select('   test    varchar  (  2  )   ,   another    int    FROM   tb1', 'db1')

if __name__ == '__main__':
    main()