# math_operations/divide_ops.py
from typing import List, Union
from functools import reduce
import operator

def divide_numbers(numbers: List[Union[int, float]]) -> Union[int, float]:
    """
    Divides a list of numbers sequentially from left to right.
    For example, [10, 2, 2] would calculate as (10 / 2) / 2 = 2.5
    
    Args:
        numbers: List of numbers to divide
    
    Returns:
        The result of the sequential division
    
    Raises:
        ZeroDivisionError: If any number after the first one is zero
    """
    if not numbers:
        raise ValueError("Numbers list cannot be empty")
    return reduce(operator.truediv, numbers)
