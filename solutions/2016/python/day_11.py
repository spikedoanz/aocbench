from collections import deque
from itertools import combinations
import os
import re

def solve(initial_state):
    """
    State format: (elevator_floor, ((gen1_floor, chip1_floor), (gen2_floor, chip2_floor), ...))
    """
    def is_valid(state):
        elevator, items = state
        
        # Check each chip
        for i, (gen_floor, chip_floor) in enumerate(items): # If chip is with its generator, it's safe
            if gen_floor == chip_floor:
                continue
            
            # Check if chip is on same floor as any other generator
            for j, (other_gen_floor, _) in enumerate(items):
                if i != j and other_gen_floor == chip_floor:
                    return False  # Chip would be fried
        return True
    
    def is_goal(state):
        _, items = state
        return all(g == 3 and c == 3 for g, c in items)
    
    def get_moves(state):
        elevator, items = state
        moves = []
        
        # Find all items on current floor
        moveable = []
        for i, (g, c) in enumerate(items):
            if g == elevator:
                moveable.append(('g', i))
            if c == elevator:
                moveable.append(('c', i))
        
        # Try moving 1 or 2 items
        for direction in [-1, 1]:
            new_floor = elevator + direction
            if not (0 <= new_floor <= 3):
                continue
            
            # Move 1 item
            for item_type, idx in moveable:
                new_items = list(items)
                g, c = new_items[idx]
                if item_type == 'g':
                    new_items[idx] = (new_floor, c)
                else:
                    new_items[idx] = (g, new_floor)
                moves.append((new_floor, tuple(new_items)))
            
            # Move 2 items
            for (t1, i1), (t2, i2) in combinations(moveable, 2):
                new_items = list(items)
                g1, c1 = new_items[i1]
                g2, c2 = new_items[i2]
                
                if t1 == 'g':
                    new_items[i1] = (new_floor, c1)
                else:
                    new_items[i1] = (g1, new_floor)
                    
                if t2 == 'g':
                    new_items[i2] = (new_floor, c2)
                else:
                    new_items[i2] = (g2, new_floor)
                
                moves.append((new_floor, tuple(new_items)))
        
        return moves
    
    def normalize_state(state):
        """Normalize state to handle equivalent states (pairs are interchangeable)"""
        elevator, items = state
        # Sort pairs by (gen_floor, chip_floor) to treat equivalent states as same
        sorted_items = tuple(sorted(items))
        return (elevator, sorted_items)
    
    # BFS
    initial_normalized = normalize_state(initial_state)
    queue = deque([(initial_normalized, 0)])
    visited = {initial_normalized}
    
    while queue:
        state, steps = queue.popleft()
        
        if is_goal(state):
            return steps
        
        for next_state in get_moves(state):
            normalized = normalize_state(next_state)
            if normalized not in visited and is_valid(next_state):
                visited.add(normalized)
                queue.append((normalized, steps + 1))
    
    return -1

def parse_input(data):
    """Parse the input to extract initial positions of generators and chips"""
    lines = data.strip().split('\n')
    
    # Dictionary to store positions: element -> [generator_floor, chip_floor]
    elements = {}
    
    for floor_num, line in enumerate(lines):
        if 'nothing relevant' in line:
            continue
        
        # Find all generators (element name followed by "generator")
        generator_pattern = r'(\w+) generator'
        for match in re.finditer(generator_pattern, line):
            element = match.group(1)
            if element not in elements:
                elements[element] = [None, None]
            elements[element][0] = floor_num
        
        # Find all microchips (element name followed by "-compatible microchip")
        microchip_pattern = r'(\w+)-compatible microchip'
        for match in re.finditer(microchip_pattern, line):
            element = match.group(1)
            if element not in elements:
                elements[element] = [None, None]
            elements[element][1] = floor_num
    
    # Convert to tuple format (generator_floor, chip_floor)
    items = []
    for element in sorted(elements.keys()):
        gen_floor, chip_floor = elements[element]
        items.append((gen_floor, chip_floor))
    
    return (0, tuple(items))  # Start on floor 0 (elevator on first floor)

# Parse input file to determine generator and chip positions
INPUT_DIR = os.path.expanduser(os.getenv('AOC_INPUT_DIR', '~/.cache/aocb/inputs/'))
data = open(os.path.join(INPUT_DIR, "2016_11.txt")).read()

# Part 1: Parse the actual input
first_state = parse_input(data)
first_solution = solve(first_state)

# Part 2: Add two more element pairs on floor 0
# We need to add elerium and dilithium pairs to the first floor
elevator, items = first_state
items_list = list(items)
# Add two new pairs, both starting on floor 0
items_list.append((0, 0))  # Elerium generator and chip on floor 0
items_list.append((0, 0))  # Dilithium generator and chip on floor 0
second_state = (elevator, tuple(items_list))
second_solution = solve(second_state)

print(first_solution)
print(second_solution)
