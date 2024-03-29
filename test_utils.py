import numpy as np

def test_case(t_input, t_output, function_to_test, additional_args):
    try:
        out = function_to_test(t_input, **additional_args)
        if np.all(out == t_output):
            print(f"Test on input {t_input}: Pass")
        else:
            print(f"Test on input {t_input}: Fail. Expected {t_output} but received {out}")
    except:
        print(f"Test on input {t_input}: Fail with error")
        raise
        
def run_tests_for_part(part, test_cases, function_to_test):
    print("")
    print(f"Running tests for part {part}")
    print("------------------------------")
    for test in test_cases:
        additional_args = {} if len(test) == 2 else test[2]
        test_case(test[0], test[1], function_to_test, additional_args)
    print("------------------------------")
    print("")