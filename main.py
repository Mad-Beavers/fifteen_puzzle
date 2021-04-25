import argparse

from board import Board


def validate_parsed_args(parsed_args: argparse.Namespace):
    if parsed_args.board_size and parsed_args.board_size <= 1:
        raise ValueError(f'Board size value must be no less than 2, provided: {parsed_args.board_size}')


def get_parsed_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('-s', '--board-size', metavar='NUM', type=int, help='Size of the board used in simulation')

    parsed_args = arg_parser.parse_args()
    validate_parsed_args(parsed_args)
    return parsed_args


def main():
    args = get_parsed_args()
    board = Board(args.board_size if args.board_size else 4)
    print(board)
    # board.play()
    print(board._board_size)


if __name__ == '__main__':
    main()
