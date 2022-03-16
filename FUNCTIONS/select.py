# Author: Carl Antiado
# Last Updated: 2/12/2022
# Created 2/12/2022

# SELECT <col_list> FROM <tb_name>
# col_list: <string> | <string> , <col_list>
# tb_name: <string>

import os
import errno
from constants import DATATYPES

def select(tokens: list[str], db = 'NULL') -> None:
    # fail if too few tokens, no database selected, or database does not exist
    if len(tokens) < 3:
        print('!Failed to query table because of missing arguments.')
        return
    if db == 'NULL':
        print('!Failed to query table because a database was not selected.')
        return
    cwd = os.getcwd()
    db_path = os.path.join(cwd,db)
    if not os.path.isdir(db_path):
        print(f'!Failed to query table because database {db} does not exist.')
        return
    # extract all column names until FROM
    col_list = [tokens.pop(0)]
    delim = tokens.pop(0)
    while delim == ',' and len(tokens) > 1:
        col_list.append(tokens.pop(0))
        delim = tokens.pop(0)
    # fail if delim is not keyword FROM, incorrect number of arguments, or table does not exist
    if delim.upper() != 'FROM':
        print('!Failed to query table because of expected keyword FROM after columns.')
        return
    if len(tokens) < 1:
        print('!Failed to query table because of missing table name.')
        return
    if len(tokens) > 1:
        print('!Failed to query table because of too many arguemnts.')
        return
    tb_name = tokens.pop()
    tb_path = os.path.join(db_path,tb_name)
    if not os.path.isfile(tb_path):
        print(f'!Failed to query table {tb_name} because it does not exist.')
        return
    # select columns from table
    # check if column is in table, fail otherwise
    # if wildcard is in column list, select all columns
    with open(tb_path,'r') as tb_file:
        table = tb_file.readlines()
    # header example: ['a1','int','|','a2','char(2)','|','a3','float']
    #   column name is every third element, i.e., i=0,3,6,...
    header = table[0].split()[0::3]
    index = []
    for col in col_list:
        if col in header:
            # record index of desired column in table if not already recorded
            if header.index(col) not in index:
                index.append(header.index(col))
        elif col == '*':
            # final check for wildcards at end
            pass
        else:
            print(f'!Failed to query table {tb_name} because column {col} is not in table.')
            return
    # pif wildcard in column list, print entire table
    # otherwise print desired columns
    if '*' in col_list:
        for row in table:
            print(row)
    else:
        for row in table:
            row = row.split(' | ')
            row_str = ''
            for i in index:
                row_str += f'{row[i]} | '
            print(row_str.removesuffix(' | '))

def main():
    tokens = '* from tb1'.split()
    select(tokens, 'db1')
    tokens = 'wrong from tb1'.split()
    select(tokens, 'db1')
    tokens = 'another , test from tb1'.split()
    select(tokens, 'db1')

if __name__ == '__main__':
    main()