import pytest

from sliding_puzzle.board import Board


@pytest.fixture
def expected_values_dict():
    return {(1, 8, 2, 0, 4, 3, 7, 6, 5): 10,
            (13, 2, 10, 3, 1, 12, 8, 4, 5, 0, 9, 6, 15, 14, 11, 7): 41,
            (6, 13, 7, 10, 8, 9, 11, 0, 15, 2, 12, 5, 14, 3, 1, 4): 62,
            (3, 9, 1, 15, 14, 11, 4, 6, 13, 0, 10, 12, 2, 7, 8, 5): 56}


@pytest.fixture
def board_solvable_dict():
    return {
        Board(rows_num=4, columns_num=4,
              values=(0, 7, 1, 4, 5, 2, 6, 3, 9, 10, 14, 8, 13, 11, 12, 15)
              ): True,
        Board(rows_num=4, columns_num=4,
              values=(3, 5, 4, 7, 1, 2, 15, 8, 9, 6, 11, 12, 13, 14, 10, 0)
              ): True,
        Board(rows_num=4, columns_num=4,
              values=(6, 2, 7, 3, 1, 10, 9, 5, 14, 4, 0, 11, 15, 13, 12, 8)
              ): True,
        Board(rows_num=4, columns_num=4,
              values=(0, 7, 1, 4, 5, 2, 6, 3, 10, 9, 14, 8, 13, 11, 12, 15)
              ): False,
        Board(rows_num=4, columns_num=4,
              values=(3, 5, 4, 13, 1, 2, 15, 8, 9, 6, 11, 12, 7, 14, 10, 0)
              ): False,
        Board(rows_num=4, columns_num=4,
              values=(3, 9, 1, 15, 14, 11, 4, 6, 13, 0, 10, 12, 2, 7, 8, 5)
              ): False,
        Board(rows_num=3, columns_num=3,
              values=(1, 8, 2, 0, 4, 3, 7, 6, 5)
              ): True,
        Board(rows_num=3, columns_num=3,
              values=(1, 8, 2, 0, 3, 4, 7, 6, 5)
              ): False
    }
