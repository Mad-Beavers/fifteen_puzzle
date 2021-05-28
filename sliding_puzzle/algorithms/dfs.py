from __future__ import annotations

import time
from typing import Optional, Iterable

from sliding_puzzle.board import Board

visited = set()

max_recursion_depth = 0

max_recursion_level = 20


class DFSNode:
    def __init__(self, board: Board, level: int = 0, leading_moves: list[str] = None):
        self.board = board
        self.level = level
        self.leading_moves = leading_moves.copy() if leading_moves else []

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.board == other.board

    def __hash__(self) -> int:
        return hash(self.board)


def dfs(current_node: DFSNode, order: Iterable[str], max_level: int, depth: int = 0) -> Optional[DFSNode]:
    global max_recursion_depth
    if depth > max_recursion_depth:
        max_recursion_depth = depth

    visited.add(current_node)
    if current_node.board.is_solved():
        return current_node

    if current_node.level == max_level:
        return

    for move in order:
        if move in current_node.board.get_available_moves():
            next_node = DFSNode(
                board=Board(rows_num=current_node.board.rows_num, columns_num=current_node.board.columns_num,
                            tiles=current_node.board.tiles), level=current_node.level + 1,
                leading_moves=current_node.leading_moves)

            next_node.board.move(move)
            next_node.leading_moves.append(move)

            if next_node not in visited:

                if result := dfs(next_node, order, max_level, depth + 1):
                    return result


def dfs_main(input_board: Board, order: Iterable[str], max_level: int = max_recursion_level) -> tuple[list[str], int,
                                                                                                      int, int, str]:
    node = DFSNode(input_board)

    start_time = time.time()
    result_node = dfs(node, order, max_level)
    execution_time = time.time() - start_time

    path = result_node.leading_moves if result_node else []

    return path, len(visited), len(visited), max_recursion_depth, f'{execution_time:.3f}'
