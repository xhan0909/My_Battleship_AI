import collections
import numpy as np
from random import random, randint

from board import Board, BOARD_SIZE, SHIP_SIZES, Point, NO_SHOT


def _place_ship(size: int, has_ship: np.ndarray, ship_type=None):
    """Randomly place a single ship using rejection sampling."""

    # loop until we find a valid placement
    while True:
        # pick a top left coordinate
        x = randint(0, BOARD_SIZE - 1)
        y = randint(0, BOARD_SIZE - 1)

        # pick a direction
        horizontal = random() > 0.5

        # if it fits, place it
        if (horizontal
                and x + size < BOARD_SIZE
                and not np.any(has_ship[x:x+size, y])):
            has_ship[x:x+size, y] = True

            # if available, keep track of ship location for each type
            if ship_type:
                return (ship_type, [(xi, y) for xi in range(x, x+size)])

            return

        if (not horizontal
                and y + size < BOARD_SIZE
                and not np.any(has_ship[x, y:y+size])):
            has_ship[x, y:y+size] = True

            # if available, keep track of ship location for each type
            if ship_type:
                return (ship_type, [(x, yi) for yi in range(y, y+size)])

            return


def random_setup() -> Board:
    """Randomly place all ships onto a new board."""
    board = Board()

    for size in SHIP_SIZES.values():
        _place_ship(size, board.has_ship, type)
    assert np.sum(board.has_ship) == np.sum(list(SHIP_SIZES.values()))
    return board


def random_setup_easy() -> Board:
    """Randomly place all ships onto a new easy board."""
    board = Board()

    for type, size in SHIP_SIZES.items():
        cur_ship_loc = _place_ship(size, board.has_ship, type)
        board.ship_loc.append(cur_ship_loc)
    assert np.sum(board.has_ship) == np.sum(list(SHIP_SIZES.values()))
    return board


def random_move(opponent_board_view: np.ndarray) -> Point:
    """
    Randomly choose an empty square to shoot at.
    opponent_board_view is a grid of ShotResults.
    """
    empty_xs, empty_ys = np.where(opponent_board_view == NO_SHOT)
    choice = randint(0, len(empty_xs) - 1)

    return Point(x=empty_xs[choice], y=empty_ys[choice])


def random_move_target(queue: collections.deque, opponent_board_view: Board) -> Point:
    """
    Randomly choose an empty square to shoot at when in 'hunt' mode,
    if hit, change to 'target' mode and focus first on neighbor cells.
    """
    # decide moving mode
    if len(queue) == 0:
        mode = 'hunt'
    else:
        mode = 'target'

    # make shot
    if mode == 'hunt':
        empty_xs, empty_ys = np.where(opponent_board_view.shots == NO_SHOT)
        choice = randint(0, len(empty_xs)-1)
        shot = Point(x=empty_xs[choice], y=empty_ys[choice])
    elif mode == 'target':
        shot = queue.popleft()
        while opponent_board_view.shots[shot.x, shot.y] != NO_SHOT:
            if len(queue) > 0:
                shot = queue.popleft()
            else:
                shot = random_move_target(queue, opponent_board_view)

    # add neighbors to queue if the shot is successful
    if opponent_board_view.has_ship[shot.x, shot.y]:
        up = Point(x=shot.x, y=max(shot.y-1, 0))
        down = Point(x=shot.x, y=min(shot.y+1, 9))
        left = Point(x=max(shot.x-1, 0), y=shot.y)
        right = Point(x=min(shot.x+1, 9), y=shot.y)
        neighbors = [up, down, left, right]
        queue.extend(neighbors)

    return shot


def random_move_parity(queue: collections.deque, opponent_board_view: Board) -> Point:
    """
    Randomly choose an empty square to shoot at when in 'hunt' mode,
    if hit, change to 'target' mode and focus first on neighbor cells.
    """
    # decide moving mode
    if len(queue) == 0:
        mode = 'hunt'
    else:
        mode = 'target'

    # make shot
    if mode == 'hunt':
        empty_xs, empty_ys = np.where(opponent_board_view.shots == NO_SHOT)

        # get only even row and even column elements
        even_x_idx, = np.where(empty_xs % 2 == 0)
        even_y_idx, = np.where(empty_ys % 2 == 0)
        indices = np.intersect1d(even_x_idx, even_y_idx)

        # random choose one element from the even r/c indices
        if len(indices) > 0:
            choice = np.random.choice(indices, size=1)
        else:
            choice = randint(0, len(empty_xs) - 1)
        shot = Point(x=empty_xs[choice], y=empty_ys[choice])

    elif mode == 'target':
        shot = queue.popleft()
        while opponent_board_view.shots[shot.x, shot.y] != NO_SHOT:
            if len(queue) > 0:
                shot = queue.popleft()
            else:
                shot = random_move_parity(queue, opponent_board_view)

    # add neighbors to queue if the shot is successful
    if opponent_board_view.has_ship[shot.x, shot.y]:
        up = Point(x=shot.x, y=max(shot.y - 1, 0))
        down = Point(x=shot.x, y=min(shot.y + 1, 9))
        left = Point(x=max(shot.x - 1, 0), y=shot.y)
        right = Point(x=min(shot.x + 1, 9), y=shot.y)
        neighbors = [up, down, left, right]
        queue.extend(neighbors)

    return shot
