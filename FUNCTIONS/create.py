# Author: Carl Antiado
# Last Updated: 2/10/2022
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

# datatypes

def create(args: str, db = 'NULL'):
    args = args.strip()
    try:
        object_type, args = args.split(' ', 1)
    except ValueError:
        print('!Failed to perform command because it is missing arguments.')
        return
    if object_type.upper() == 'DATABASE':
        object_name = args.strip()
        try:
            cwd = os.getcwd()
            db_path = os.path.join(cwd,object_name)
            os.mkdir(db_path)
            print(f'Database {object_name} created.')
        except OSError as error:
            if error.errno == errno.EINVAL:
                print(f'!Failed to create database {object_name} because of invalid syntax.')
            elif error.errno == errno.EEXIST:
                print(f'!Failed to create database {object_name} because it already exits.')
            else:
                print(error.errno, error)

    if object_type.upper() == 'TABLE':
        object_name = args[:args.find('(')]
        object_name = object_name.strip()
        col_list = args[args.find('('):]
        col_list = col_list.strip()

        if not (col_list.startswith('(') and col_list.endswith(')')):
            print(f'!Failed to create table {object_name} because of invalid argument syntax.')
            return

        col_list = col_list.removeprefix('(')
        col_list = col_list.removesuffix(')')

        if db == 'NULL':
            print(f'Failed to create table {object_name} because a database was not selected.')
            return
        else:
            cwd = os.getcwd()
            db_path = os.path.join(cwd,db)
            tb_path = os.path.join(db_path,object_name)
            if os.path.isfile(tb_path):
                print(f'!Failed to create table {object_name} because it already exists.')
                return
            try:
                col_list = col_list.split(',')
                header = ''
                for entry in col_list:
                    column, datatype = entry.split(maxsplit=1)
                    column = column.strip()
                    datatype = datatype.strip()
                    if '(' in datatype and ')' in datatype:
                        # char(<int>), varchar(<int>)
                        datatype, str_length = datatype.replace(' ','').replace('(',' ').replace(')','').split()
                        try:
                            if datatype == 'char':
                                if 0 <= int(str_length) <= 255:
                                    header += f'{column} {datatype}({str_length}),'

                            elif datatype == 'varchar':
                                if 0 <= int(str_length) <= 65535:
                                    header += f'{column} {datatype}({str_length}),'
                            else:
                                print(f'!Failed to create table {object_name} because of invalid an datatype.')
                                return
                        except ValueError as error:
                            print(f'!Failed to create table {object_name} because of invalid string length.')
                            return
                    elif datatype == 'int' or datatype == 'float':
                        header += f'{column} {datatype},'
                    else:
                        print(f'!Failed to create table {object_name} because of invalid an datatype.')
                        return
                header = header.removesuffix(',')
                with open(tb_path,'w') as tb:
                    tb.write(header)
                    print(f'Table {object_name} created.')
            except OSError as error:
                if error.errno == errno.ENOENT:
                    print(f'!Failed to create table {object_name} because database {db} was not found.')
                else:
                    print(error.errno, error)
            except ValueError:
                print(f'!Failed to create table {object_name} because of invalid number of arguments.')



# test script

def main():
    db = ' database       db1'
    create(db)
    tb = '   table     tb1    (   test    varchar (  2 )   ,    another  int  )'
    create(tb,'db1')

if __name__ == '__main__':
    main()