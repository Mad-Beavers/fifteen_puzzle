from __future__ import annotations

import time
from copy import deepcopy
from typing import Optional, Dict, Iterable

from sliding_puzzle.board import Board
from sliding_puzzle.config import get_dimensions_and_values_from_file


def timer(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        print(f'Function "{function.__name__}" execution took {time.time() - start_time}s')
        return result

    return wrapper


class AStarNode:
    __slots__ = 'board', 'parent_node', 'level', 'leading_move', 'h', 'total_cost'

    def __init__(self, board: Board, heuristic: str, parent_node: AStarNode = None,
                 level: int = 0, leading_move: str = None):
        self.board = board
        self.parent_node = parent_node
        self.level = level
        self.leading_move = leading_move
        self.h = self.get_h(heuristic)
        self.total_cost = self.level + self.h

    def get_h(self, heuristic: str) -> int:
        if heuristic.lower() == 'manhattan':
            return get_manhattan_distance_value(self.board)
        if heuristic.lower() == 'hamming':
            return get_hamming_distance(self.board)
        raise AttributeError(f'Unsupported heuristic: {heuristic}')

        # return {'manhattan': get_manhattan_distance_value,
        #         'hamming': get_hamming_distance}[heuristic.lower()](self.board)

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.board == other.board

    def __hash__(self) -> int:
        return hash(self.board)

    # @property
    # def total_cost(self) -> int:
    #     return self.g + self.h


def get_hamming_distance(board: Board) -> int:
    return sum(1 for tile_pos in board.tiles if board.get_tile_distance_from_solved(tile_pos) != 0)


def get_manhattan_distance_value(board: Board) -> int:
    return sum(board.get_tile_distance_from_solved(tile_pos) for tile_pos, val in board.tiles.items() if val != 0)


@timer
def a_star(board_______: Board, heuristic: str) -> Optional[AStarNode]:
    counter = 0
    start_node = AStarNode(board_______, heuristic)
    # open_nodes: Dict[AStarNode, int, int] = {start_node: start_node.total_cost}
    # visited_nodes = {}

    open_nodes = {start_node}
    visited_nodes = set()

    while len(open_nodes) > 0:
        current_node: AStarNode = min(open_nodes, key=lambda x: x.total_cost)

        if current_node.board.is_solved():
            print('Done')
            print(current_node.board)
            return current_node

        open_nodes.discard(current_node)
        visited_nodes.add(current_node)

        for move in current_node.board.get_available_moves():
            new_board = Board(current_node.board.rows_num, current_node.board.columns_num,
                              tiles=current_node.board.tiles)
            # print(move)

            # print(current_node.board)
            new_board.move(move)
            # counter += 1
            # if counter % 10000 == 0:
            #     print(new_board)
            #     print(counter)

            new_node = AStarNode(new_board, heuristic, current_node, current_node.level + 1, move)

            # print(new_node.board)

            if new_node in visited_nodes:
                continue

            open_nodes.add(new_node)


def get_path_to_solved(final_node: AStarNode) -> Iterable[str]:
    current_node = final_node
    path = []

    while current_node.parent_node:
        path.append(current_node.leading_move)
        current_node = current_node.parent_node

    return reversed(path)


if __name__ == '__main__':
    # args = get_parsed_args()
    # board_file = r'../../generated_puzzles/4x4_13_06588.txt'
    board_file = r'../../generated_puzzles/4x4_13_06589.txt'

    (rows_num, columns_num), values = get_dimensions_and_values_from_file(board_file)
    # values = [3, 5, 12, 13, 4, 2, 9, 11, 7, 1, 14, 10, 6, 8, 0, 15]

    # getting kwargs dict and filtering non-None values
    board_kwargs = {name: value for name, value
                    in {'columns_num': columns_num,
                        'rows_num': rows_num,
                        'values': values}.items() if value}

    board = Board(**board_kwargs)
    print(board.is_solvable())
    # x = a_star(board, 'hamming')

    x = a_star(board, 'hamming')

    # x = a_star(board, 'manhattan')

    print(list(get_path_to_solved(x)))
    board.play()

    # start_time = time.time()
    # for _ in range(100_000):
    #     z = board.is_solved()
    # print(time.time() - start_time)
    # ['u', 'r', 'd', 'r', 'u', 'l', 'l', 'd', 'r', 'u', 'r', 'r', 'd'] hamming
