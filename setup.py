from setuptools import setup
from mypyc.build import mypycify

setup(
    name='sliding_puzzle_solver',
    packages=['sliding_puzzle', 'sliding_puzzle.algorithms'],
    ext_modules=mypycify([
        'sliding_puzzle/main.py',
        'sliding_puzzle/config.py',
        'sliding_puzzle/__init__.py',
        'sliding_puzzle/board.py',
        'sliding_puzzle/decorators.py',
        'sliding_puzzle/algorithms/__init__.py',
        'sliding_puzzle/algorithms/a_star.py',
        'sliding_puzzle/algorithms/bfs.py',
        'sliding_puzzle/algorithms/dfs.py'
    ])
)
