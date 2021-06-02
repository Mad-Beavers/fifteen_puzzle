import os
import re

from concurrent.futures import ThreadPoolExecutor


def main():
    init_file_name_regex = re.compile(r'^[a-zA-Z0-9]+_[0-9]+_[0-9]+.txt$')
    orders = ('RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD')
    heuristics = ('manh', 'hamm')
    brute_force_methods = ('bfs', 'dfs')
    a_star = 'astr'
    program_command = 'python3.9 -m sliding_puzzle.main'
    files = [f for f in os.listdir('.') if os.path.isfile(f) and init_file_name_regex.match(f)]
    # astr manh 4x4_01_00001.txt solution.txt stats.txt

    with ThreadPoolExecutor(max_workers=3) as executor:
        for file in files:
            executor.submit(sub_method, brute_force_methods, file, heuristics, orders, program_command)


def sub_method(brute_force_methods, file, heuristics, orders, program_command):
    base_file_name = file[:-4]
    print(base_file_name)
    with ThreadPoolExecutor() as executor:
        for method in brute_force_methods:
            for order in orders:
                executor.submit(os.system,
                                f'{program_command} {method} {order} {file} stats/{base_file_name}_{method}_{order.lower()}_sol.txt stats/{base_file_name}_{method}_{order.lower()}_stats.txt')
        for heuristic in heuristics:
            executor.submit(os.system,
                            f'{program_command} astr {heuristic} {file} stats/{base_file_name}_astr_{heuristic}_sol.txt stats/{base_file_name}_astr_{heuristic}_stats.txt')


if __name__ == '__main__':
    main()
