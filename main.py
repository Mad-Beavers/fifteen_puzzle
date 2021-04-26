from board import Board
from config import get_parsed_args, get_dimensions_and_values_from_file


def main():
    args = get_parsed_args()

    values = None
    if args.board_file:
        (rows_num, columns_num), values = get_dimensions_and_values_from_file(args.board_file)
    else:
        columns_num, rows_num = args.columns_num, args.rows_num

    # getting kwargs dict and filtering non-None values
    board_kwargs = {name: value for name, value
                    in {'columns_num': columns_num,
                        'rows_num': rows_num,
                        'values': values}.items() if value}

    board = Board(**board_kwargs)

    board.play()


if __name__ == '__main__':
    main()
