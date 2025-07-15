# math_operations/reduction_ops.py
from typing import List, Union, Callable
from functools import reduce

def reduce_numbers(numbers: List[Union[int, float]], operation: str) -> Union[int, float]:
    ops = {
        'add': lambda x, y: x + y,
        'subtract': lambda x, y: x - y,
        'multiply': lambda x, y: x * y,
        'divide': lambda x, y: x / y if y != 0 else float('inf')
    }
    return reduce(ops[operation], numbers)
