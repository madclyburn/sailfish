import argparse
from copyreg import pickle
import numpy as np 
from pickle import load
from matplotlib import pyplot as plt
from statistics import mean

shock_pos = []
time=[]

def checkpoint_reader():
    """
    This function returns a list of dictionaries from the read checkpoints.
    :return: [{}, {}, ...]
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="+")
    args = parser.parse_args()

    raw_data = []

    for filename in args.filenames:
        chkpt = load(open(filename, "rb"))
        raw_data.append(chkpt)

    return raw_data


for item in checkpoint_reader():

    rho = item["primitive"][:,0]
    pre = item["primitive"][:,2]
    t = item["time"]
    domain = item["config"]["domain"]
    ni = domain["num_zones"][0]
    x0 = domain["extent_i"][0]
    x1 = domain["extent_i"][1]
    dx = (x1 - x0) / ni
    x = np.linspace(x0 + 0.5 * dx, x1 - 0.5 * dx, ni)
    
    j=1
    while True:
        if pre[-1] != pre[-1-j]:
            shock_pos.append(x[-1-j])
            time.append(t)
            break
        else:
            j+=1

shock_speed_list = []
for i in range(np.size(shock_pos)-1):
    shock_speed_list.append((shock_pos[i+1]-shock_pos[i])/(time[i+1]-time[i]))

shock_speed = mean(shock_speed_list)

y=[]
for i in range(np.size(time)):
    y.append(shock_speed*time[i]+0.501)

shock_speed = "{:.3}".format(shock_speed)

plt.scatter(time, shock_pos)
plt.plot(time,y, linestyle = ":", color='r', label = f"Shock Speed = {shock_speed} units/s")
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Shock Position")
plt.show()


