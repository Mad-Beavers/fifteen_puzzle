from __future__ import annotations

import time
from copy import deepcopy
from typing import Optional, Dict

from sliding_puzzle.board import Board
from sliding_puzzle.config import get_dimensions_and_values_from_file


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
    return sum(1 for tile_pos in board.tiles if board.get_tile_distance_from_solved(tile_pos) == 0)


def get_manhattan_distance_value(board: Board) -> int:
    return sum(board.get_tile_distance_from_solved(tile_pos) for tile_pos, val in board.tiles.items() if val != 0)


def a_star(board: Board, heuristic: str) -> Optional[AStarNode]:
    starting_node = AStarNode(board, heuristic)
    # open_nodes_dict: dict[Board, AStarNode] = {starting_node.board: starting_node}
    # open_nodes: set[AStarNode] = {starting_node}
    open_nodes: Dict[AStarNode, int] = {starting_node: starting_node.total_cost}
    closed_nodes: Dict[AStarNode, int] = {}
    # closed_nodes_dict: dict[Board, AStarNode] = {}

    counter = 0
    super_start_time = time.time()
    while len(open_nodes) > 0:
        # current_node = open_nodes_dict.pop(min(open_nodes_dict, key=lambda k: open_nodes_dict[k].total_cost))
        start_time = time.time()
        current_node: AStarNode = min(open_nodes, key=open_nodes.get)
        open_nodes.pop(current_node)
        closed_nodes[current_node] = current_node.total_cost

        stop_time = time.time() - start_time
        # if counter % 1000 == 0:
        #     print(f'{stop_time=}')

        # print(current_node.total_cost, counter, current_node.leading_move)
        # closed_nodes_dict |= {current_node.board: current_node}

        if current_node.board.is_solved():
            print('Yo, I made it!')
            return current_node

        for move in current_node.board.get_available_moves():
            counter += 1
            if counter % 20_000 == 0:
                print(f'super stop time = {time.time() - super_start_time}')
                super_start_time = time.time()
            # if counter % 1000 == 0:
            #     print(current_node.board)
            #     print(current_node.h)
            # print(counter)
            new_board = deepcopy(current_node.board)
            new_board.move(move)

            new_node = AStarNode(new_board, heuristic, current_node, level=current_node.level + 1,
                                 leading_move=move)

            # if new_board in open_nodes_dict and open_nodes_dict[new_board].total_cost < new_node.total_cost:
            #     continue

            if new_node in open_nodes and open_nodes[new_node] < new_node.total_cost:
                continue

            # if new_board in closed_nodes_dict and closed_nodes_dict[new_board].total_cost < new_node.total_cost:
            #     continue

            if new_node in closed_nodes and closed_nodes[new_node] < new_node.total_cost:
                continue

            if new_node in open_nodes:
                del open_nodes[new_node]

            if new_node in closed_nodes:
                del closed_nodes[new_node]

            open_nodes[new_node] = new_node.total_cost
    return None


if __name__ == '__main__':
    # args = get_parsed_args()
    board_file = r'../../generated_puzzles/3x3_01_00001.txt'

    (rows_num, columns_num), values = get_dimensions_and_values_from_file(board_file)

    # getting kwargs dict and filtering non-None values
    board_kwargs = {name: value for name, value
                    in {'columns_num': columns_num,
                        'rows_num': rows_num,
                        'values': values}.items() if value}

    board = Board(**board_kwargs)

    start_time = time.time()
    tilezz = board.tiles
    for _ in range(100_000):
        x = hash(frozenset(tilezz.items()))
    print(f'hashing 1 took {time.time() - start_time}')

    for _ in range(100_000):
        x = hash(tuple(tilezz.items()))
    print(f'hashing 2 took {time.time() - start_time}')
