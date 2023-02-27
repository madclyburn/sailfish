import argparse
from copyreg import pickle
import numpy as np 
from pickle import load
from matplotlib import pyplot as plt
from statistics import mean

with open("/Users/Madeline/Documents/Sailfish_Beta/sailfish/chkpt.0001.pk", "rb") as infile:
    chkpt = load(infile)

rho = chkpt["primitive"][:,0]
pre = chkpt["primitive"][:,2]
domain = chkpt["config"]["domain"]
ni = domain["num_zones"][0]
x0 = domain["extent_i"][0]
x1 = domain["extent_i"][1]
dx = (x1 - x0) / ni
x = np.linspace(x0 + 0.5 * dx, x1 - 0.5 * dx, ni)
plt.plot(x, rho, label=r"$\rho$")
plt.plot(x, pre, label=r"$p$")
plt.legend()
plt.show()