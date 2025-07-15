# math_operations/multiply_ops.py
from typing import List, Union
from functools import reduce
import operator

def multiply_numbers(numbers: List[Union[int, float]]) -> Union[int, float]:
    return reduce(operator.mul, numbers, 1)
