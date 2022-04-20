# Author: Carl Antiado
# Last updated: 4/16/2022
# Created: 4/16/2022

from typing import Any, Callable, Union, NewType
import os

# custom data types
Char = NewType('char', str)
Varchar = NewType('varchar', str)
Maxlen = int
Datatype = Union[int, float, Char, Varchar, tuple[Char, Maxlen], tuple[Varchar, Maxlen]]
Header = list[tuple[str, Datatype]]
Rows = list[list[Datatype]]
# data types
CRLF = '\n'
QUOTE = "'"
WILDCARD = '*'
DATATYPES = {'int': int, 'float': float, 'char': Char, 'varchar': Varchar}
DEFAULT_VAL = {'int': -9999, 'float': -9999.0, 'char': QUOTE*2, 'varchar': QUOTE*2}

def get_table(file_path: str) -> tuple[Header, Rows]:
    with open(file_path, 'r') as f:
        table = f.readlines()
    header = []
    for col in table[0].split(' | '):
        col_name, data_type = col.split()
        if 'char' in data_type:
            maxlen = data_type[data_type.index('(') + 1 : data_type.index(')')]
            data_type = data_type[:data_type.index('(')]
            data_type = (DATATYPES[data_type], maxlen)
        else:
            data_type = DATATYPES[data_type]
        header.append((col_name, data_type))
    rows = []
    for row in table[1:]:
        formatted_row = []
        for entry in row.split(' | '):
            entry = entry.strip()
            if is_int(entry):
                formatted_row.append(int(entry))
            elif is_float(entry):
                formatted_row.append(float(entry))
            else:
                formatted_row.append(entry)
        rows.append(formatted_row)
    return header, rows

def make_table(file_path: str, header: Header, rows: Rows = []) -> None:
    table = format_header(header) + CRLF + format_rows(rows)
    with open(file_path, 'w') as f:
        f.write(table)
    return

def print_table(header: Header, rows: Rows) -> None:
    print(format_header(header) + CRLF + format_rows(rows))

def get_cols_indices(header: Header, cols: list[str]) -> list[int]:
    col_names = [h[0] for h in header]
    return [col_names.index(c) for c in cols]

def get_table_at_cols(header: Header, rows: Rows, col_indices = list[int]) -> tuple[Header, Rows]:
    new_header = [header[i] for i in col_indices]
    new_rows = []
    for row in rows:
        new_row = [row[i] for i in col_indices]
        new_rows.append(new_row)
    return new_header, new_rows

def get_header_index(header: Header, col_name: str) -> int:
    col_names = [h[0] for h in header]
    return col_names.index(col_name)

def get_rows_where_cond(rows: Rows, header_index: int, logic_operator: Callable[[Any, Any], bool], value: Any) -> Rows:
    return [row for row in rows if logic_operator(row[header_index], value)]

def format_header(header: Header) -> str:
    cols = []
    for col_name, data_type in header:
        if data_type == int:
            cols.append(f'{col_name} int')
        elif data_type == float:
            cols.append(f'{col_name} float')
        else:
            dt, maxlen = data_type
            if dt == Char:
                cols.append(f'{col_name} char({maxlen})')
            else:
                cols.append(f'{col_name} varchar({maxlen})')
    return ' | '.join(cols)

def format_rows(rows: Rows) -> str:
    f_rows = []
    for row in rows:
        row = [str(r) for r in row]
        f_rows.append(' | '.join(row))
    return CRLF.join(f_rows)

def is_cols_in_header(cols: list[str], header: Header) -> bool:
    col_names = [h[0] for h in header]
    for col in cols:
        if col == '*':
            pass
        elif col not in col_names:
            return False
    return True

def is_int(s: str) -> bool:
    return s.isdigit()

def is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_char(s: str, str_len_lim: int) -> bool:
    if s[0] == s[-1] == QUOTE:
        if len(s) - 2 <= str_len_lim:
            return True
    return False

# Logical operators

def is_equal(a: Any, b: Any) -> bool:
    return a == b

def is_not_equal(a: Any, b: Any) -> bool:
    return a != b

def is_less_than(a: Any, b: Any) -> bool:
    return a < b

def is_greater_than(a: Any, b: Any) -> bool:
    return a > b

def is_less_than_or_equal(a: Any, b: Any) -> bool:
    return a <= b

def is_greater_than_or_equal(a: Any, b: Any) -> bool:
    return a >= b

LOGIC = {'=': is_equal, '!=': is_not_equal, '<': is_less_than, '>': is_greater_than,
    '<=': is_less_than_or_equal, '>=': is_greater_than_or_equal}


def main():
    path = os.path.join(os.getcwd(),'Test','test')
    header = [('a1', int), ('a2', float), ('a3', (Char, 20)), ('a4', (Varchar, 2000))]
    rows = [[1, 3.10, "'hello'", "'world'"], [2, -2.7, "'good'", "'bye'"]]
    print(format_header(header))
    print(format_rows(rows))
    make_table(path, header, [])

if __name__ == '__main__':
    main()