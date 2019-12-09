import copy
import itertools
import numpy as np
import sys
from collections import defaultdict

sys.path.append("/Users/jessicawetstone/advent-of-code-2019/")
import test_utils

def read_input(file_name):
    with open(file_name,"r") as f:
        raw_codes = [int(x) for x in f.read().strip().split(",")]
    return raw_codes

class Intcode:
    
    def __init__(self, input_array, codes):
        self.curPosition = 0
        self.current_input = input_array
        self.codes = defaultdict(int)
        self.codes.update({k:v for k,v in zip(range(len(codes)), copy.deepcopy(codes))})
        self.halted = False
        self.relative_base = 0
        
    def _getPosition(self, location, mode):
        if mode == '0':
            return self.codes[location]
        elif mode == '1':
            return location
        elif mode == '2':
            return self.codes[location] + self.relative_base
        
    def stepForward(self, new_input=None):
        
        if self.halted:
            return self.current_input, None
        
        if new_input:
            self.current_input = new_input
        
        curOpcodeStr = str(self.codes[self.curPosition])
        
        ## Test the length of the opcode
        ## If greater then 1, then we are in the more complicated mode
        if len(curOpcodeStr) > 1:
            curOpcode = int(curOpcodeStr[-2:])
            programModes = curOpcodeStr[-3::-1]
        else:
            curOpcode = self.codes[self.curPosition]
            programModes = ''
        
        while len(programModes) < 3:
            programModes += '0'
        
        if curOpcode not in (1,2,3,4,5,6,7,8,9):
            self.halted = True
            return self.current_input, None
        
        if curOpcode in (1,2,7,8):
            program_len = 4
        elif curOpcode in (3,4,9):
            program_len = 2
        else:
            program_len = 3
        
        curPositionUpdated = False
        
        input_1 = self.codes[self._getPosition(self.curPosition + 1, programModes[0])]

        if program_len > 2:
            input_2 = self.codes[self._getPosition(self.curPosition + 2, programModes[1])]
            
        if curOpcode in (1,2,7,8):
            if curOpcode == 1:
                val = input_1 + input_2
            elif curOpcode == 2:
                val = input_1 * input_2
            elif curOpcode == 7:
                val = 1 if input_1 < input_2 else 0
            elif curOpcode == 8:
                val = 1 if input_1 == input_2 else 0
            self.codes[self._getPosition(self.curPosition + 3, programModes[2])] = val
        
        elif curOpcode == 3:
            self.codes[self._getPosition(self.curPosition + 1, programModes[0])] = self.current_input.pop(0)
        
        elif curOpcode == 4:
            self.curPosition = self.curPosition + program_len 
            return copy.deepcopy(self.current_input), [input_1]
        
        elif curOpcode == 5 and input_1 != 0:
            self.curPosition = input_2
            curPositionUpdated = True
        
        elif curOpcode == 6 and  input_1 == 0:
            self.curPosition = input_2
            curPositionUpdated = True
            
        elif curOpcode == 9:
            self.relative_base = self.relative_base + input_1
        
        if not curPositionUpdated:
            self.curPosition = self.curPosition + program_len 
            
        return self.current_input, None    
    
def run_program(raw_codes, input_val = []):
    IC = Intcode(input_val, raw_codes)
    output_array = None
    final_output = []
    while not IC.halted:
        input_array, output_array = IC.stepForward(output_array)
        if output_array is not None:
            final_output += output_array
    return final_output

## For backwards compatibility testing on day 7
def run_sequence(raw_codes, phase_setting_sequence):
    machines = [Intcode([], raw_codes) for x in phase_setting_sequence]
    
    input_arrays = [[x] for x in phase_setting_sequence]
    
    all_halted = False
    input_arrays[0] += [0]
    current_machine = 0
    idx = 0
    
    while (not all_halted):
        prev_input_array, output_array = machines[current_machine].stepForward(input_arrays[current_machine])
        input_arrays[current_machine] = prev_input_array
        if output_array:
            current_machine = (current_machine + 1) % 5
            input_arrays[current_machine] += output_array
        elif machines[current_machine].halted:
            current_machine = (current_machine + 1) % 5
        all_halted = np.all([machine.halted for machine in machines])
    
    output = input_arrays[0][0]
    return output

test_utils.run_tests_for_part("day 7 - 1", [
    ([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], 43210, {'phase_setting_sequence': [4,3,2,1,0]}),
    ([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], 54321, {'phase_setting_sequence': [0,1,2,3,4]}),
    ([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], 65210, {'phase_setting_sequence': [1,0,4,3,2]}),
], run_sequence)

test_utils.run_tests_for_part("day 7 - 2", [
    ([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], 139629729, {'phase_setting_sequence': [9,8,7,6,5]}),
    ([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
    -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
    53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], 18216, {'phase_setting_sequence': [9,7,8,5,6]}),
], run_sequence)

test_utils.run_tests_for_part("day 9 - 1", [
   ([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99],[109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]),
   ([104,1125899906842624,99], [1125899906842624])
], run_program)

print(f"Part 1 answer: {run_program(read_input('/Users/jessicawetstone/advent-of-code-2019/9/input.txt'),[1])}")
print(f"Part 2 answer: {run_program(read_input('/Users/jessicawetstone/advent-of-code-2019/9/input.txt'),[2])}")