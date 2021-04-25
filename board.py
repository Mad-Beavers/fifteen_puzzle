import random
import re
from typing import Union, Iterator


class Board:
    default_size: int = 4

    def __init__(self, board_size: int = default_size):
        self._board_size = board_size
        tiles_values = list(range(board_size ** 2))
        random.shuffle(tiles_values)
        self._tiles = {index: value for index, value in zip(range(1, board_size ** 2 + 1), tiles_values)}
        self._blank_title_pos = next(key for key, value in self._tiles.items() if value == 0)

    def __str__(self) -> str:
        board_str_sequence = (f'{val:3d}\n\n' if not index % self._board_size else f'{val:3d}  '
                              for index, val in self._tiles.items())
        return re.sub(r'(?<!\d)0', ' ', ''.join(board_str_sequence))

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

            if key == 'a' and (blank_title_key := self._blank_title_pos) % self._board_size:
                self.swap_titles(blank_title_key, blank_title_key + 1)

            elif key == 'd' and (blank_title_key := self._blank_title_pos) % self._board_size != 1:
                self.swap_titles(blank_title_key, blank_title_key - 1)

            elif key == 's' and (blank_title_key := self._blank_title_pos) / self._board_size > 1:
                self.swap_titles(blank_title_key, blank_title_key - self._board_size)

            elif key == 'w' and \
                    (blank_title_key := self._blank_title_pos) / self._board_size <= self._board_size - 1:
                self.swap_titles(blank_title_key, blank_title_key + self._board_size)
