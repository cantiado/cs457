# Author: Carl Antiado
# Last Updated: 3/27/2022
# Created 2/10/2022

# CREATE <object_type> <object_name> (<col_list>)
# object_type: DATABASE | TABLE
# object_name: <string>
# col_list: <column> <datatype> | <column> <datatype> <col_list>
# column: <string>
# datatype: int | float | char(<int>) | varchar(<int>)

# Notes: (<col_list>) is only for object_type = TABLE

import os
import errno

DATATYPES = {'int','float','char','varchar'}

def create(tokens: list[str], db = 'NULL') -> None:
    # fail if no tokens
    if len(tokens) == 0:
        print('!Failed to create table because of missing arguments.')
        return
    
    # determine object_type from first token
    object_type = tokens.pop(0)
    if object_type.upper() == 'DATABASE':
        # fail if not only one token remaining, or attempting to use name 'NULL'
        # otherwise create database with last token as database name
        if len(tokens) == 0:
            print('!Failed to create database because of missing database name.')
            return
        elif len(tokens) != 1:
            print('!Failed to create database because of too many arguments.')
            return
        elif tokens[0] == 'NULL':
            print('!Failed to create database because NULL is a reserved database name.')
            return
        else:
            object_name = tokens.pop()
            cwd = os.getcwd()
            db_path = os.path.join(cwd,object_name)
            try:
                os.mkdir(db_path)
            except OSError as error:
                if error.errno == errno.EINVAL:
                    print(f'!Failed to create database {object_name} because of invalid syntax.')
                elif error.errno == errno.EEXIST:
                    print(f'!Failed to create database {object_name} because it already exits.')
                else:
                    print(error.errno, error)
                return
            print(f'Database {object_name} created.')
            
    elif object_type.upper() == 'TABLE':
        # fail if not more than 3 tokens (object_name and both parentheses),
        #   database was not selected, database does not exist, or table already exists
        # otherwise attempt to create table
        if len(tokens) <= 3:
            print('!Failed to create table because of missing arguments.')
            return
        elif db == 'NULL':
            print(f'Failed to create table because a database was not selected.')
            return
        cwd = os.getcwd()
        db_path = os.path.join(cwd,db)
        if not os.path.isdir(db_path):
            print(f'!Failed to create table because database {db} does not exist.')
            return
        object_name = tokens.pop(0)
        tb_path = os.path.join(db_path,object_name)
        if os.path.isfile(tb_path):
            print(f'!Failed to create table {object_name} because it already exists.')
            return
        # fail if invalid syntax or datatype in col_list
        if tokens.pop(0) != '(':
            print(f"!Failed to create table {object_name} because of missing '(' before columns.")
            return
        # initialize col_list to empty
        col_list = ''
        while len(tokens) != 0: # verify all datatypes are valid
            try:
                column = tokens.pop(0)
                datatype = tokens.pop(0)
                if datatype not in DATATYPES:
                    print(f'!Failed to create table {object_name} because of invalid datatype {datatype}.')
                    return
                if datatype in {'char','varchar'}:
                    # fail if missing parameter or invalid parameter
                    if tokens[0] != '(' or tokens[2] != ')':
                        print(f'!Failed to create table {object_name} because column datatype {datatype} is missing parameter parentheses.')
                        return
                    try:
                        str_len = int(tokens[1])
                    except ValueError:
                        print(f'!Failed to create table {object_name} because expected <int> but got {tokens[1]} instead.')
                        return
                    if datatype == 'char' and not (0 <= str_len <= 255):
                        print(f'!Failed to create table {object_name} because {str_len} not between 0 and 255.')
                        return
                    if datatype == 'varchar' and not (0 <= str_len <= 65535):
                        print(f'!Failed to create table {object_name} because {str_len} not between 0 and 65535.')
                        return
                    col_list += f'{column} {datatype}({str_len})'
                    tokens = tokens[3:]
                else:
                    col_list += f'{column} {datatype}'
                col_list += ' | '
                delimiter = tokens.pop(0)
                # check to see if delimiter makes sense
                if len(tokens) > 0 and delimiter != ',':
                    print(f"!Failed to create table {object_name} because missing ',' between columns.")
                    return
                if len(tokens) == 0 and delimiter != ')':
                    print(f"!Failed to create table {object_name} because missing terminating ')' after columns.")
                    return
            # for whatever reason, fail if ran out of tokens unexpectedly
            except IndexError:
                print(f'!Failed to create table {object_name} because missing arguments in columns.')
                return
        # remove extra separator
        col_list = col_list.removesuffix(' | ') + '\n'
        # create table
        with open(tb_path,'w') as tb:
            tb.write(col_list)
        print(f'Table {object_name} created.')
    
    else:
        # invalid object_type
        print('!Invalid command.')

# test script

def main():
    db = 'database db1'
    create(db.split())
    tb = 'table tb1 ( test varchar ( 2 ) , another int )'
    create(tb.split(),'db1')

if __name__ == '__main__':
    main()