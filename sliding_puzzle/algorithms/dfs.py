from __future__ import annotations

import time
from copy import copy
from typing import List

from sliding_puzzle.board import Board

visited = set()
max_level = 100

# goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

order = 'rdul'


class DFSNode:
    def __init__(self, board: Board, level: int = 0, leading_moves: List[str] = None):
        self.board = board
        self.level = level
        self.leading_moves = leading_moves.copy() if leading_moves else []

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.board == other.board  # and self.level == other.level

    def __hash__(self) -> int:
        # return hash((self.board, self.level))
        return hash(self.board)

    def __str__(self) -> str:
        return f"""start: level => {self.level} | visited len => {len(visited)} ===================================================================
{self.board}
{self.leading_moves}
end: ==================================================================================================="""


def dfs(current_node: DFSNode):
    visited.add(current_node)
    if list(current_node.board.tiles.values()) == goal_state:
        print("DONE")
        return current_node

    if current_node.level == max_level:
        print("MAX_LEVEL")
        return

    available_moves = current_node.board.get_available_moves()
    for o in order:
        if o in available_moves:
            next_node = DFSNode(
                board=Board(rows_num=current_node.board.rows_num, columns_num=current_node.board.columns_num,
                            tiles=current_node.board.tiles), level=current_node.level,
                leading_moves=current_node.leading_moves)
            next_node.level += 1
            next_node.board.move(o)
            next_node.leading_moves.append(o)
            if next_node not in visited:
                result = dfs(next_node)
                if result:
                    return result


if __name__ == '__main__':
    b = Board(4, 4, [1, 2, 3, 4,
                     5, 6, 7, 8,
                     9, 10, 12, 0,
                     13, 14, 11, 15])
    # b.play()
    # b = Board(4, 4, [3, 5, 12, 13, 4, 2, 9, 11, 7, 1, 14, 10, 6, 8, 0, 15])

    node = DFSNode(b)

    start_time = time.time()
    dfs(current_node=node)
    print(f'Constructor: {time.time() - start_time}')
# ['d', 'l', 'u', 'r', 'd', 'l', 'u', 'r', 'd']
