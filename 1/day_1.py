import numpy as np
import sys

sys.path.append("/Users/jessicawetstone/advent-of-code-2019/")
import test_utils

with open("1/input.txt","r") as f:
    masses = [int(x.strip()) for x in f.readlines()]

def calculateFuel(mass):
    return mass // 3 - 2

test_utils.run_tests_for_part(1, [(12,2),(14,2),(1969,654),(100756,33583)], calculateFuel)

## Question 1
fuel_reqs = np.sum([calculateFuel(m) for m in masses])

print(f"Part 1 answer: {fuel_reqs}")

def calculateFuelRecursive(mass):
    fuel = calculateFuel(mass)
    if fuel <= 0:
        return 0
    else:
        return fuel + calculateFuelRecursive(fuel)

test_utils.run_tests_for_part(2, [(14,2),(1969,966),(100756,50346)], calculateFuelRecursive)
    
## Question 2
fuel_reqs = np.sum([calculateFuelRecursive(m) for m in masses])

print(f"Part 2 answer: {fuel_reqs}")

