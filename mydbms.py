# Author: Carl Antiado
# Last updated: 3/19/2022
# Created: 2/8/2022

from FUNCTIONS.parse import parse
from FUNCTIONS.create import create
from FUNCTIONS.drop import drop
from FUNCTIONS.use import use
from FUNCTIONS.select import select
from FUNCTIONS.alter import alter
from FUNCTIONS.insert import insert
from FUNCTIONS.update import update
from FUNCTIONS.delete import delete
'''
--- Grammar ---
command_line := <command> <args> ; | .EXIT
command := CREATE
        | DROP
        | USE 
        | SELECT 
        | ALTER
        | INSERT
        | DELETE
'''

# initialize selected database to NULL
selected_db = 'NULL'

# get first input and parse it
command_line = input('>> ')
tokens = parse(command_line)
while True:
    # parse command line for tokens until terminating semicolon reached
    #   or only input is .EXIT
    # reset tokens if first token is a comment (begins with '--')
    while ';' not in tokens and not (len(tokens) == 1 and tokens[0].upper() == '.EXIT'):
        if len(tokens) != 0 and tokens[0].startswith('--'):
            tokens = []
        cmd_line = input()
        tokens.extend(parse(cmd_line))
    # terminate program if only token is .EXIT
    if len(tokens) == 1 and tokens[0].upper() == '.EXIT':
        break
    # attempt to perform a command
    else:
        # removes terminating semicolon
        tokens.pop()
        # if tokens is now empty, invalid command
        if len(tokens) == 0:
            print('!Invalid command.')
        else:
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
            elif command.upper() == 'INSERT':
                insert(tokens, selected_db)
            elif command.upper() == 'UPDATE':
                update(tokens, selected_db)
            elif command.upper() == 'DELETE':
                delete(tokens, selected_db)
            else:
                print('!Invalid command.')
    # command was attempted
    # get next input and loop
    command_line = input('>> ')
    tokens = parse(command_line)

# terminate program
print('All done.')