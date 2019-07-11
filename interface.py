import os
import numpy as np

from board import Board, BOARD_SIZE, Point, HIT, MISS, NO_SHOT


if BOARD_SIZE > 26:
    raise AssertionError("This interface uses letters for columns, "
                         "so it can't handle boards that large.")

CHARS = 'abcdefghijklmnopqrstuvwxyz'


def display_boards(player_board: Board, opponent_board_view: np.ndarray):
    # clear the terminal, if running on a unix-like system
    try:
        os.system('clear')
    except:
        pass

    board_display_width = 3 * BOARD_SIZE
    horizontal_bar = '---+' + '-' * board_display_width + '+' + \
                     '-' * board_display_width + '+'

    print('')
    print('   | YOUR BOARD'
          + ' ' * (board_display_width - len(' YOUR BOARD'))
          + '| ENEMY BOARD')
    print(horizontal_bar)

    # column labels
    print('   |', end='')
    for c in range(BOARD_SIZE):
        print(f' {CHARS[c]} ', end='')
    print('|', end='')
    for c in range(BOARD_SIZE):
        print(f' {CHARS[c]} ', end='')
    print('|')
    print(horizontal_bar)

    for y in range(BOARD_SIZE):
        # row label
        print(f' {y} |', end='')

        # our board
        for x in range(BOARD_SIZE):
            if player_board.shots[x, y] == HIT:
                print('💥 ', end='')
            elif player_board.has_ship[x, y]:
                print('🚢 ', end='')
            elif player_board.shots[x, y] == MISS:
                print('💦 ', end='')
            else:
                print(' . ', end='')

        # center divider
        print('|', end='')

        # our view of their board
        for x in range(BOARD_SIZE):
            if opponent_board_view[x, y] == HIT:
                print('💥 ', end='')
            elif opponent_board_view[x, y] == MISS:
                print('💦 ', end='')
            else:
                print(' . ', end='')

        print('|')

    print(horizontal_bar)
    print('')
    print(player_board.text_field)


def input_move(opponent_board_view: np.ndarray) -> Point:
    while True:
        raw_input = input('Move (e.g "f0") --> ')
        try:
            col = raw_input[0]
            row = raw_input[-1]
            x = CHARS.index(col.lower())
            y = int(row)
            if opponent_board_view[x, y] != NO_SHOT:
                print(f'Already shot at ({row},{col})')
            else:
                return Point(x, y)
        except:
            pass
