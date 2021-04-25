import argparse

from board import Board


def get_parsed_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('-r', '--rows-num', metavar='NUM', type=int, help='Number of rows on the board')
    arg_parser.add_argument('-c', '--columns-num', metavar='NUM', type=int, help='Number of columns on the board')

    parsed_args = arg_parser.parse_args()
    validate_parsed_args(parsed_args)
    return parsed_args


def validate_parsed_args(parsed_args: argparse.Namespace):
    for arg_name, arg_value in {'rows_num': parsed_args.rows_num, 'columns_num': parsed_args.columns_num}.items():
        if arg_value and arg_value < 2:
            raise ValueError(f'{arg_name} value must be no less than 2, provided: {arg_value}')


def main():
    args = get_parsed_args()

    # getting kwargs dict and filtering non-None values
    board_kwargs = {name: value for name, value
                    in {'columns_num': args.columns_num, 'rows_num': args.rows_num}.items() if value}

    board = Board(**board_kwargs)

    board.play()


if __name__ == '__main__':
    main()
