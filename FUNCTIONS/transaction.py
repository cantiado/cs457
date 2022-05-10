# Author: Carl Antiado
# Last Updated: 5/10/2022
# Created 5/10/2022

import os

from . import update, parse, utility
from .update import update
from .parse import parse
from .utility import get_table, make_table

def transaction(db: str) -> None:
    print('Transaction starts.')

    cwd = os.getcwd()
    db_path = os.path.join(cwd, db)

    command_line = input('>> ')
    tokens = parse(command_line)

    locks = set()

    while True:
        # remove semicolon
        tokens.pop()
        # get command
        command = tokens.pop(0)
        if command.upper() == 'UPDATE':
            tb_name = tokens[0]
            tb_path = os.path.join(db_path, tb_name)
            if not os.path.isfile(tb_path):
                print(f'!Failed to update table {tb_name} because it does not exist.')
            else:
                lock_name = f'{tb_name}-LOCK'
                lock_path = os.path.join(db_path, lock_name)
                if lock_name not in locks and os.path.isfile(lock_path):
                    print(f'Error: Table {tb_name} is locked!')
                else:
                    header, rows = get_table(tb_path)
                    make_table(lock_path, header, rows)
                    locks.add(lock_name)
                    tokens[0] = lock_name
                    update(tokens, db)
        elif command.upper() == 'COMMIT':
            if len(locks) == 0:
                print('Transaction abort.')
            else:
                for lock in locks:
                    lock_path = os.path.join(db_path, lock)
                    tb_name = lock.removesuffix('-LOCK')
                    tb_path = os.path.join(db_path, tb_name)
                    os.remove(tb_path)
                    os.rename(lock_path, tb_path)
                print('Transaction committed.')
            return
        else:
            print('!Invalid command')
        
        
        command_line = input('>> ')
        tokens = parse(command_line)