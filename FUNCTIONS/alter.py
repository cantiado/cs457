# Author: Carl Antiado
# Last Updated: 3/16/2022
# Created 2/22/2022

# ALTER TABLE <tb_name> ADD <column> <datatype>
# tb_name: <string>
# column: <string>
# datatype: int | float | char(<int>) | varchar(<int>)

import os
import errno
from constants import DATATYPES

def alter(tokens: list[str], db = 'NULL') -> None:
    # fail if missing arguments, no database selected, database does not exist,
    #   or table does not exist
    if len(tokens) < 5:
        print('!Failed to alter table because of missing arguments')
        return
    if tokens.pop(0).upper() != 'TABLE':
        print('!Failed to alter table because of missing keyword TABLE.')
        return
    tb_name = tokens.pop(0)
    if tokens.pop(0).upper() != 'ADD':
        print('!Failed to alter table because of missing keyword ADD.')
        return
    if db == 'NULL':
        print(f'!Failed to alter table {tb_name} because a database was not selected.')
        return
    cwd = os.getcwd()
    db_path = os.path.join(cwd,db)
    if not os.path.isdir(db_path):
        print(f'!Failed to alter table {tb_name} because database {db} does not exist.')
        return
    tb_path = os.path.join(db_path,tb_name)
    if not os.path.isfile(tb_path):
        print(f'!Failed to alter table {tb_name} because table {tb_name} does not exist.')
        return
    column =  tokens.pop(0)
    datatype = tokens.pop(0)
    # fail if invalid datatype
    if datatype not in DATATYPES:
        print(f'!Failed to alter table {tb_name} because {datatype} is not a valid datatype.')
        return
    
    col_str = f' | {column} {datatype}'
    if datatype in {'char','varchar'}:
        # fail if missing parameter for datatype, or invalid parameter
        if len(tokens) < 3:
            print(f'!Failed to alter table {tb_name} because of missing parameter for datatype {datatype}.')
            return
        if len(tokens) > 3:
            print(f'!Failed to alter table {tb_name} because of too many parameter arguments for datatype {datatype}.')
            return
        if tokens[0] != '(' or tokens[2] != ')':
            print(f'!Failed to alter table {tb_name} because of missing parameter parentheses.')
            return
        try:
            str_len = int(tokens[1])
        except ValueError:
            print(f'!Failed to alter table {tb_name} because expected <int> but got {tokens[1]} instead.')
            return
        if datatype == 'char' and not (0 <= str_len <= 255):
            print(f'!Failed to alter table {tb_name} because {str_len} not between 0 and 255.')
            return
        if datatype == 'varchar' and not (0 <= str_len <= 65535):
            print(f'!Failed to alter table {tb_name} because {str_len} not between 0 and 65535.')
            return
        # valid parameter so append parameter
        col_str += f'({str_len})'
    # add column to table
    with open(tb_path,'r') as tb_file:
        # get the table rows
        table = tb_file.readlines()
    # append new column
    for i in range(len(table)):
        if i == 0:
            table[i] += col_str
        else:
            table[i] += ' | '
    # write table to file
    with open(tb_path,'w') as tb_file:
        tb_file.writelines(table)
    print(f'Table {tb_name} modified.')

# test script

def main():
    tokens = 'TABLE tb1 ADD a3 float'.split()
    alter(tokens, 'db1')

if __name__ == '__main__':
    main()