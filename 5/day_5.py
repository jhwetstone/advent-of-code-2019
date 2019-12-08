import copy
import numpy as np
import sys

sys.path.append("/Users/jessicawetstone/advent-of-code-2019/")
import test_utils

def read_input(file_name):
    with open(file_name,"r") as f:
        raw_codes = [int(x) for x in f.read().strip().split(",")]
    return raw_codes
    
def IntCode(raw_codes, input_param):
    curPosition = 0
    codes = copy.deepcopy(raw_codes)
    
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
            break
        
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
            codes[codes[curPosition + 1]] = input_param
        
        elif curOpcode == 4:
            input_param = input_1
            print("output:", input_param)
        
        elif curOpcode == 5 and input_1 != 0:
            curPosition = input_2
            curPositionUpdated = True
        
        elif curOpcode == 6 and  input_1 == 0:
            curPosition = input_2
            curPositionUpdated = True
        
        if not curPositionUpdated:
            curPosition = curPosition + program_len    
    
    return input_param

print(f"Part 1 answer: {IntCode(read_input('5/input.txt'),1)}")
      
test_utils.run_tests_for_part(2, [
    (read_input("5/test.txt"), 1000, {'input_param': 8}),
    (read_input("5/test.txt"), 999, {'input_param': 6}),
    (read_input("5/test.txt"), 1001, {'input_param': 16})
], IntCode)

print(f"Part 2 answer: {IntCode(read_input('5/input.txt'),5)}")