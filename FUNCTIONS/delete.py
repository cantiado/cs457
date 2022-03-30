# Author: Carl Antiado
# Last Updated: 3/28/2022
# Created 3/19/2022

# DELETE FROM <tb_name> WHERE <col_name> <logic> <value>
# tb_name: <string>
# col_name: <string>
# logic: = | >
# value: <int> | <float> | '<string>'

import os

def delete(tokens: list[str], db = 'NULL') -> None:
    if len(tokens) != 6:
        return
    if tokens.pop(0).upper() != 'FROM':
        return
    if db == 'NULL':
        return
    cwd = os.getcwd()
    db_path = os.path.join(cwd,db)
    if not os.path.isdir(db_path):
        return
    tb_name = tokens.pop(0)
    tb_path = os.path.join(db_path,tb_name)
    if not os.path.isfile(tb_path):
        return
    if tokens.pop(0).upper() != 'WHERE':
        return
    col_name = tokens.pop(0)
    logic = tokens.pop(0)
    value = tokens.pop()
    with open(tb_path,'r') as tb_file:
        table = tb_file.readlines()
    col_names = table[0].split()[0::3]
    for i in range(len(table)):
        table[i] = table[i].split(' | ')
    target_index = col_names.index(col_name)
    counter = 0
    #print(table)
    #print(target_index)
    del_index = []
    for i in range(1,len(table)):
        #print(i)
        #print(table[i][target_index])
        if logic == '=' and table[i][target_index] == value:
            del_index.append(i)
            counter += 1
        elif logic == '>' and float(table[i][target_index]) > float(value):
            del_index.append(i)
            counter += 1
    while len(del_index) > 0:
        table.pop(del_index.pop(0))
        for i in range(len(del_index)):
            del_index[i] -= 1
    with open(tb_path,'w') as tb_file:
        for row in table:
            new_row = ''
            for col in row:
                new_row += f'{col} | '
            new_row = new_row.removesuffix(' | ')
            new_row = new_row.removesuffix('\n') + '\n'
            tb_file.write(new_row)
    if counter == 1:
        print('1 record deleted.')
    else:
        print(f'{counter} records deleted.')