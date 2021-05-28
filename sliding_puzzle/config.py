import argparse
import os.path
import re
from typing import Optional, Collection, Tuple, List


def get_parsed_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('-r', '--rows-num', metavar='NUM', type=int, help='Number of rows on the board')
    arg_parser.add_argument('-c', '--columns-num', metavar='NUM', type=int, help='Number of columns on the board')
    arg_parser.add_argument('-f', '--board-file', metavar='FILE', help='File containing board data')
    arg_parser.add_argument('-v', '--values',
                            help='Tiles values, should be in form of quotation marks enclosed, '
                                 'comma separated list ie. "1, 9, 8, 12"')

    parsed_args = arg_parser.parse_args()
    validate_parsed_args(parsed_args)
    return parsed_args


def validate_parsed_args(parsed_args: argparse.Namespace):
    if parsed_args.board_file:
        if any((parsed_args.rows_num, parsed_args.columns_num, parsed_args.values)):
            raise AttributeError('--rows-num, --columns-num, --values cannot be used when board file is specified')

        if not os.path.exists(parsed_args.board_file):
            raise FileNotFoundError(f'Provided file: {parsed_args.board_file} was not found')

    if parsed_args.values and not re.match(r'^(?:\d+,\s*)+\d+$', parsed_args.values):
        raise ValueError('Provided values sequence does not fit expected pattern')

    for arg_name, arg_value in {'rows_num': parsed_args.rows_num, 'columns_num': parsed_args.columns_num}.items():
        if arg_value and arg_value < 2:
            raise ValueError(f'{arg_name} value must be no less than 2, provided: {arg_value}')


def get_dimensions_and_values_from_file(file_path: str) -> Tuple[List[int], List[int]]:
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


def get_values_from_args(args: argparse.Namespace) -> Optional[List[int]]:
    return [int(x) for x in re.split(r',\s?', args.values)] if args.values else None
