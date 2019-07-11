import time
import collections
import numpy as np
from random import random, randint

from board import Board, BOARD_SIZE, SHIP_SIZES, Point, NO_SHOT
# from game import Player


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


def random_move_parity(opponent_board_view: Board, player) -> Point:
    """
    Randomly choose an empty square to shoot at when in 'hunt' mode,
    if hit, change to 'target' mode and focus first on neighbor cells.
    """
    # decide moving mode
    if len(player.queue) == 0:
        mode = 'hunt'
        player.hit_direction = [None, None]
        player.prev_hit = None
    else:
        mode = 'target'

    # end infinite loop for test purpose
    # TODO: fix this infinite loop bug in the recursive call
    timeout = time.time() + .1  # 1 seconds from now

    # make shot
    if mode == 'hunt':
        empty_xs, empty_ys = np.where(opponent_board_view.shots == NO_SHOT)

        # get only cells whose r + c is even
        sum_idx = empty_xs + empty_ys
        target_idx,  = np.where(sum_idx % 2 == 0)

        # random choose one element from the even r/c indices
        choice = np.random.choice(target_idx, size=1)[0]
        shot = Point(x=empty_xs[choice], y=empty_ys[choice])

    elif mode == 'target':
        shot = player.queue.popleft()
        while is_shot_invalid(player, opponent_board_view, shot):
            if time.time() > timeout:
                break
            if len(player.queue) > 0:
                shot = player.queue.popleft()
            else:
                shot = random_move_parity(opponent_board_view, player)

    # add neighbors to queue if the shot is a hit
    if opponent_board_view.has_ship[shot.x, shot.y]:
        # update hit direction
        player.prev_hit, player.hit_direction = \
            update_hit_direction(player.prev_hit, shot, player.hit_direction)

        up = Point(x=shot.x, y=max(shot.y - 1, 0))
        down = Point(x=shot.x, y=min(shot.y + 1, 9))
        left = Point(x=max(shot.x - 1, 0), y=shot.y)
        right = Point(x=min(shot.x + 1, 9), y=shot.y)
        neighbors = [up, down, left, right]
        player.queue.extend(neighbors)

    return shot


def update_hit_direction(prev_hit: Point, cur_hit: Point, hit_direction: list):
    """Update previous hit and hit direction inplace"""
    if not prev_hit:
        # first hit, then all four directions are available
        prev_hit = cur_hit
        hit_direction[0] = cur_hit.x
        hit_direction[1] = cur_hit.y
    else:
        x_direction = cur_hit.x if cur_hit.x == prev_hit.x else None
        y_direction = cur_hit.y if cur_hit.y == prev_hit.y else None
        hit_direction[0] = x_direction
        hit_direction[1] = y_direction

    return prev_hit, hit_direction


def is_shot_invalid(player, opponent_board_view, shot):
    return opponent_board_view.shots[shot.x, shot.y] != NO_SHOT \
           or not (shot.x == player.hit_direction[0] or shot.y == player.hit_direction[1])
