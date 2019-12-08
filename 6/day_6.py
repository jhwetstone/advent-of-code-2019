import copy
import numpy as np
import sys

sys.path.append("/Users/jessicawetstone/advent-of-code-2019/")
import test_utils

def read_input(file_name):
    with open(file_name,"r") as f:
        raw_codes = [x.strip().split(')') for x in f.readlines()]
    return raw_codes

class Planet:
    
    def __init__(self, name):
        self.name = name
        self.orbitters = []
        self.orbit = None
    
    def add_orbitter(self, orbitter):
        self.orbitters.append(orbitter)
    
    def add_orbit(self, planet):
        self.orbit = planet

def load_planets(filename):
    raw_input = read_input(filename)
    planets = {}
    for planet, orbiter in raw_input:
        if planet not in planets:
            planets[planet] = Planet(planet)

        if orbiter not in planets:
            planets[orbiter] = Planet(orbiter)

        planets[planet].add_orbitter(orbiter)
        planets[orbiter].add_orbit(planet)
    return planets

def count_all_orbits(filename):
    planets = load_planets(filename)
    root = 'COM'
    to_visit = [(x, 1) for x in planets[root].orbitters]
    total = 0
    while not len(to_visit) == 0:
        next_planet, depth = to_visit.pop()
        total += depth
        to_visit += [(x, depth + 1) for x in planets[next_planet].orbitters]
    return total

test_utils.run_tests_for_part(1, [
    ("6/test.txt", 42),
], count_all_orbits)

print(f"Part 1 answer: {count_all_orbits('6/input.txt')}")

def find_ancestors(filename, current):
    ancestors = {}
    depth = 0
    planets = load_planets(filename)
    while planets[current].orbit is not None:
        depth = depth + 1
        ancestors[planets[current].orbit] = depth
        current = planets[current].orbit
    return ancestors

def find_common_ancestors_with_santa(filename):
    santas_ancestors = find_ancestors(filename, 'SAN')
    your_ancestors = find_ancestors(filename, 'YOU')
    common_keys = set(santas_ancestors.keys()).intersection(set(your_ancestors.keys()))
    min_distance = np.inf
    min_ancestor = None
    for key in common_keys:
        distance = santas_ancestors[key] + your_ancestors[key] - 2
        if distance < min_distance:
            min_distance = distance
            min_ancestor = key
    return min_distance
        
test_utils.run_tests_for_part(2, [
    ("6/test_2.txt", 4),
], find_common_ancestors_with_santa)

print(f"Part 2 answer: {find_common_ancestors_with_santa('6/input.txt')}")