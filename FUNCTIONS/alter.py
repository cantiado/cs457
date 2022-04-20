# Author: Carl Antiado
# Last Updated: 4/16/2022
# Created 2/22/2022

'''
ALTER: TABLE <tb_name> ADD <col_name> <data_type>
tb_name: <string>
col_name: <string>
data_type: int | float | char(<max_len>) | varchar(<max_len>)
max_len: <int>
'''

import os

from . import utility
from .utility import is_int, get_table, make_table, DATATYPES, DEFAULT_VAL

def alter(tokens: list[str], db: str = 'NULL') -> None:
    # Check if minimum number of tokens is met.
    if len(tokens) < 5:
        print('!Failed to alter table because of missing arguments.')
        return
    # Check if a database was selected.
    if db == 'NULL':
        print('!Failed to alter table because no database was selected.')
        return
    # Check that database db exists.
    cwd = os.getcwd()
    db_path = os.path.join(cwd, db)
    if not os.path.isdir(db_path):
        print(f'!Failed to alter table because database {db} no longer exists.')
        return
    # Check for TABLE keyword.
    if tokens.pop(0).upper() != 'TABLE':
        print('!Failed to alter table because of missing keyword TABLE.')
        return
    # Check that table tb_name exists.
    tb_name = tokens.pop(0)
    tb_path = os.path.join(db_path, tb_name)
    if not os.path.isfile(tb_path):
        print(f'!Failed to alter table {tb_name} because it does not exist.')
        return
    # Check for ADD keyword.
    if tokens.pop(0).upper() != 'ADD':
        print('!Failed to alter table because of missing keyword ADD.')
        return
    # Check if data_type is valid
    col_name = tokens.pop(0)
    data_type = tokens.pop(0)
    if data_type not in DATATYPES:
        print(f'!Failed to alter table {tb_name} because of invalid data type {data_type}.')
        return
    # Get and check if valid max_len for char or varchar
    if data_type in {'char', 'varchar'}:
        # Must have 3 tokens left: ( <int> )
        if tokens.pop(0) != '(':
            print(f"!Failed to alter table {tb_name} because of missing '(' after {data_type}.")
            return
        max_len = tokens.pop(0)
        if not is_int(max_len):
            print(f'!Failed to alter table {tb_name} because of unexpected {max_len} when expecting <int>.')
            return
        max_len = int(max_len)
        if tokens.pop(0) != ')':
            print(f"!Failed to alter table {tb_name} because of missing ')' after {max_len}.")
            return
        if data_type == 'char':
            if not (0 <= max_len <= 255):
                print(f'!Failed to create table {tb_name} because of invalid max length {max_len}.')
                return
        else:
            if not (0 <= max_len <= 65535):
                print(f'!Failed to create table {tb_name} because of invalid max length {max_len}.')
                return
        # Create new column
        new_col = (col_name, (DATATYPES[data_type], max_len))
    # Create new column
    else:
        new_col = (col_name, DATATYPES[data_type])
    # Get header and rows from table
    header, rows = get_table(tb_path)
    header.append(new_col)
    # Add default values to new column
    for row in rows:
        row.append(DEFAULT_VAL[data_type])
    # Update table
    make_table(tb_path, header, rows)
    print(f'Table {tb_name} modified.')

# Test script
def main():
    tokens = 'TABLE test ADD a5 int'.split()
    alter(tokens, 'Test')

if __name__ == '__main__':
    main()