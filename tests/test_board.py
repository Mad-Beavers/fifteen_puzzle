from typing import Sequence

from sliding_puzzle.board import Board


def test_get_inversions_count(expected_values_dict: dict[Sequence[int], int]):
    for key, value in expected_values_dict.items():
        assert Board.get_inversions_count(key) == value


def test_is_solvable(board_solvable_dict: [Board, bool]):
    for board, expected_is_solvable in board_solvable_dict.items():
        assert board.is_solvable() == expected_is_solvable
