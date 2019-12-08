import copy
import itertools
import numpy as np
import sys

sys.path.append("/Users/jessicawetstone/advent-of-code-2019/")
import test_utils

def read_input(file_name):
    with open(file_name,"r") as f:
        raw_codes = [int(x) for x in f.read().strip().split(",")]
    return raw_codes

raw_codes = read_input("7/input.txt")

def run_sequence(raw_codes, phase_setting_sequence):
    input_arrays = [[x] for x in phase_setting_sequence]
    curPositions = [0 for x in phase_setting_sequence]
    codes = [copy.deepcopy(raw_codes) for x in phase_setting_sequence]
    
    halt = False
    input_arrays[0] += [0]
    current_machine = 0
    idx = 0
    
    while (not halt):
        # print(f"Running codes on {current_machine} with input array {input_arrays[current_machine]}")
        phase_set = phase_setting_sequence[current_machine]
        input_array, curPosition, curCodes, halt = IntCode(input_arrays[current_machine], curPositions[current_machine], codes[current_machine])
        curPositions[current_machine] = curPosition
        codes[current_machine] = curCodes
        current_machine = (current_machine + 1) % 5
        input_arrays[current_machine] += input_array
        idx = idx + 1
    
    output = input_array[0]
    return output

def IntCode(input_array, curPosition, codes):
    while curPosition < len(codes):
        curOpcodeStr = str(codes[curPosition])

        ## Test the length of the opcode
        ## If greater then 1, then we are in the more complicated mode
        if len(curOpcodeStr) > 1:
            curOpcode = int(curOpcodeStr[-2:])
            programModes = curOpcodeStr[-3::-1]
        else:
            curOpcode = codes[curPosition]
            programModes = ''
        
        while len(programModes) < 2:
            programModes += '0'
        
        if curOpcode not in (1,2,3,4,5,6,7,8):
            # print("Halted")
            return input_array, curPosition, codes, True
        
        if curOpcode in (1,2,7,8):
            program_len = 4
        elif curOpcode in (3,4):
            program_len = 2
        else:
            program_len = 3
        
        curPositionUpdated = False
        
        input_1 = codes[codes[curPosition + 1]] if programModes[0] == '0' else codes[curPosition + 1]
        
        if program_len > 2:
            input_2 = codes[codes[curPosition + 2]] if programModes[1] == '0' else codes[curPosition + 2]
            
        if curOpcode in (1,2,7,8):
            if curOpcode == 1:
                val = input_1 + input_2
            elif curOpcode == 2:
                val = input_1 * input_2
            elif curOpcode == 7:
                val = 1 if input_1 < input_2 else 0
            elif curOpcode == 8:
                val = 1 if input_1 == input_2 else 0
            codes[codes[curPosition + 3]] = val
            #print(f"Storing {val} at position {codes[curPosition + 3]}")
        
        elif curOpcode == 3:
            codes[codes[curPosition + 1]] = input_array.pop(0)
        
        elif curOpcode == 4:
            curPosition = curPosition + program_len 
            # print("Output")
            return [input_1], curPosition, codes, False
        
        elif curOpcode == 5 and input_1 != 0:
            curPosition = input_2
            curPositionUpdated = True
        
        elif curOpcode == 6 and  input_1 == 0:
            curPosition = input_2
            curPositionUpdated = True
        
        if not curPositionUpdated:
            curPosition = curPosition + program_len    
            
def get_max_sequence(raw_codes, phase_settings):
    max_output = - np.inf
    max_perm = None
    for phase_setting_sequence in itertools.permutations(phase_settings):
        output = run_sequence(raw_codes, phase_setting_sequence)
        if output > max_output:
            max_output = output
            max_perm = phase_setting_sequence

    return max_output

test_utils.run_tests_for_part(1, [
    ([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], 43210, {'phase_setting_sequence': [4,3,2,1,0]}),
    ([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], 54321, {'phase_setting_sequence': [0,1,2,3,4]}),
    ([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], 65210, {'phase_setting_sequence': [1,0,4,3,2]}),
], run_sequence)

print(f"Part 1 answer: {get_max_sequence(read_input('7/input.txt'), range(0,5))}")

test_utils.run_tests_for_part(2, [
    ([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], 139629729, {'phase_setting_sequence': [9,8,7,6,5]}),
    ([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
    -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
    53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], 18216, {'phase_setting_sequence': [9,7,8,5,6]}),
], run_sequence)

print(f"Part 2 answer: {get_max_sequence(read_input('7/input.txt'), range(5,10))}")