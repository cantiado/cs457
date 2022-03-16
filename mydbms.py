# Author: Carl Antiado
# Last updated: 3/11/2022
# Created: 2/8/2022

from FUNCTIONS.parse import parse
from FUNCTIONS.create import create
from FUNCTIONS.drop import drop
from FUNCTIONS.use import use
from FUNCTIONS.select import select
from FUNCTIONS.alter import alter

'''
--- Grammar ---
command_line := <command> <args> ;
command    := CREATE
            | DROP
            | USE 
            | SELECT 
            | ALTER
'''

# initialize selected database to NULL
selected_db = 'NULL'

# get first inputs
command_line = input('>> ')

while command_line.upper() != '.EXIT':
    # parse command line for tokens
    tokens = parse(command_line)

    # ignore comments and no tokens
    if tokens[0].startswith('--') or len(tokens) == 0:
        pass
    # invalid command if no terminating semicolon
    elif tokens[-1] == ';':
        print("!Missing terminating semicolon ';'.")
    # attempt to perform a command
    else:
        # removes terminating semicolon
        tokens.pop()
        # first token determines the command,
        # remove first token and pass remaining tokens into command function
        command = tokens.pop(0)
        if command.upper() == 'CREATE':
            create(tokens, selected_db)
        elif command.upper() == 'DROP':
            drop(tokens, selected_db)
        elif command.upper() == 'USE':
            selected_db = use(tokens)
        elif command.upper() == 'SELECT':
            select(tokens, selected_db)
        elif command.upper() == 'ALTER':
            alter(tokens, selected_db)
        else:
            print('!Invalid command.')
    # command was attempted
    # get next input and loop
    command_line = input('>> ').strip()

# terminate program
print('All done.')