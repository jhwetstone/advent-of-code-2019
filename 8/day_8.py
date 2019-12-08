import copy
import imageio
import numpy as np
import sys

sys.path.append("/Users/jessicawetstone/advent-of-code-2019/")
import test_utils

def read_input(file_name):
    with open(file_name,"r") as f:
        raw_sequence = [int(x) for x in f.read().strip()]
    return raw_sequence

def load_image(input_file, width, length):
    raw_sequence = read_input(input_file)
    image = np.array(raw_sequence).reshape(-1,length,width)
    return image

image = load_image("8/input.txt",25,6)

min_num_zeros = np.inf
result = None
for layer_idx in range(image.shape[0]):
    layer = image[layer_idx,:,:]
    if np.sum(layer == 0) < min_num_zeros:
        min_num_zeros = np.sum(layer == 0)
        result = np.sum(layer == 1) * np.sum(layer == 2)
        
test_utils.run_tests_for_part(1, [
    ("8/test.txt", np.array([[[1,2,3],[4,5,6]],[[7,8,9],[0,1,2]]]), {'width': 3, 'length': 2}),
], load_image)
    
print(f"Part 1 answer: {result}")

def flatten_image(image):
    final_image = image[0,:,:]
    for layer_idx in range(1,image.shape[0]):
        unfrozen_x, unfrozen_y = np.where(final_image > 1)
        final_image[unfrozen_x, unfrozen_y] = image[layer_idx, unfrozen_x, unfrozen_y]
    return final_image

test_utils.run_tests_for_part(2, [
    (load_image("8/test_2.txt",2,2), np.array([[0,1],[1,0]])),
], flatten_image)

imageio.imwrite('8/out.jpg',flatten_image(image))

print(f"Part 2 answer: see out.jpg")
    