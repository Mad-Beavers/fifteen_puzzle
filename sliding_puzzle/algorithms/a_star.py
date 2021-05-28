from __future__ import annotations

from typing import Optional, Iterable

from sliding_puzzle.board import Board
from sliding_puzzle.decorators import timer


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
        return {'manh': get_manh_distance_value,
                'hamm': get_hamm_distance}[heuristic.lower()](self.board)

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.board == other.board

    def __hash__(self) -> int:
        return hash(self.board)


def get_hamm_distance(board: Board) -> int:
    return sum(1 for tile_pos, val in board.tiles.items()
               if val != 0 and board.get_tile_distance_from_solved(tile_pos) != 0)


def get_manh_distance_value(board: Board) -> int:
    return sum(board.get_tile_distance_from_solved(tile_pos) for tile_pos, val in board.tiles.items() if val != 0)


def sort_key(node: AStarNode) -> int:
    return node.total_cost


@timer
def a_star(initial_board: Board, heuristic: str) -> tuple[Optional[AStarNode], int, int, int]:
    processed_count = 0
    max_depth = 0

    start_node = AStarNode(initial_board, heuristic)

    open_nodes = [start_node]
    visited_nodes = set()

    while len(open_nodes) > 0:
        open_nodes.sort(key=sort_key)
        current_node: AStarNode = open_nodes.pop(0)
        visited_nodes.add(current_node)

        processed_count += 1

        if current_node.board.is_solved():
            return current_node, len(visited_nodes) + len(open_nodes), processed_count, max_depth

        for move in current_node.board.get_available_moves():
            new_board = Board(current_node.board.rows_num, current_node.board.columns_num,
                              tiles=current_node.board.tiles)

            new_board.move(move)

            new_node = AStarNode(new_board, heuristic, current_node, current_node.level + 1, move)
            if new_node.level > max_depth:
                max_depth = new_node.level

            if new_node in visited_nodes:
                continue

            open_nodes.append(new_node)


def get_path_to_solved(final_node: AStarNode) -> Iterable[str]:
    current_node = final_node
    path = []

    while current_node.parent_node:
        path.append(current_node.leading_move)
        current_node = current_node.parent_node

    return reversed(path)


def a_star_main(initial_board: Board, heuristic: str) -> tuple[list[str], int, int, int, str]:
    (final_node, visited_count, processed_count, max_depth), execution_time = a_star(initial_board, heuristic)

    path = list(get_path_to_solved(final_node))

    return path, visited_count, processed_count, max_depth, f'{execution_time:.3f}'
