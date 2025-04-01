"""
Optimizes a specific set of policy choices in order to achieve sustainable development.
"""

import numpy as np
import itertools
import json

from pyworld3.pyworld3 import World3


def grid_search():
    modified_json_path = "modified_functions_table_world3.json"
    
    parameters_ranges = [
        np.arange(1, 3, 1), # pyear, when we implement the 1-2 policies
        np.arange(1, 3, 1), # imti
        np.arange(1, 2, 1), # iopcd
        np.arange(1, 2, 1), # alai_2
        np.arange(1, 2, 1), # fsafc scaling factor
        np.arange(1, 2, 1), # hsapc scaling factor
    ]

    fsafc_default_values = np.array([0, 0.005, 0.015, 0.025, 0.03, 0.035], dtype=int)
    hsapc_default_values = np.array([0, 20, 50, 95, 140, 175, 200, 220, 230], dtype=int)

    best_param_set = None
    best_metric = -np.inf

    for param_set in itertools.product(*parameters_ranges):
        print(f"param_set={param_set}")

        # open the file
        with open(modified_json_path, 'r') as file:
            # Edit the contents of the file object
            data = json.load(file)
            data[16]["y.values"] = (fsafc_default_values * param_set[4]).tolist()
            data[5]["y.values"] = (hsapc_default_values * param_set[5]).tolist() # access the data using the keys within the json file
            new_data = json.dumps(data)
        # write the file
        with open(modified_json_path, 'w') as file:
            file.write(new_data)

        
        # define a world simulation with this parameter_set
        world3 = World3(pyear=param_set[0])                    # choose the time limits and step.
        world3.init_world3_constants(imti=param_set[1], iopcd=param_set[2], alai2=param_set[3])       # choose the model constants.
        world3.init_world3_variables()       # initialize all variables.
        world3.set_world3_table_functions(modified_json_path)  # get tables from a json file.
        world3.set_world3_delay_functions()  # initialize delay functions.

        # run the simulation
        world3.run_world3()

        # evaluate the run according to our notion of sustainable development
        eval_metric = world3.pop[-1] # TODO: Replace with actual metric
        
        if eval_metric > best_metric:
            best_param_set = param_set
            best_metric = eval_metric

    # report results (plot, table, ...)
    print(f"Best metric: {best_metric}.\nBest param_set: {best_param_set}\n")

grid_search()