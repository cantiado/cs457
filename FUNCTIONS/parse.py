# Author: Carl Antiado
# Last Updated: 3/11/2022
# Created 3/11/2022

def parse(cmd_line: str) -> list[str]:
    tokens = []
    next_token = ''
    IGNORE = {' ','\t','\n','\r'}
    SPECIAL = {'(',')',',',';'}
    # parse command line by character
    for ch in cmd_line:
        if ch in IGNORE:
            if next_token != '':
                tokens.append(next_token)
                next_token = ''
        elif ch in SPECIAL:
            if next_token != '':
                tokens.append(next_token)
                next_token = ''
            tokens.append(ch)
            # stop parsing if encounter terminating semicolon
            if ch == ';':
                break
        else:
            next_token += ch
    if next_token != '': tokens.append(next_token)
    return tokens

def main():
    x = '''            CREATE TABLE tbl_1                         
    (a1 int, a2 varchar(20))                ; junk junk junk'''
    y = parse(x)
    print(y)

if __name__ == '__main__':
    main()