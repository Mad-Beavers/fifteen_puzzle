import random
import re


class Board:
    default_size: int = 4

    def __init__(self, board_size: int = default_size):
        self.board_size = board_size
        tiles_values = list(range(board_size ** 2))
        random.shuffle(tiles_values)
        self.tiles = {index: value for index, value in zip(range(1, board_size ** 2 + 1), tiles_values)}

    def __str__(self) -> str:
        board_str_sequence = (f'{val:3d}\n\n' if not index % self.board_size else f'{val:3d}  '
                              for index, val in self.tiles.items())
        return re.sub(r'(?<!\d)0', ' ', ''.join(board_str_sequence))

    def play(self):
        while True:
            print(self)
            if (key := input().lower()) not in 'rlud':
                continue
            print(key)


def main():
    b = Board(4)
    b.play()


if __name__ == '__main__':
    main()
