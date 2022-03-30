# Author: Carl Antiado
# Last Updated: 3/27/2022
# Created 3/19/2022

# INSERT INTO <tb_name> VALUES (<val_list>)
# tb_name: <string>
# val_list: <value> | <value> , <val_list>
# value: <int> | <float> | '<string>'

import os

def insert(tokens: list[str], db = 'NULL') -> None:
    # fail if missing arguments, database not selected, database does not exist,
    #   missing keywords, table does not exist
    if len(tokens) < 6:
        print('!Failed to insert into table because of missing arguments.')
        return
    if db == 'NULL':
        print('!Failed to insert into table because no database was selected.')
        return
    cwd = os.getcwd()
    db_path = os.path.join(cwd,db)
    if not os.path.isdir(db_path):
        print(f'!Failed to insert into table because database {db} does not exist.')
        return
    if tokens.pop(0).upper() != 'INTO':
        print('!Failed to insert into table because of missing keyword INTO.')
        return
    tb_name = tokens.pop(0)
    tb_path = os.path.join(db_path,tb_name)
    if not os.path.isfile(tb_path):
        print(f'!Failed to insert into table {tb_name} because it does not exist.')
        return
    if tokens.pop(0).upper() != 'VALUES':
        print(f'!Failed to insert into table {tb_name} because of missing keyword VALUES.')
        return
    # fail if missing starting parethesis, value type does not match column type,
    #   or missing terminating parenthesis
    if tokens.pop(0) != '(':
        print(f'!Failed to insert into table {tb_name} because of missing starting parenthesis.')
        return
    # select rows from table
    with open(tb_path,'r',newline='') as tb_file:
        table = tb_file.readlines()
    # header example: ['a1','int','|','a2','char(2)','|','a3','float']
    #   column datatype is every third element starting with 2nd element, i.e., i=1,4,7,...
    col_datatype = table[0].split()[1::3]
    # verify value matches column datatype
    new_row = ''
    for dt in col_datatype:
        # checking value datatype
        if len(tokens) < 2:
            print(f'!Failed to insert into table {tb_name} because of missing values.')
            return
        value = tokens.pop(0)
        if dt == 'int' and value.isdigit():
            new_row += f'{value} | '
        elif dt == 'float' and __isfloat(value):
            new_row += f'{value} | '
        elif 'char' in dt and value[0] == value[-1] == "'":
            str_len = int(dt[dt.find('(') + 1 : dt.find(')')])
            if len(value) > str_len + 2:
                print(f'!Failed to insert into table {tb_name} because {value} exceeds character count {str_len}.')
                return
            new_row += f'{value} | '
        else:
            print(f'!Failed to insert into table {tb_name} because expected {dt} but got {value}.')
            return
        # checking for comma or parenthesis
        delim = tokens.pop(0)
        if len(tokens) == 0 and delim != ')':
            print(f"!Failed to insert into table {tb_name} because expected ')' after values.")
            return
        elif len(tokens) > 0 and delim != ',':
            print(f"!Failed to insert into table {tb_name} because expected ',' after value {value}.")
            return
        else:
            # syntax is correct so do nothing
            pass
    # tokens should be empty, otherwise too many values
    if len(tokens) != 0:
        print(f'!Failed to insert into table {tb_name} because of too many values.')
        return
    new_row = new_row.removesuffix(' | ') + '\n'
    table.append(new_row)
    # update table file with new row
    with open(tb_path,'w') as tb_file:
        tb_file.writelines(table)
    print('1 new recored inserted.')

def __isfloat(num: str) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False