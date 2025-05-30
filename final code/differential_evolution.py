import numpy as np
from scipy.optimize import differential_evolution
from pyworld3 import World3
import json
from grid_search import plot_world_3

# === Sigmoid Function ===
# This is a scaled logistic function to map inputs to values between 0 and 1.
# Useful for smoothly evaluating how close a metric is to a desired target.
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# === Evaluation Function ===
# Computes a custom "quality of life" metric (QL) based on model outputs.
# Each component is mapped to a normalized factor (0 to 1) via a sigmoid function.
def evaluation_function(world3):
    # Extract key outputs from the simulation
    population = np.mean(world3.pop)
    nrfr_final = world3.nrfr[-1]  # Non-renewable resource fraction at final year
    iopc = np.mean(world3.iopc)   # Industrial output per capita
    ppolx = np.mean(world3.ppolx) # Persistent pollution index
    fpc = np.mean(world3.fpc)     # Food per capita

    # Calculate normalized population factor (closer to desired is better)
    desired_population = 2e9
    pop_std = 2e8  # standard deviation for smoothness
    pop_factor = sigmoid((population - desired_population) / pop_std)

    # Use final non-renewable resource fraction directly (higher = better)
    nrfr_factor = nrfr_final

    # Normalize IOPC (more is better)
    desired_iopc = 400
    iopc_std = 50
    iopc_factor = sigmoid((iopc - desired_iopc) / iopc_std)

    # Normalize pollution (less is better, so subtract sigmoid from 1)
    desired_ppolx = 0.5
    ppolx_std = 0.2
    ppolx_factor = 1 - sigmoid((ppolx - desired_ppolx) / ppolx_std)

    # Normalize food per capita (more is better)
    desired_fpc = world3.sfpc * 1.5
    fpc_std = world3.sfpc / 8
    fpc_factor = sigmoid((fpc - desired_fpc) / fpc_std)

    # Combine all components using geometric mean (balanced importance)
    ql = pop_factor * nrfr_factor * iopc_factor * ppolx_factor * fpc_factor
    return ql**(1/5)

# === Simulation Wrapper ===
# Runs a single World3 simulation given a parameter vector `x`.
# Applies changes to the table function JSON before running.
def simulate_world3_with_constants(x):
    # Unpack optimization parameters
    pyear = x[0]    # Initial year of the simulation
    ppgf2 = x[1]    # ppgf - pollution generation factor (discrete steps)
    alai2 = x[2]    # alai2 - average life agricultural input multiplier
    hsid = x[3]     # hsid - health service impact delay (in years)
    imti = x[4]     # imti - industrial material toxicity index (note order descending)
    dcfs = x[5]     # dcfs - desired number of children (discrete options)


    # Instantiate and configure the World3 model with the modified parameters
    world3 = World3(pyear=pyear)
    world3.init_world3_constants(ppgf2=ppgf2, alai2=alai2, hsid=hsid, imti=imti, dcfsn=dcfs)
    world3.init_world3_variables()
    world3.set_world3_table_functions()
    world3.set_world3_delay_functions()

    # Run the simulation
    world3.run_world3()
    return world3

# === Objective Function ===
# This is the function that differential evolution tries to minimize.
# Since we want to *maximize* the evaluation metric, we return its negative.
def obj(x):
    try:
        world3 = simulate_world3_with_constants(x)
        return -evaluation_function(world3)  # negative for maximization
    except Exception as e:
        # Print any error and return a large penalty to steer the search away
        print(f"Error with parameters {x}: {e}")
        return 1e6

# === Callback Function ===
# Called after every iteration of the optimizer to monitor progress.
iteration = 0
def callback_func(xk, convergence):
    global iteration
    iteration += 1
    current_score = -obj(xk)  # Convert back to original (non-negative) score
    print(f"Iteration {iteration}: Current best evaluation metric = {current_score:.5f}")

# === Parameter Bounds ===
# Each tuple defines the lower and upper bounds for each parameter being optimized
# bounds = [
#     (0.25, 4),      # hsapc-multiplier (fertility effectiveness time)
#     (0.5, 8),       # fsafc-multiplier (land development delay)
#     (100, 800),     # iopcd (persistent materials use)
#     (2, 20),        # imti (social adjustment delay)
#     (0.5, 4),       # alai2 (pollution generation factor)
#     (1970, 2050)    # pyear (policy year)
# ]

# # === Run Differential Evolution Optimization ===
# # Optimizes the parameters to maximize the quality of life score
# result = differential_evolution(
#     obj,                    # Objective function
#     bounds,                 # Parameter bounds
#     strategy='best1bin',    # DE strategy
#     maxiter=20,             # Max iterations
#     popsize=5,              # Population size per iteration
#     seed=42,                # Random seed for reproducibility
#     disp=True,              # Display progress in console
#     callback=callback_func  # Log each iteration's result
# )

# # === Output the Results ===
# print("\n=== Optimization Results ===")
# print("Best Score (maximized QL):", -result.fun)
# print("Best Parameters:")

# # Print the best set of parameters found
# param_names = ["pyear", "ppgf2", "alai2", "hsid", "imti", "dcfs"]
# for name, val in zip(param_names, result.x):
#     print(f"  {name}: {val}")
