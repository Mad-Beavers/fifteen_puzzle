from typing import Iterable, Optional

from sliding_puzzle.board import Board
from sliding_puzzle.decorators import timer


class BFSNode:
    def __init__(self, board: Board, leading_moves: list[str] = None):
        self.board = board
        self.leading_moves = leading_moves.copy() if leading_moves else []


@timer
def bfs(root_node: BFSNode, order: Iterable[str]) -> tuple[Optional[BFSNode], int, int, int]:
    processed_count = 0

    visited_nodes = set()
    open_nodes = [root_node]

    while len(open_nodes) > 0:
        current_node: BFSNode = open_nodes.pop(0)
        visited_nodes.add(current_node)

        processed_count += 1

        if current_node.board.is_solved():
            return current_node, len(visited_nodes) + len(open_nodes), processed_count, len(current_node.leading_moves)

        for move in order:
            if move in current_node.board.get_available_moves():
                new_board = Board(current_node.board.rows_num, current_node.board.rows_num,
                                  tiles=current_node.board.tiles)
                new_board.move(move)

                new_node = BFSNode(new_board, current_node.leading_moves)
                new_node.leading_moves.append(move)

                if new_node in visited_nodes:
                    continue

                open_nodes.append(new_node)


def bfs_main(initial_board, move_order: str) -> tuple[list[str], int, int, int, str]:
    node = BFSNode(initial_board)
    (final_node, visited_count, processed_count, max_depth), execution_time = bfs(node, move_order)

    return final_node.leading_moves, visited_count, processed_count, max_depth, f'{execution_time:.3f}'
