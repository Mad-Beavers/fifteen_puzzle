import argparse
import os.path


def get_parsed_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('-r', '--rows-num', metavar='NUM', type=int, help='Number of rows on the board')
    arg_parser.add_argument('-c', '--columns-num', metavar='NUM', type=int, help='Number of columns on the board')
    arg_parser.add_argument('-f', '--board-file', metavar='FILE', help='File containing board data')

    parsed_args = arg_parser.parse_args()
    validate_parsed_args(parsed_args)
    return parsed_args


def validate_parsed_args(parsed_args: argparse.Namespace):
    if parsed_args.board_file:
        if parsed_args.rows_num or parsed_args.columns_num:
            raise AttributeError('--rows-num and --columns-num cannot be used when board file is specified')

        if not os.path.exists(parsed_args.board_file):
            raise FileNotFoundError(f'Provided file: {parsed_args.board_file} was not found')

    for arg_name, arg_value in {'rows_num': parsed_args.rows_num, 'columns_num': parsed_args.columns_num}.items():
        if arg_value and arg_value < 2:
            raise ValueError(f'{arg_name} value must be no less than 2, provided: {arg_value}')


def get_dimensions_and_values_from_file(file_path: str) -> tuple[list[int, int], list[int]]:
    with open(file_path, 'r') as f:
        dimensions = [int(val) for val in f.readline().split()]
        values = [int(val) for val in f.read().split()]

    if len(values) != dimensions[0] * dimensions[1]:
        raise EOFError(f'Number of values {len(values)} '
                       f'does not match provided dimensions {dimensions[0]}x{dimensions[1]}')

    return dimensions, values
