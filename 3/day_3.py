import copy
import numpy as np
import sys

sys.path.append("/Users/jessicawetstone/advent-of-code-2019/")
import test_utils

def read_input(file_name):
    with open(file_name, "r") as f:
        raw_codes = [x.strip().split(',') for x in f.readlines()]
    
    return raw_codes

def find_intersections(raw_codes):
    locations = {}
    for idx in (0,1):
        instructions = raw_codes[idx]
        cur_locations = []
        x_idx = 0
        y_idx = 0
        for instruct in instructions:
            direction = instruct[0]
            count = int(instruct[1:])
            if direction == 'U':
                cur_locations += [(x_idx, y_idx + el) for el in range(1, count+1)]
                y_idx = y_idx + count
            elif direction == 'D':
                cur_locations += [(x_idx, y_idx - el) for el in range(1, count+1)]
                y_idx = y_idx - count
            elif direction == 'R':
                cur_locations += [(x_idx + el, y_idx) for el in range(1, count+1)]
                x_idx = x_idx + count
            elif direction == 'L':
                cur_locations += [(x_idx - el, y_idx) for el in range(1, count+1)]
                x_idx = x_idx - count
        locations[idx] = cur_locations

    intersects = set(locations[0]).intersection(set(locations[1]))
    return intersects
    
def calculateDistanceToClosestIntersection(raw_codes):    
    intersects = find_intersections(raw_codes)
    result = sorted(intersects, key=lambda x: abs(x[0]) + abs(x[1]), reverse=False)[0]
    return abs(result[0]) + abs(result[1])

test_utils.run_tests_for_part(1, [
    (read_input("3/test_1.txt"), 159),
    (read_input("3/test_2.txt"), 135)
], calculateDistanceToClosestIntersection)

print(f"Part 1 answer: {calculateDistanceToClosestIntersection(read_input('3/input.txt'))}")
      
def find_intersections_part_2(raw_codes):
    locations = {}
    for idx in (0,1):
        instructions = raw_codes[idx]
        cur_locations = []
        x_idx = 0
        y_idx = 0
        total_steps = 0
        for instruct in instructions:
            direction = instruct[0]
            count = int(instruct[1:])
            if direction == 'U':
                cur_locations += [(x_idx, y_idx + el, total_steps + el) for el in range(1, count+1)]
                y_idx = y_idx + count
            elif direction == 'D':
                cur_locations += [(x_idx, y_idx - el, total_steps + el) for el in range(1, count+1)]
                y_idx = y_idx - count
            elif direction == 'R':
                cur_locations += [(x_idx + el, y_idx, total_steps + el) for el in range(1, count+1)]
                x_idx = x_idx + count
            elif direction == 'L':
                cur_locations += [(x_idx - el, y_idx, total_steps + el) for el in range(1, count+1)]
                x_idx = x_idx - count
            total_steps += count
        locations[idx] = cur_locations
      
    location_dicts = []
    for idx in (0,1):
        location_dict = {}
        for x, y, ct in locations[idx]:
            if (x,y) not in locations:
                location_dict[(x,y)] = ct
        location_dicts.append(location_dict)
      
    return location_dicts, set(location_dicts[0].keys()).intersection(set(location_dicts[1].keys()))

def calculateDistanceToClosestIntersection_part_2(raw_codes):    
    location_dicts, intersects = find_intersections_part_2(raw_codes)
    result = sorted(intersects, key=lambda x: location_dicts[0][x] + location_dicts[1][x], reverse=False)[0]
    return location_dicts[0][result] + location_dicts[1][result]
      
test_utils.run_tests_for_part(2, [
    (read_input("3/test_1.txt"), 610),
    (read_input("3/test_2.txt"), 410)
], calculateDistanceToClosestIntersection_part_2)

print(f"Part 2 answer: {calculateDistanceToClosestIntersection_part_2(read_input('3/input.txt'))}")