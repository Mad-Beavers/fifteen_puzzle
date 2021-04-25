import random
from typing import Union, Iterator


class Board:
    default_rows_num: int = 4
    default_columns_num: int = 4

    def __init__(self, rows_num: int = default_rows_num, columns_num: int = default_columns_num):
        self._rows_num = rows_num
        self._columns_num = columns_num

        tiles_values = list(range(rows_num * columns_num))
        random.shuffle(tiles_values)

        self._tiles = {index: value for index, value in zip(range(1, rows_num * columns_num + 1), tiles_values)}
        self._blank_title_pos = next(key for key, value in self._tiles.items() if value == 0)

    def __str__(self) -> str:
        board_str_sequence = (f'{val:3d}\n\n' if not index % self._columns_num else f'{val:3d}  '
                              for index, val in self._tiles.items())
        return ''.join(board_str_sequence).replace(' 0', '  ')

    def swap_titles(self, blank_title_pos: int, title_pos: int):
        self._blank_title_pos = title_pos
        self._tiles[blank_title_pos], self._tiles[title_pos] = self._tiles[title_pos], self._tiles[blank_title_pos]

    def play(self, move_sequence: Union[str, Iterator[str]] = None):
        if move_sequence and type(move_sequence) == str:
            move_sequence = iter(move_sequence)

        while True:
            print(self)
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
                self.swap_titles(blank_title_key, blank_title_key + 1)

            elif key == 'd' and (blank_title_key := self._blank_title_pos) % self._columns_num != 1:
                self.swap_titles(blank_title_key, blank_title_key - 1)

            elif key == 's' and (blank_title_key := self._blank_title_pos) / self._columns_num > 1:
                self.swap_titles(blank_title_key, blank_title_key - self._columns_num)

            elif key == 'w' and (blank_title_key := self._blank_title_pos) / self._columns_num <= self._rows_num - 1:
                self.swap_titles(blank_title_key, blank_title_key + self._columns_num)
