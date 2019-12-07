import copy
import numpy as np
import sys

sys.path.append("/Users/jessicawetstone/advent-of-code-2019/")
import test_utils

with open("2/input.txt","r") as f:
    raw_codes = [int(x) for x in f.read().strip().split(",")]
    
def IntCodePt1(raw_codes):
    codes = copy.deepcopy(raw_codes)
    
    curPosition = 0

    while curPosition < len(codes):
        curOpcode = codes[curPosition]
        if curOpcode not in (1,2):
            break
        elif curOpcode == 1:
            val = codes[codes[curPosition + 1]] + codes[codes[curPosition + 2]]
        elif curOpcode == 2:
            val = codes[codes[curPosition + 1]] * codes[codes[curPosition + 2]]

        codes[codes[curPosition + 3]] = val    
        curPosition = curPosition + 4
        
    return codes

test_utils.run_tests_for_part(1, [
    ([1,0,0,0,99], [2,0,0,0,99]),
    ([2,3,0,3,99], [2,3,0,6,99]),
    ([2,4,4,5,99,0], [2,4,4,5,99,9801]),
    ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99]),
], IntCodePt1)

codes = copy.deepcopy(raw_codes)
codes[1] = 12
codes[2] = 2
res = IntCodePt1(codes)

print(f"Part 1 answer: {res[0]}")

def IntCode(noun, verb, raw_codes):
    codes = copy.deepcopy(raw_codes)
    codes[1] = noun
    codes[2] = verb
    
    curPosition = 0
    while curPosition < len(codes):
        curOpcode = codes[curPosition]
        if curOpcode not in (1,2):
            break
        elif curOpcode == 1:
            val = codes[codes[curPosition + 1]] + codes[codes[curPosition + 2]]
        elif curOpcode == 2:
            val = codes[codes[curPosition + 1]] * codes[codes[curPosition + 2]]

        codes[codes[curPosition + 3]] = val    
        curPosition = curPosition + 4
    return codes[0]

def gridSearch():
    for noun in range(99):
        for verb in range(99):
            result = IntCode(noun, verb, raw_codes)
            if result == 19690720:
                return noun, verb

noun, verb = gridSearch()

print(f"Part 2 answer: {100 * noun + verb}")