# Author: Carl Antiado
# Last Updated: 3/27/2022
# Created 3/19/2022

# UPDATE <tb_name> SET <col_name> = <value> WHERE <col_name> = <value>
# tb_name: <string>
# col_name: <string>
# value: <int> | <float> | '<string>'

import os

def update(tokens: list[str], db = 'NULL') -> None:
    # fail if wrong number of arguments, database not selected, database does not exist,
    #   table does not exist, or missing keywords
    if len(tokens) != 9:
        print('!Failed to update table because of missing arguments.')
        return
    if db == 'NULL':
        print('!Failed to update table because no database was selected.')
        return
    cwd = os.getcwd()
    db_path = os.path.join(cwd,db)
    if not os.path.isdir(db_path):
        print(f'!Failed to update table because database {db} does not exist.')
        return
    tb_name = tokens.pop(0)
    tb_path = os.path.join(db_path,tb_name)
    if not os.path.isfile(tb_path):
        print(f'!Failed to update table {tb_name} because it does not exist.')
        return
    if tokens.pop(0).upper() != 'SET':
        print(f'!Failed to update table {tb_name} because of missing keyword SET after {tb_name}.')
        return
    target_col = tokens.pop(0)
    if tokens.pop(0) != '=':
        print(f'!Failed to update table {tb_name} because of missing = after {target_col}.')
        return
    new_value = tokens.pop(0)
    if tokens.pop(0).upper() != 'WHERE':
        print(f'!Failed to update table {tb_name} because of missing keyword WHERE after {new_value}.')
        return
    search_col = tokens.pop(0)
    if tokens.pop(0) != '=':
        print(f'!Failed to update table {tb_name} because of missing = after {search_col}.')
        return
    search_val = tokens.pop()

    # get table
    with open(tb_path,'r') as tb_file:
        table = tb_file.readlines()
    # extract column names and datatypes
    col_names = table[0].split()[0::3]
    datatypes = table[0].split()[1::3]
    # fail if target column not in table, new value is of wrong datatype,
    #   search column is not in table, or search value is of wrong datatype
    if target_col not in col_names:
        print(f'!Failed to update table {tb_name} because column {target_col} is not in the table.')
        return
    target_index = col_names.index(target_col)
    if datatypes[target_index] == 'int' and not new_value.isdigit():
        print(f'!Failed to update table {tb_name} because attempting to assign {new_value} when expecting int.')
        return
    elif datatypes[target_index] == 'float' and not __isfloat(new_value):
        print(f'!Failed to update table {tb_name} because attempting to assign {new_value} when expecting float.')
        return
    elif 'char' in datatypes[target_index]:
        if new_value[0] != new_value[-1] != "'":
            print(f'!Failed to update table {tb_name} because attempting to assign {new_value} when expecting {datatypes[target_index]}.')
            return
        str_len = int(datatypes[target_index][datatypes[target_index].find('(') + 1 : datatypes[target_index].find(')')])
        if len(new_value) > str_len + 2:
            print(f'!Failed to update table {tb_name} because {new_value} exceeds character count {str_len}.')
            return
    if search_col not in col_names:
        print(f'!Failed to update table {tb_name} because column {search_col} is not in the table.')
        return
    search_index = col_names.index(search_col)
    if datatypes[search_index] == 'int' and not search_val.isdigit():
        print(f'!Failed to update table {tb_name} because attempting to assign {search_val} when expecting int.')
        return
    elif datatypes[search_index] == 'float' and not __isfloat(search_val):
        print(f'!Failed to update table {tb_name} because attempting to assign {search_val} when expecting float.')
        return
    elif 'char' in datatypes[search_index]:
        if search_val[0] != search_val[-1] != "'":
            print(f'!Failed to update table {tb_name} because attempting to assign {search_val} when expecting {datatypes[search_index]}.')
            return
        str_len = int(datatypes[search_index][datatypes[search_index].find('(') + 1 : datatypes[search_index].find(')')])
        if len(search_val) > str_len + 2:
            print(f'!Failed to update table {tb_name} because {search_val} exceeds character count {str_len}.')
            return
    # separate table rows into columns
    for i in range(len(table)):
        table[i] = table[i].split(' | ')
    # update columns with new value
    counter = 0
    for i in range(1,len(table)):
        if table[i][search_index] == search_val:
            table[i][target_index] = new_value
            counter += 1
    # write new table to table file
    with open(tb_path,'w') as tb_file:
        for row in table:
            new_row = ''
            for col in row:
                new_row += f'{col} | '
            new_row = new_row.removesuffix(' | ')
            new_row = new_row.removesuffix('\n') + '\n'
            tb_file.write(new_row)
    if counter == 1:
        print('1 record modified.')
    else:
        print(f'{counter} records modified.')
        
def __isfloat(num: str) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False