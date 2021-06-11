from __future__ import annotations

import time
from typing import Optional, Iterable, List, Tuple

from sliding_puzzle.board import Board

visited = set()

max_recursion_depth = 0

max_recursion_level = 20


class DFSNode:
    __slots__ = 'board', 'level', 'parent_node', 'leading_move'

    def __init__(self, board: Board, level: int = 0, leading_move: str = None, parent_node: DFSNode = None):
        self.board = board
        self.level = level
        self.parent_node = parent_node
        self.leading_move = leading_move

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
        return None

    for move in order:
        if move in current_node.board.get_available_moves():
            next_node = DFSNode(
                board=Board(rows_num=current_node.board.rows_num, columns_num=current_node.board.columns_num,
                            tiles=current_node.board.tiles), level=current_node.level + 1,
                leading_move=move, parent_node=current_node)

            next_node.board.move(move)

            if next_node not in visited:
                result = dfs(next_node, order, max_level, depth + 1)
                if result:
                    return result
    return None  # stated to satisfy mypyc


def get_path_to_solved(final_node: DFSNode) -> List[Optional[str]]:
    current_node = final_node
    path = []

    while current_node.parent_node:
        path.append(current_node.leading_move)
        current_node = current_node.parent_node

    return path[::-1]


def dfs_main(input_board: Board, order: Iterable[str], max_level: int = max_recursion_level) -> Tuple[List[Optional[str]],
                                                                                                      int, int, int, str]:
    node = DFSNode(input_board)

    start_time = time.time()
    result_node = dfs(node, order, max_level)
    execution_time = time.time() - start_time

    path = get_path_to_solved(result_node) if result_node else []

    return path, len(visited), len(visited), max_recursion_depth, f'{execution_time:.3f}'
