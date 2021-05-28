import math
import random
from collections import namedtuple
from typing import Iterable, Sequence, Tuple, Dict, List

Tile_pos = namedtuple('Tile_pos', ('row', 'column'))


class Board:
    __slots__ = '_rows_num', '_columns_num', '_tiles', '_blank_tile_pos'

    default_rows_num: int = 4
    default_columns_num: int = 4

    def __init__(self, rows_num: int = default_rows_num, columns_num: int = default_columns_num,
                 values: Sequence[int] = None, tiles: Dict[Tile_pos, int] = None):

        if any(dim < 2 for dim in (columns_num, rows_num)):
            raise ValueError('At least one dimension is less than 2')

        self._rows_num = rows_num
        self._columns_num = columns_num

        if tiles:
            self._tiles = tiles

        else:
            if values:
                self._validate_values(columns_num=columns_num, rows_num=rows_num, values=values)
                tiles_values = values

            else:
                tiles_values = list(range(rows_num * columns_num))
                random.shuffle(tiles_values)

            self._tiles = {Tile_pos(i // columns_num + 1,
                                    (i + 1) % columns_num if (i + 1) % columns_num != 0 else columns_num): val
                           for i, val in enumerate(tiles_values)}

        self._blank_tile_pos: Tile_pos = next(key for key, value in self._tiles.items() if value == 0)

    def __str__(self) -> str:
        board_str_sequence = (f'{val:3d}  ' if index.column != self._columns_num else f'{val:3d}\n\n'
                              for index, val in self._tiles.items())

        return ''.join(board_str_sequence).replace(' 0', '  ')

    @property
    def tiles(self):
        return self._tiles.copy()  # restricting any outside modifications on original object

    @property
    def rows_num(self) -> int:
        return self._rows_num

    @property
    def columns_num(self) -> int:
        return self._columns_num

    def play(self, move_sequence: Iterable[str] = None, print_after_each_move: bool = True):
        if move_sequence:
            move_sequence = iter(move_sequence)

        while True:
            if print_after_each_move:
                print(self)

            if self.is_solved():
                print('You won!')
                return

            if move_sequence:
                try:
                    key = next(move_sequence).lower()
                except StopIteration:
                    return
            else:
                key = input().lower()
                if key == 'b':
                    return

            if key not in 'rlud':
                continue

            self.move(key)

    def move(self, key: str):
        if key not in 'rlud':
            raise AttributeError("Move has to be one of 'a', 'w', 's' or 'd'")
        elif key not in self.get_available_moves():
            # raise AttributeError("Illegal move made")
            return
        blank_title_pos = self._blank_tile_pos

        if key == 'r':
            self._swap_tiles(blank_title_pos, (blank_title_pos.row, blank_title_pos.column + 1))
        elif key == 'l':
            self._swap_tiles(blank_title_pos, (blank_title_pos.row, blank_title_pos.column - 1))
        elif key == 'u':
            self._swap_tiles(blank_title_pos, (blank_title_pos.row - 1, blank_title_pos.column))
        elif key == 'd':
            self._swap_tiles(blank_title_pos, (blank_title_pos.row + 1, blank_title_pos.column))

    def get_available_moves(self) -> List[str]:
        available_moves = []
        if self._blank_tile_pos.column != self._columns_num:
            available_moves.append('r')
        if self._blank_tile_pos.column != 1:
            available_moves.append('l')
        if self._blank_tile_pos.row != 1:
            available_moves.append('u')
        if self._blank_tile_pos.row != self._rows_num:
            available_moves.append('d')
        return available_moves

    def is_solved(self) -> bool:
        return all(self._tiles[key] == (key if key != len(self._tiles) else 0) for key in self._tiles)

    def is_solvable(self) -> bool:
        if self._columns_num != self._rows_num:
            raise NotImplementedError('MxN puzzle validation is yet to be implemented')

        else:
            inversion_count = self.get_inversions_count(self._tiles.values())

            if self._columns_num % 2:
                return inversion_count % 2 == 0
            else:
                return (self._rows_num + 1 - self._blank_tile_pos.row) % 2 != inversion_count % 2

    def get_tile_distance_from_solved(self, tile_position: Tuple[int, int]) -> int:
        if self._tiles.get(tile_position) is None:
            raise AttributeError('Given position is not present in board')

        tile_value = self._tiles.get(tile_position)

        if tile_value == 0:
            solved_position = (self.rows_num, self._columns_num)
        else:
            solved_position = ((tile_value - 1) // self._columns_num + 1,
                               tile_value % self._columns_num if tile_value % self._columns_num != 0
                               else self._columns_num)

        return sum(math.fabs(a - b) for a, b in zip(tile_position, solved_position))

    @staticmethod
    def get_inversions_count(values: Iterable[int]) -> int:
        if not isinstance(values, list):
            values = list(values)

        if 0 in values:
            values.remove(0)

        # looping through all tiles and accumulating sum of inversions for each
        return sum(
            sum(1 for val in values[i + 1:] if val < x)
            for i, x in enumerate(values))

    def _swap_tiles(self, blank_title_pos: Tuple[int, int], tile_pos: Tuple[int, int]):
        blank_title_pos, tile_pos = Tile_pos(*blank_title_pos), Tile_pos(*tile_pos)
        self._blank_tile_pos = tile_pos
        self._tiles[blank_title_pos], self._tiles[tile_pos] = self._tiles[tile_pos], self._tiles[blank_title_pos]

    @staticmethod
    def _validate_values(columns_num: int, rows_num: int, values: Sequence[int]):
        if len(values) != rows_num * columns_num:
            raise AttributeError(f'Provided values sequence length: {len(values)} '
                                 f'does not match board dimensions {rows_num}x{columns_num}')

        if len(values) != len(set(values)):
            raise ValueError('Provided values sequence contains duplicate values')

        if any(val < 0 or val > rows_num * columns_num - 1 for val in values):
            raise ValueError(f'At least one provided value does not fit in range [0, {rows_num * columns_num - 1}]')

    def __hash__(self) -> int:
        return hash(frozenset(self._tiles.items()))

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self._tiles.items() == other._tiles.items()
