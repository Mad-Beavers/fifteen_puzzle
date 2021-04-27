import random
from typing import Union, Iterator, Collection


class Board:
    default_rows_num: int = 4
    default_columns_num: int = 4

    def __init__(self, rows_num: int = default_rows_num, columns_num: int = default_columns_num,
                 values: Collection[int] = None):
        if any(dim < 2 for dim in (columns_num, rows_num)):
            raise ValueError('At least one dimension is less than 2')

        self._rows_num = rows_num
        self._columns_num = columns_num

        if values:
            self._validate_values(columns_num=columns_num, rows_num=rows_num, values=values)
            tiles_values = values

        else:
            tiles_values = list(range(rows_num * columns_num))
            random.shuffle(tiles_values)

        self._tiles = {index: value for index, value in zip(range(1, rows_num * columns_num + 1), tiles_values)}
        self._blank_title_pos = next(key for key, value in self._tiles.items() if value == 0)
        self.moves_count = 0

    def __str__(self) -> str:
        board_str_sequence = (f'{val:3d}\n\n' if not index % self._columns_num else f'{val:3d}  '
                              for index, val in self._tiles.items())
        return ''.join(board_str_sequence).replace(' 0', '  ')

    def _swap_titles(self, blank_title_pos: int, title_pos: int):
        self._blank_title_pos = title_pos
        self._tiles[blank_title_pos], self._tiles[title_pos] = self._tiles[title_pos], self._tiles[blank_title_pos]
        self.moves_count += 1

    def is_solved(self) -> bool:
        return all(self._tiles[key] == (key if key != len(self._tiles) else 0) for key in self._tiles)

    def play(self, move_sequence: Union[str, Iterator[str]] = None, print_after_each_move: bool = True):
        if move_sequence and type(move_sequence) == str:
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

            if key not in 'awsd':
                continue

            if key == 'a' and (blank_title_key := self._blank_title_pos) % self._columns_num:
                self._swap_titles(blank_title_key, blank_title_key + 1)

            elif key == 'd' and (blank_title_key := self._blank_title_pos) % self._columns_num != 1:
                self._swap_titles(blank_title_key, blank_title_key - 1)

            elif key == 's' and (blank_title_key := self._blank_title_pos) / self._columns_num > 1:
                self._swap_titles(blank_title_key, blank_title_key - self._columns_num)

            elif key == 'w' and (blank_title_key := self._blank_title_pos) / self._columns_num <= self._rows_num - 1:
                self._swap_titles(blank_title_key, blank_title_key + self._columns_num)

    @staticmethod
    def _validate_values(columns_num: int, rows_num: int, values: Collection[int]):
        if len(values) != rows_num * columns_num:
            raise AttributeError(f'Provided values sequence length: {len(values)} '
                                 f'does not match board dimensions {rows_num}x{columns_num}')

        if len(values) != len(set(values)):
            raise ValueError('Provided values sequence contains duplicate values')

        if any(val < 0 or val > rows_num * columns_num - 1 for val in values):
            raise ValueError(f'At least one provided value does not fit in range [0, {rows_num * columns_num - 1}]')

    def is_solvable(self) -> bool:
        if self._columns_num != self._rows_num:
            raise NotImplementedError('MxN puzzle validation is yet to be implemented')

        else:
            if self._columns_num % 2:
                return self.get_inversions_count(list(self._tiles.values())) % 2 == 0
            else:
                inversions_count = self.get_inversions_count(list(self._tiles.values()))
                return (self._blank_title_pos - 1) // self._columns_num % 2 != inversions_count % 2

    @staticmethod
    def get_inversions_count(values: list[int]) -> int:
        values.remove(0)

        # looping through all tiles and accumulating sum of inversions for each
        return sum(
            sum(1 for val in values[i + 1:] if val < x)
            for i, x in enumerate(values))
