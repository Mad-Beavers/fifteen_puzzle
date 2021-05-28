import argparse
import os.path
from typing import Collection


def get_parsed_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('algorithm', choices=['bfs', 'dfs', 'astr'],
                            help='Algorithm used for calculations')
    arg_parser.add_argument('order', help='Move order | heuristic')
    arg_parser.add_argument('board_file', metavar='FILE', help='File containing board data')
    arg_parser.add_argument('solution_file', metavar='FILE', help='Solution file')
    arg_parser.add_argument('stats_file', metavar='FILE', help='Stats file')

    parsed_args = arg_parser.parse_args()
    validate_parsed_args(parsed_args)
    return parsed_args


def validate_parsed_args(parsed_args: argparse.Namespace):
    if parsed_args.board_file and not os.path.exists(parsed_args.board_file):
        raise FileNotFoundError(f'Provided file: {parsed_args.board_file} was not found')


def get_dimensions_and_values_from_file(file_path: str) -> tuple[list[int], list[int]]:
    with open(file_path, 'r') as f:
        dimensions = [int(val) for val in f.readline().split()]

        if len(dimensions) != 2:
            raise ValueError(f'2 dimensions expected, provided: {len(dimensions)}')

        values = [int(val) for val in f.read().split()]

    validate_values_len(*dimensions, values=values)
    return dimensions, values


def validate_values_len(rows_num: int, columns_num: int, values: Collection[int]):
    if len(values) != rows_num * columns_num:
        raise EOFError(f'Number of values: {len(values)} '
                       f'does not match provided dimensions: {rows_num}x{columns_num}')
