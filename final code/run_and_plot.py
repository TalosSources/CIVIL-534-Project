import numpy as np
from pyworld3 import World3
from grid_search import plot_world_3
def simulate_world3(x):
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
    plot_world_3(world3)