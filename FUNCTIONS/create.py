# Author: Carl Antiado
# Last Updated: 4/16/2022
# Created 2/10/2022

import os
import errno

from . import utility
from .utility import make_table, is_int, DATATYPES

'''
CREATE: <object_type>
object_type: DATABASE <db_name> | TABLE <tb_name> (<header>)
db_name: <string>
tb_name: <string>
header: <col_name> <data_type> | <col_name> <data_type> <header>
col_name: <string>
data_type: int | float | char(<max_len>) | varchar(<max_len>)
max_len: <int>
'''

'''
Creates either a database or table in a database.
'''
def create(tokens: list[str], db: str = 'NULL') -> None:
    object_type = tokens.pop(0)
    if object_type.upper() == 'DATABASE':
        create_database(tokens)
    elif object_type.upper() == 'TABLE':
        if db == 'NULL':
            print('!Failed to create table because no database was selected.')
            return
        create_table(tokens, db)
    else:
        pass

def create_database(tokens: list[str]) -> None:
    # Check for appropriate number of tokens.
    # Exactly one token, the db_name, is expected.
    if len(tokens) == 0:
        print('!Failed to create database because of missing database name.')
        return
    if len(tokens) > 1:
        print('!Failed to create database because of too many arguments.')
        return
    db_name = tokens.pop()
    # Check that db_name is not NULL.
    if db_name == 'NULL':
        print('!Failed to create database because NULL is not a valid name.')
        return
    cwd = os.getcwd()
    db_path = os.path.join(cwd, db_name)
    # Check that directory db_name does not already exist.
    if os.path.isdir(db_path):
        print(f'!Failed to create database {db_name} because it already exists.')
        return
    try:
        os.mkdir(db_path)
    except OSError as error:
        # Handle exceptions.
        if error.errno == errno.EINVAL:
            print(f'!Failed to create database {db_name} because of invalid syntax.')
        else:
            print(error.errno, error)
        return
    print(f'Database {db_name} created.')

def create_table(tokens: list[str], db: str) -> None:
    # Check for minimum of 5 tokens.
    if len(tokens) < 5:
        print('!Failed to create table because of missing arguments.')
        return
    # Check that directory db exists.
    cwd = os.getcwd()
    db_path = os.path.join(cwd, db)
    if not os.path.isdir(db_path):
        print(f'!Failed to create table because it database {db} no longer exists.')
        return
    # Check if table tb_name already exists.
    tb_name = tokens.pop(0)
    tb_path = os.path.join(db_path, tb_name)
    if os.path.isfile(tb_path):
        print(f'!Failed to create table {tb_name} because it already exists.')
        return
    # Check for starting parenthesis.
    if tokens.pop(0) != '(':
        print('!Failed to create table because of missing parenthesis before columns.')
        return
    # Get all column headings.
    header = []
    last_delim = ''
    while len(tokens) >= 3:
        col_name = tokens.pop(0)
        data_type = tokens.pop(0)
        # Check if data_type is valid.
        if data_type not in DATATYPES:
            print(f'!Failed to create table {tb_name} because of invalid data type {data_type}.')
        # Get and check if valid max_len for char or varchar.
        if data_type in {'char', 'varchar'}:
            # Must be at least 4 tokens: ( <int> ) ...
            if len(tokens) < 4:
                print(f'!Failed to create table {tb_name} because of missing arguments after {col_name} {data_type}.')
                return
            if tokens.pop(0) != '(':
                print(f"!Failed to create table {tb_name} because of missing '(' after {col_name} {data_type}.")
                return
            max_len = tokens.pop(0)
            if not is_int(max_len):
                print(f'!Failed to create table {tb_name} because of unexpected {max_len} when expecting an <int>.')
                return
            max_len = int(max_len)
            if tokens.pop(0) != ')':
                print(f"!Failed to create table {tb_name} because of missing '(' after {col_name} {data_type}({max_len}.")
                return
            if data_type == 'char':
                if not (0 <= max_len <= 255):
                    print(f'!Failed to create table {tb_name} because of invalid max length {max_len}.')
                    return
            else:
                if not (0 <= max_len <= 65535):
                    print(f'!Failed to create table {tb_name} because of invalid max length {max_len}.')
                    return
            # Append valid header.
            header.append((col_name, (DATATYPES[data_type], max_len)))
        # Append valid header.
        else:
            header.append((col_name, DATATYPES[data_type]))
        # Save last delimiter (either ',' or ')').
        last_delim = tokens.pop(0)
        # Check if its a valid delimiter.
        if last_delim not in {',',')'}:
            print(f"!Failed to create table {tb_name} because of a missing ',' or ')' after a column entry.")
            return
    # Check if ended correctly.
    if len(tokens) != 0:
        if last_delim == ')':
            print(f'!Failed to create table {tb_name} because of unexpected arguments after closing parenthesis after columns.')
        else:
            print(f'!Failed to create table {tb_name} because of missing arguments in columns.')
        return
    elif last_delim != ')':
        print(f"!Failed to create table {tb_name} because of missing expected ')' after columns.")
        return
    else:
        make_table(tb_path, header)
        print(f'Table {tb_name} created.')

# Test Script
def main():
    db = 'database Test'
    create(db.split())
    tb = 'table test ( a1 int , a2 float , a3 char ( 200 ) , a4 varchar ( 1000 ) )'
    create(tb.split(),'Test')

if __name__ == '__main__':
    main()