import numpy as np
from dataclasses import dataclass


BOARD_SIZE = 10
# SHIP_SIZES = [
#     5,  # carrier
#     4,  # battleship
#     3,  # cruiser
#     3,  # submarine
#     2,  # destroyer
# ]

SHIP_SIZES = {
    'carrier': 5,
    'battleship': 4,
    'cruiser': 3,
    'submarine': 3,
    'destroyer': 2
}

# encoding for board.shots
NO_SHOT = 0
MISS = 1
HIT = 2


@dataclass
class Point:
    x: int
    y: int


# class Board:
#     def __init__(self):
#         # an array of NO_SHOT, MISS, or HIT
#         # this is the opponent's view of the board
#         self.shots = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
#
#         # a boolean array, only visible to the player:
#         #   0 where there is no ship
#         #   1 where there is a ship
#         self.has_ship = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=bool)
#
#     def make_move(self, shot: Point) -> None:
#         if (shot.x < 0 or shot.x >= BOARD_SIZE
#                 or shot.y < 0 or shot.y >= BOARD_SIZE
#                 or self.shots[shot.x, shot.y] != NO_SHOT):
#             raise ValueError(f'{shot} is an illegal move.')
#
#         if self.has_ship[shot.x, shot.y]:
#             self.shots[shot.x, shot.y] = HIT
#         else:
#             self.shots[shot.x, shot.y] = MISS
#
#     def all_sunk(self) -> bool:
#         hit_count = np.sum(self.shots == HIT)
#         ship_count = np.sum(list(SHIP_SIZES.values()))
#         return hit_count == ship_count


class Board:
    """This version of board will tell the player the type of a sunk ship."""

    def __init__(self):
        # an array of NO_SHOT, MISS, or HIT
        # this is the opponent's view of the board
        self.shots = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

        # a boolean array, only visible to the player:
        #   0 where there is no ship
        #   1 where there is a ship
        self.has_ship = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=bool)

        # an empty to store the head and tail position of each ship
        self.ship_loc = []

        # empty text field to show the human player which type of ship is sunk
        self.text_field = ''

    def make_move(self, shot: Point) -> None:
        if (shot.x < 0 or shot.x >= BOARD_SIZE
                or shot.y < 0 or shot.y >= BOARD_SIZE
                or self.shots[shot.x, shot.y] != NO_SHOT):
            raise ValueError(f'{shot} is an illegal move.')

        # print(self.shots, self.has_ship)
        if self.has_ship[shot.x, shot.y]:
            self.shots[shot.x, shot.y] = HIT

            # keep track of ship status
            for ship, loc in self.ship_loc:
                if (shot.x, shot.y) in loc:
                    loc.remove((shot.x, shot.y))
        else:
            self.shots[shot.x, shot.y] = MISS
            # print(self.shots, shot)

    def all_sunk(self) -> bool:
        hit_count = np.sum(self.shots == HIT)
        ship_count = np.sum(list(SHIP_SIZES.values()))
        return hit_count == ship_count
