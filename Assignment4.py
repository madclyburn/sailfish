import argparse as argp
import json
import numpy as np
import glob
from os import system
from matplotlib import pyplot as plt
from pickle import load


parser = argp.ArgumentParser()
parser.add_argument("iterations", nargs=1)
parser.add_argument("m_i", nargs=1)
parser.add_argument("m_f", nargs=1)
args = parser.parse_args()

m_i = float(args.m_i.pop())
m_f = float(args.m_f.pop())
iterations = int(args.iterations.pop())
it_range = np.linspace(start=m_i, stop=m_f, num=iterations)

list_of_dicts = []
for i in it_range:
    job_dict = {
        "initial_data.model": "kelvin-helmholtz",
        "initial_data.mach_number": round(i, 2),
        "domain.num_zones": [256, 256, 1],
        "domain.extent_i": [-0.5, 0.5],
        "domain.extent_j": [-0.5, 0.5],
        "driver.tfinal": 5.0,
        "driver.checkpoint.cadence": 0.01,
        "driver.report.cadence": 50,
        "scheme.reconstruction": ["plm", 1.5],
        "scheme.time_integration": "rk3",
        "strategy.hardware": "gpu",
        "strategy.cache_flux": True,
        "boundary_condition": {
            "lower_i": "periodic",
            "lower_j": "periodic",
            "upper_i": "periodic",
            "upper_j": "periodic",
        }
    }
    list_of_dicts.append(job_dict)

i = 0
for j in it_range:
    with open(str(round(j, 2))+".json", "w") as outfile:
        json.dump(list_of_dicts[i], indent=4, fp=outfile)
    i += 1

path = "/Users/clyburn/Work/Codes/sailfish_v06beta/sailfish/*.pk"
inst = dict()
for k in it_range:
    system('./bin/sailfish run ' + str(round(k, 2)) + '.json')
    system('rm -f chkpt.final.pk')
    data_arr = [[], []]
    for filename in glob.glob(path):
        with open(filename, 'rb') as f:
            chkpt = load(f)
            data_arr[0].append(chkpt["time"])
            vy = chkpt["primitive"][:,2]
            vy2 = np.square(np.abs(v))
            avg_vy = np.average(vy2)
            data_arr[1].append(avg_vy)
            inst[str(round(k, 2))] = data_arr
        
with open('instability.pk', 'wb') as pkfile:
    pickle.dump(inst, pkfile)

"""
with open('instability.pk', 'rb') as pkfile:
    list_of_vel = load(pkfile)
for m in it_range:
    m_data = list_of_vel[m]
    vy2 = []
    time = []
    for i in range(50):
        vy2.append(np.log(m_data[i][1]))
        time.append(m_data[i][0])
    j=1
    while True:
        if vy2[-1] - vy2[-1-j] > 10:
            if vy2[j+1] - vy2[j] > 10:
                slope = (vy2[-1-j]-vy2[j+1])/(time[-1-j]-time[j+1])
                break
            else:
                break
        else:
            j+=1
    print(slope)
    """

