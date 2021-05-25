from __future__ import annotations

import time
from copy import deepcopy
from typing import Optional, Dict

from sliding_puzzle.board import Board


class AStarNode:

    def __init__(self, board: Board, heuristic: str, parent_node: AStarNode = None,
                 g: int = 0, leading_move: str = None):
        self.board = board
        self.heuristic = heuristic
        self.parent_node = parent_node
        self.g = g
        self.leading_move = leading_move
        self.h = self.get_h()
        self.total_cost = self.g + self.h

    def get_h(self) -> int:
        if self.heuristic.lower() == 'manhattan':
            return get_manhattan_distance_value(self.board)
        if self.heuristic.lower() == 'hamming':
            return get_hamming_distance(self.board)
        raise AttributeError(f'Unsupported heuristic: {self.heuristic}')

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

            new_node = AStarNode(new_board, heuristic, current_node, g=current_node.g + 1,
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
    # # b = Board(4, 4, [0, 1, 2, 11, 5, 4, 7, 6, 10, 9, 8, 3, 14, 15, 12, 13])
    # b = Board(3, 3)
    # start_time = time.time()
    # for _ in range(100_000):
    #     b.move(random.choice(b.get_available_moves()))
    # print(f'moves {time.time() - start_time}')
    #
    # start_time = time.time()
    # for _ in range(100_000):
    #     b.get_available_moves()
    # print(time.time() - start_time)
    # print(b.is_solvable())
    # a_star(b, 'manhattan')
    b = Board(4, 4)
    start_time = time.time()
    for _ in range(100_000):
        x = deepcopy(b)
    print(f'Deepcopy: {time.time() - start_time}')

    # start_time = time.time()
    # for _ in range(100_000):
    #     x = b.tiles
    # print(time.time() - start_time)

    start_time = time.time()
    for _ in range(100_000):
        x = Board(4, 4, tiles=b.tiles)
    print(f'Constructor: {time.time() - start_time}')
