# Author: Carl Antiado
# Last Updated: 4/18/2022
# Created 2/12/2022

'''
SELECT: <col_list> <from_clause> [<where_clause>]
col_list: * | <col_name> | <col_name>,  <col_list>
from_clause: FROM <tb_name> | FROM <inner_join> | FROM <left_outer_join>
inner_join: <tb_name> <tb_alias>, <tb_name> <tb_alias> <on_condition> 
    | <tb_name> <tb_alias> INNER JOIN <tb_name> <tb_alias> <on_condition>
on_condition: ON <tb_alias>.<col_name> = <tb_alias>.<col_name>
left_outer_join: <tb_name> <tb_alias> LEFT OUTER JOIN <tb_name> <tb_alias> <on_condition>
where_clause: WHERE <col_name> <logic> <value>
col_name: <string>
tb_name: <string>
tb_alias: <string>
logic: !=
value: <int> | <float> | '<string>'
'''

import os

from . import utility
from .utility import is_cols_in_header, is_int, is_float, is_char, print_table
from .utility import get_table_at_cols, get_cols_indices, get_rows_where_cond, get_table, get_header_index
from .utility import WILDCARD, LOGIC

def select(tokens: list[str], db: str = 'NULL') -> None:
    # Check for minimum number of tokens: col_name FROM tb_name
    if len(tokens) < 3:
        print('!Failed to query table because of missing arguments.')
        return
    # Check if valid database was selected.
    if db == 'NULL':
        print('!Failed to query table because no table was selected.')
        return
    cwd = os.getcwd()
    db_path = os.path.join(cwd, db)
    if not os.path.isdir(db_path):
        print(f'!Failed to query table because database {db} no longer exists.')
        return
    # Get columns until FROM keyword.
    col_list = []
    next_token = tokens.pop(0)
    while len(tokens) >= 2 and next_token.upper() != 'FROM':
        # Must have at least one column
        if len(col_list) == 0:
            if next_token == ',':
                print("!Failed to query table because of missing first column before ','.")
                return
            col_list.append(next_token)
            next_token = tokens.pop(0)
        else:
            # Columns must be separated by commas
            if next_token != ',':
                print("!Failed to query table because of missing ',' between columns.")
                return
            next_token = tokens.pop(0)
            # Check if missing column between commas
            if next_token.upper() in {',', 'FROM'}:
                print("!Failed to query table because of missing column after ','.")
                return
            col_list.append(next_token)
            next_token = tokens.pop(0)
    # Check if at least one column was given.
    if len(col_list) == 0:
        print('!Failed to query table because no columns were given.')
        return
    # Check if last obtained token was keyword FROM
    if next_token.upper() != 'FROM':
        print('!Failed to query table because of missing keyword FROM after columns.')
        return
    # Get first table name
    tb_args = []
    next_token = tokens.pop(0)
    if next_token == 'WHERE':
        print('!Failed to query table because no table name was given.')
        return
    tb_args.append(next_token)
    # Get any other table arguments before keyword WHERE
    while len(tokens) != 0:
        next_token = tokens.pop(0)
        if next_token.upper() == 'WHERE':
            break
        tb_args.append(next_token)
    # Check that there are table arguments
    if len(tb_args) == 0:
        print('!Failed to query table because no table name was given.')
        return
    # Check if need to handle WHERE clause
    if next_token.upper() != 'WHERE':
        # No WHERE clause
        
        # Check which FROM clause we're in
        if len(tb_args) == 1:
            # Only 1 table. Check if table tb_name exists.
            tb_name = tb_args.pop(0)
            tb_path = os.path.join(db_path, tb_name)
            if not os.path.isfile(tb_path):
                print(f'!Failed to query table {tb_name} because it does not exist.')
                return
            # Get table.
            header, rows = get_table(tb_path)
            # Check if all columns in col_list in table header
            if not is_cols_in_header(col_list, header):
                print(f'!Failed to query table {tb_name} because a specified column is not in the table.')
                return
            # Check if wildcard was selected. If so, print table and return.
            if WILDCARD in col_list:
                print_table(header, rows)
                return
            # Get queried columns and print table at queried columns
            col_indices = get_cols_indices(header, col_list)
            header, rows = get_table_at_cols(header, rows, col_indices)
            print_table(header, rows)
            return
        elif len(tb_args) == 10:
            # Explicit inner join: tb_name1 tb_alias1 INNER JOIN tb_name2 tb_alias2 ON col1 logic col2
            tb_name1 = tb_args.pop(0)
            tb_alias1 = tb_args.pop(0)
            if tb_args.pop(0).upper() != 'INNER':
                print(f"!Failed to query table because of missing keyword INNER after {tb_name1} {tb_alias1}.")
                return
            if tb_args.pop(0).upper() != 'JOIN':
                print(f"!Failed to query table because of missing keyword JOIN after {tb_name1} {tb_alias1}.")
                return
            tb_name2 = tb_args.pop(0)
            tb_alias2 = tb_args.pop(0)
            table_alias = {tb_alias1: tb_name1, tb_alias2: tb_name2}
            # Check if tables are valid
            tb_path1 = os.path.join(db_path, tb_name1)
            tb_path2 = os.path.join(db_path, tb_name2)
            if not os.path.isfile(tb_path1):
                print(f'!Failed to query table {tb_name1} because it does not exist.')
                return
            if not os.path.isfile(tb_path2):
                print(f'!Failed to query table {tb_name2} because it does not exist.')
                return
            # Check for ON keyword
            if tb_args.pop(0).upper() != 'ON':
                print('!Failed to query table because of missing keyword ON in table arguments.')
                return
            # Get tables
            header1, rows1 = get_table(tb_path1)
            header2, rows2 = get_table(tb_path2)
            # Get condition cols
            col1 = tb_args.pop(0)
            logic = tb_args.pop(0)
            col2 = tb_args.pop(0)
            alias1, col_name1 = col1.split('.')
            alias2, col_name2 = col2.split('.')
            # Check if column is in table
            if alias1 == alias2:
                print('!Failed to query table because the same table alias was used twice.')
                return
            for alias, col in [(alias1, col_name1), (alias2, col_name2)]:
                if table_alias[alias] == tb_name1:
                    if not is_cols_in_header([col], header1):
                        print(f'!Failed to query table because {col} is not in {tb_name1}.')
                        return
                elif table_alias[alias] == tb_name2:
                    if not is_cols_in_header([col], header2):
                        print(f'!Failed to query table because {col} is not in {tb_name2}.')
                else:
                    print(f'!Failed to query table because alias {alias} does not match to a table.')
                    return
            # Get rows where condition is met
            index_c1 = get_cols_indices(header1, [col_name1]).pop()
            index_c2 = get_cols_indices(header2, [col_name2]).pop(0)
            new_header = header1 + header2
            new_rows = []
            for r1 in rows1:
                for r2 in get_rows_where_cond(rows2, index_c2, LOGIC[logic], r1[index_c1]):
                    new_rows.append(r1 + r2)
            # Check if all columns in col_list in table header
            #### Need to implement
            ##if not is_cols_in_header(col_list, header):
            ##    print(f'!Failed to query table {tb_name} because a specified column is not in the table.')
            ##   return
            # Check if wildcard was selected. If so, print table and return.
            if WILDCARD in col_list:
                print_table(new_header, new_rows)
                return
            # Get queried columns and print table at queried columns
            #### Need to implement
            ##col_indices = get_cols_indices(header, col_list)
            ##header, rows = get_table_at_cols(header, rows, col_indices)
            ##print_table(header, rows)
            return

        elif len(tb_args) == 11:
            # Left outer join: tb_name1 tb_alias1 LEFT OUTER JOIN tb_name2 tb_alias2
            tb_name1 = tb_args.pop(0)
            tb_alias1 = tb_args.pop(0)
            if tb_args.pop(0).upper() != 'LEFT':
                print(f"!Failed to query table because of missing keyword LEFT after {tb_name1} {tb_alias1}.")
                return
            if tb_args.pop(0).upper() != 'OUTER':
                print(f"!Failed to query table because of missing keyword OUTER after {tb_name1} {tb_alias1}.")
                return
            if tb_args.pop(0).upper() != 'JOIN':
                print(f"!Failed to query table because of missing keyword JOIN after {tb_name1} {tb_alias1}.")
                return
            tb_name2 = tb_args.pop(0)
            tb_alias2 = tb_args.pop(0)
            table_alias = {tb_alias1: tb_name1, tb_alias2: tb_name2}
            # Check if tables are valid
            tb_path1 = os.path.join(db_path, tb_name1)
            tb_path2 = os.path.join(db_path, tb_name2)
            if not os.path.isfile(tb_path1):
                print(f'!Failed to query table {tb_name1} because it does not exist.')
                return
            if not os.path.isfile(tb_path2):
                print(f'!Failed to query table {tb_name2} because it does not exist.')
                return
            # Check for ON keyword
            if tb_args.pop(0).upper() != 'ON':
                print('!Failed to query table because of missing keyword ON in table arguments.')
                return
            # Get tables
            header1, rows1 = get_table(tb_path1)
            header2, rows2 = get_table(tb_path2)
            # Get condition cols
            col1 = tb_args.pop(0)
            logic = tb_args.pop(0)
            col2 = tb_args.pop(0)
            alias1, col_name1 = col1.split('.')
            alias2, col_name2 = col2.split('.')
            # Check if column is in table
            if alias1 == alias2:
                print('!Failed to query table because the same table alias was used twice.')
                return
            for alias, col in [(alias1, col_name1), (alias2, col_name2)]:
                if table_alias[alias] == tb_name1:
                    if not is_cols_in_header([col], header1):
                        print(f'!Failed to query table because {col} is not in {tb_name1}.')
                        return
                elif table_alias[alias] == tb_name2:
                    if not is_cols_in_header([col], header2):
                        print(f'!Failed to query table because {col} is not in {tb_name2}.')
                else:
                    print(f'!Failed to query table because alias {alias} does not match to a table.')
                    return
            # Get rows where condition is met
            index_c1 = get_cols_indices(header1, [col_name1]).pop()
            index_c2 = get_cols_indices(header2, [col_name2]).pop(0)
            new_header = header1 + header2
            new_rows = []
            for r1 in rows1:
                true_rows2 = get_rows_where_cond(rows2, index_c2, LOGIC[logic], r1[index_c1])
                if len(true_rows2) != 0:
                    for r2 in true_rows2:
                        new_rows.append(r1 + r2)
                else:
                    new_rows.append(r1 + ['' for _ in header2])
            # Check if all columns in col_list in table header
            #### Need to implement
            ##if not is_cols_in_header(col_list, header):
            ##    print(f'!Failed to query table {tb_name} because a specified column is not in the table.')
            ##   return
            # Check if wildcard was selected. If so, print table and return.
            if WILDCARD in col_list:
                print_table(new_header, new_rows)
                return
            # Get queried columns and print table at queried columns
            #### Need to implement
            ##col_indices = get_cols_indices(header, col_list)
            ##header, rows = get_table_at_cols(header, rows, col_indices)
            ##print_table(header, rows)
            return
        
        
        
        else:
            print('!Failed to query table because of invalid table arguments.')
            return
        
    else:
        # Must handle WHERE clause
        
        # Check which FROM clause we're in
        if len(tb_args) == 1:
            # Only 1 table. Check if table tb_name exists.
            tb_name = tb_args.pop(0)
            tb_path = os.path.join(db_path, tb_name)
            if not os.path.isfile(tb_path):
                print(f'!Failed to query table {tb_name} because it does not exist.')
                return
            # Get table.
            header, rows = get_table(tb_path)
            # Check if all columns in col_list in table header
            if not is_cols_in_header(col_list, header):
                print(f'!Failed to query table {tb_name} because a specified column is not in the table.')
                return
                # Check if exactly 3 arguments for WHERE clause
            if len(tokens) < 3:
                print(f'!Failed to query table {tb_name} because of missing WHERE clause arguments.')
                return
            if len(tokens) > 3:
                print(f'Failed to query table {tb_name} because of too many arguments in WHERE clause.')
                return
            # Get WHERE clause arguments
            where_col = tokens.pop(0)
            logic = tokens.pop(0)
            value = tokens.pop(0)
            header_index = get_header_index(header, where_col)
            # Check if value is of correct type.
            _ , data_type = header[header_index]
            if data_type == int:
                if not is_int(value):
                    print(f'!Failed to query table {tb_name} because {value} is not an <int>.')
                    return
                value = int(value)
            elif data_type == float:
                if not is_float(value):
                    print(f'!Failed to query table {tb_name} because {value} is not a <float>.')
                    return
                value = float(value)
            else:
                if not is_char:
                    print(f'!Failed to query table {tb_name} because {value} is not a <string>.')
                    return
            # Select rows under the WHERE condition
            rows = get_rows_where_cond(rows, header_index, LOGIC[logic], value)
            # Check if wildcard was selected. If so, print table and return.
            if WILDCARD in col_list:
                print_table(header, rows)
                return
            # Get queried columns and print table at queried columns
            col_indices = get_cols_indices(header, col_list)
            header, rows = get_table_at_cols(header, rows, col_indices)
            print_table(header, rows)
            return
        else:
            # Check which join type
            if len(tb_args) == 5:
                # Implicit inner join: tb_name1 tb_alias1 , tb_name2 tb_alias2
                tb_name1 = tb_args.pop(0)
                tb_alias1 = tb_args.pop(0)
                if tb_args.pop(0) != ',':
                    print(f"!Failed to query table because of missing ',' after {tb_name1} {tb_alias1}.")
                    return
                tb_name2 = tb_args.pop(0)
                tb_alias2 = tb_args.pop(0)
                table_alias = {tb_alias1: tb_name1, tb_alias2: tb_name2}
                # Check if tables are valid
                tb_path1 = os.path.join(db_path, tb_name1)
                tb_path2 = os.path.join(db_path, tb_name2)
                if not os.path.isfile(tb_path1):
                    print(f'!Failed to query table {tb_name1} because it does not exist.')
                    return
                if not os.path.isfile(tb_path2):
                    print(f'!Failed to query table {tb_name2} because it does not exist.')
                    return
                # Get tables
                header1, rows1 = get_table(tb_path1)
                header2, rows2 = get_table(tb_path2)
                # Get condition cols
                col1 = tokens.pop(0)
                logic = tokens.pop(0)
                col2 = tokens.pop(0)
                alias1, col_name1 = col1.split('.')
                alias2, col_name2 = col2.split('.')
                # Check if column is in table
                if alias1 == alias2:
                    print('!Failed to query table because the same table alias was used twice.')
                    return
                for alias, col in [(alias1, col_name1), (alias2, col_name2)]:
                    if table_alias[alias] == tb_name1:
                        if not is_cols_in_header([col], header1):
                            print(f'!Failed to query table because {col} is not in {tb_name1}.')
                            return
                    elif table_alias[alias] == tb_name2:
                        if not is_cols_in_header([col], header2):
                            print(f'!Failed to query table because {col} is not in {tb_name2}.')
                    else:
                        print(f'!Failed to query table because alias {alias} does not match to a table.')
                        return
                # Get rows where condition is met
                index_c1 = get_cols_indices(header1, [col_name1]).pop()
                index_c2 = get_cols_indices(header2, [col_name2]).pop(0)
                new_header = header1 + header2
                new_rows = []
                for r1 in rows1:
                    for r2 in get_rows_where_cond(rows2, index_c2, LOGIC[logic], r1[index_c1]):
                        new_rows.append(r1 + r2)
                # Check if all columns in col_list in table header
                #### Need to implement
                ##if not is_cols_in_header(col_list, header):
                ##    print(f'!Failed to query table {tb_name} because a specified column is not in the table.')
                ##   return
                # Check if wildcard was selected. If so, print table and return.
                if WILDCARD in col_list:
                    print_table(new_header, new_rows)
                    return
                # Get queried columns and print table at queried columns
                #### Need to implement
                ##col_indices = get_cols_indices(header, col_list)
                ##header, rows = get_table_at_cols(header, rows, col_indices)
                ##print_table(header, rows)
                return

            else:
                print('!Failed to query table because of invalid table arguments.')
                return
            
            

        
        


# Test script
def main():
    tokens = '* FROM test'.split()
    select(tokens, 'Test')
    tokens = 'a2 , a3 , a1 , a4 , a1 FROM test'.split()
    select(tokens, 'Test')
    tokens = '* FROM test WHERE a5 < 2.0'.split()
    select(tokens, 'Test')

if __name__ == '__main__':
    main()