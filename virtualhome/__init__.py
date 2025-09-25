import glob
import sys
from sys import platform

# Needs to be fixed!
original_path = sys.path[5]
new_path = original_path + '/virtualhome/simulation'
sys.path.append(new_path)

from virtualhome.simulation.unity_simulator.comm_unity import UnityCommunication
from virtualhome.simulation.unity_simulator import utils_viz