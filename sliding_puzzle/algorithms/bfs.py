from __future__ import annotations

from typing import Iterable, Optional, Tuple, List

from sliding_puzzle.board import Board
from sliding_puzzle.decorators import timer


class BFSNode:
    __slots__ = 'board', 'leading_move', 'parent_node'

    def __init__(self, board: Board, leading_move: str = None, parent_node: BFSNode = None):
        self.board = board
        self.leading_move = leading_move
        self.parent_node = parent_node


@timer
def bfs(root_node: BFSNode, order: Iterable[str]) -> Tuple[Optional[BFSNode], int, int]:
    processed_count = 0

    visited_nodes = set()
    open_nodes = [root_node]

    while len(open_nodes) > 0:
        current_node: BFSNode = open_nodes.pop(0)
        visited_nodes.add(current_node)

        processed_count += 1

        if current_node.board.is_solved():
            return current_node, len(visited_nodes) + len(open_nodes), processed_count

        for move in order:
            if move in current_node.board.get_available_moves():
                new_board = Board(current_node.board.rows_num, current_node.board.rows_num,
                                  tiles=current_node.board.tiles)
                new_board.move(move)

                new_node = BFSNode(new_board, move, parent_node=current_node)

                if new_node in visited_nodes:
                    continue

                open_nodes.append(new_node)
    return None, 0, 0  # default return values, should never be reached, stated to satisfy mypyc


def get_path_to_solved(final_node: BFSNode) -> List[Optional[str]]:
    current_node = final_node
    path = []

    while current_node.parent_node:
        path.append(current_node.leading_move)
        current_node = current_node.parent_node

    return path[::-1]


def bfs_main(initial_board, move_order: str) -> Tuple[List[Optional[str]], int, int, int, str]:
    node = BFSNode(initial_board)
    (final_node, visited_count, processed_count), execution_time = bfs(node, move_order)

    path = get_path_to_solved(final_node)

    return path, visited_count, processed_count, len(path), f'{execution_time:.3f}'
