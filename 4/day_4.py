import copy
import numpy as np
import sys

sys.path.append("/Users/jessicawetstone/advent-of-code-2019/")
import test_utils

number_range = [240298,784956]

def meetsCriteria(num):
    prev_digit = -1
    one_double = False
    for digit in str(num):
        if int(digit) < int(prev_digit):
            return False
        if digit == prev_digit:
            one_double = True
        prev_digit = digit
    return one_double
        
test_utils.run_tests_for_part(1, [
    (111111, True),
    (223450, False),
    (123789, False)
], meetsCriteria)

count = 0
for num in range(number_range[0], number_range[1] + 1):
    if meetsCriteria(num):
        count += 1
        #print(num)

print(f"Part 1 answer: {count}")

def meetsCriteriaTwo(num):
    num_str = str(num)
    prev_digit = int(num_str[0])
    chain_length = 1
    chain_of_two = False
    for idx in range(1, len(num_str)):
        digit = int(num_str[idx])
        if digit > prev_digit:
            if chain_length == 2:
                chain_of_two = True
            chain_length = 1      
        if digit < prev_digit:
            return False
        if digit == prev_digit:
            chain_length += 1
        prev_digit = digit
    if chain_length == 2:
        chain_of_two = True
    return chain_of_two

test_utils.run_tests_for_part(2, [
    (112233, True),
    (123444, False),
    (111122, True)
], meetsCriteriaTwo)

count = 0
for num in range(number_range[0], number_range[1] + 1):
    if meetsCriteriaTwo(num):
        count += 1
        #print(num)

print(f"Part 2 answer: {count}")