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

def __isfloat(num: str) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False
    
print(__isfloat('14.99'))