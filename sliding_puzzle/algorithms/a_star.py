from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field

from sliding_puzzle.board import Board


@dataclass
class AStarNode:
    board: Board
    heuristic: str
    parent_node: AStarNode = None
    g: int = 0
    # leading_moves: list[str] = field(default_factory=list)
    leading_move: str = None

    def __hash__(self) -> int:
        return hash(self.board)

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.board == other.board

    @property
    def h(self) -> int:
        if self.heuristic.lower() == 'manhattan':
            return get_manhattan_distance_value(self.board)
        if self.heuristic.lower() == 'hamming':
            return get_hamming_distance(self.board)
        raise AttributeError(f'Unsupported heuristic: {self.heuristic}')

    @property
    def total_cost(self) -> int:
        return self.g + self.h


def get_hamming_distance(board: Board) -> int:
    return sum(1 for tile_pos in board.tiles if board.get_tile_distance_from_solved(tile_pos) == 0)


def get_manhattan_distance_value(board: Board) -> int:
    return sum(board.get_tile_distance_from_solved(tile_pos) for tile_pos, val in board.tiles.items() if val != 0)


def a_star(board: Board, heuristic: str) -> AStarNode:
    # if not move_sequence:
    #     move_sequence = []
    # nodes_queue: Deque[AStarNode] = deque()
    starting_node = AStarNode(board, heuristic)
    open_nodes_dict: dict[Board, AStarNode] = {starting_node.board: starting_node}
    closed_nodes_dict: dict[Board, AStarNode] = {}
    # open_nodes = {starting_node}
    # closed_nodes = set()
    counter = 0
    moves = []

    while len(open_nodes_dict) > 0:
        current_node = open_nodes_dict.pop(min(open_nodes_dict, key=lambda k: open_nodes_dict[k].total_cost))

        print(current_node.total_cost, counter, current_node.leading_moves)
        closed_nodes_dict |= {current_node.board: current_node}

        if current_node.board.is_solved():
            print('Yo, I made it!')
            return current_node

        for move in current_node.board.get_available_moves():
            counter += 1
            # print(counter)
            new_board = deepcopy(current_node.board)
            new_board.move(move)

            new_node = AStarNode(new_board, heuristic, current_node, g=current_node.g + 1,
                                 leading_move=move)

            if new_node in closed_nodes_dict or (node := open_nodes_dict.get(new_board)) and node.g <= new_node.g:
                continue

            open_nodes_dict[new_board] = new_node


if __name__ == '__main__':
    b = Board(4, 4, [0, 1, 2, 11, 5, 4, 7, 6, 10, 9, 8, 3, 14, 15, 12, 13])