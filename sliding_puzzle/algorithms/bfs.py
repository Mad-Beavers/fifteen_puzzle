import time
from typing import List

from sliding_puzzle.board import Board

order = 'ruld'


def timer(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        print(f'Function "{function.__name__}" execution took {time.time() - start_time}s')
        return result

    return wrapper


class BFSNode:
    def __init__(self, board: Board, leading_moves: List[str] = None):
        self.board = board
        self.leading_moves = leading_moves.copy() if leading_moves else []


@timer
def bfs(root_node: BFSNode):
    visited_nodes = set()
    open_nodes = [root_node]

    while len(open_nodes) > 0:
        current_node: BFSNode = open_nodes.pop(0)
        visited_nodes.add(current_node)

        if current_node.board.is_solved():
            print('Done')
            print(current_node.board)
            print(current_node.leading_moves)
            return current_node

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


if __name__ == '__main__':

    # b.play()
    b = Board(4, 4, [3, 5, 12, 13, 4, 2, 9, 11, 7, 1, 14, 10, 6, 8, 0, 15])
    node = BFSNode(b)
    bfs(node)
