import os
import re
from concurrent.futures import ThreadPoolExecutor
from subprocess import Popen

"""
WARNING

The only purpose of this script is to generate solution and stats files from given board input files as fast as possible
Without any adjustment it WILL use 100% CPU and may cause some problems if used without consideration.
"""


def main():
    init_file_name_regex = re.compile(r'^[a-zA-Z0-9]+_[0-9]+_[0-9]+.txt$')
    orders = ('RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD')
    heuristics = ('manh', 'hamm')
    brute_force_methods = ('bfs', 'dfs')
    program_command = 'python3.9 -c "import main; main.main()"'
    files = [f for f in os.listdir('.') if os.path.isfile(f) and init_file_name_regex.match(f)]
    # astr manh 4x4_01_00001.txt solution.txt stats.txt

    with ThreadPoolExecutor(max_workers=4) as executor:
        for file in files:
            executor.submit(sub_method, brute_force_methods, file, heuristics, orders, program_command)


def sub_method(brute_force_methods, input_file, heuristics, orders, program_command):
    base_file_name = input_file[:-4]
    print(base_file_name)
    for method in brute_force_methods:
        for order in orders:
            sol_file = f'../stats/{base_file_name}_{method}_{order.lower()}_sol.txt'
            stats_file = f'../stats/{base_file_name}_{method}_{order.lower()}_stats.txt'

            Popen(
                [f'{program_command} {method} {order} ../{input_file} {sol_file} {stats_file}'],
                shell=True,
                cwd="sliding_puzzle"
            )

    for heuristic in heuristics:
        sol_file = f'../stats/{base_file_name}_astr_{heuristic}_sol.txt'
        stats_file = f'../stats/{base_file_name}_astr_{heuristic}_stats.txt'
        Popen(
            [f'{program_command} astr {heuristic} ../{input_file} {sol_file} {stats_file}'],
            shell=True,
            cwd="sliding_puzzle"
        )


if __name__ == '__main__':
    main()
