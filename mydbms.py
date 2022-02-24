# Author: Carl Antiado
# Last updated: 2/8/2022
# Created: 2/8/2022

from FUNCTIONS.create import create
from FUNCTIONS.drop import drop
from FUNCTIONS.use import use
from FUNCTIONS.select import select
from FUNCTIONS.alter import alter

# command_line := <command> <args> ;
# command  := CREATE
#           | DROP
#           | USE 
#           | SELECT 
#           | ALTER

selected_db = 'NULL'

command_line = input('>> ').strip()

while command_line.upper() != '.EXIT':
    # ignore comments
    if command_line.startswith('--'):
        print('comment')
    # invalid command if no terminating semicolon
    if not command_line.endswith(';'):
        print('!Missing terminating semicolon \';\'.')
    
    else:
        # removes terminating semicolon
        command_line = command_line.removesuffix(';').strip()
        command, args = command_line.split(' ', 1)
        if command.upper() == 'CREATE':
            create(args, selected_db)
        elif command.upper() == 'DROP':
            drop(args, selected_db)
        elif command.upper() == 'USE':
            selected_db = use(args)
        elif command.upper() == 'SELECT':
            select(args, selected_db)
        elif command.upper() == 'ALTER':
            alter(args, selected_db)
        else:
            print('!Invalid command.')
            
    command_line = input('>> ').strip()


print('All done.')