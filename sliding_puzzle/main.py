from board import Board
from config import get_parsed_args, get_dimensions_and_values_from_file
from algorithms.a_star import a_star_main
from sliding_puzzle.algorithms.bfs import bfs_main
from sliding_puzzle.algorithms.dfs import dfs_main


def save_solution_file(file: str, solution: list[str]):
    with open(file, 'w') as f:
        f.write(f'{len(solution)}\n{solution}')


def save_stats_file(file: str, solution_len: int, visited_count: int,
                    processed_count: int, max_recursion_depth: int, execution_time: str):
    with open(file, 'w') as f:
        f.write(f'''{solution_len}
{visited_count}
{processed_count}
{max_recursion_depth}
{execution_time}''')


def main():
    args = get_parsed_args()

    (rows_num, columns_num), values = get_dimensions_and_values_from_file(args.board_file)

    algorithm = args.algorithm[0] if isinstance(args.algorithm, tuple) else args.algorithm
    order = args.order
    solution_file = args.solution_file
    stats_file = args.stats_file

    # getting kwargs dict and filtering non-None values
    board_kwargs = {name: value for name, value
                    in {'columns_num': columns_num,
                        'rows_num': rows_num,
                        'values': values}.items() if value}

    board = Board(**board_kwargs)

    solution, visited_count, processed_count, max_recursion_depth, execution_time = \
        {'astr': a_star_main, 'bfs': bfs_main, 'dfs': dfs_main}[algorithm](board, order)

    path_len = len(solution) if solution else -1

    print(f'''{solution=}
{path_len=}
{visited_count=}
{processed_count=}
{max_recursion_depth=}
{execution_time=}''')

    save_solution_file(solution_file, solution)
    save_stats_file(stats_file, len(solution), visited_count, processed_count, max_recursion_depth, execution_time)


if __name__ == '__main__':
    main()
