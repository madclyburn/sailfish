import argparse as argp
import json
import numpy as np
from subprocess import Popen
from pickle import load


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
        "domain.num_zones": [1024, 1024, 1],
        "domain.extent_i": [-0.5, 0.5],
        "domain.extent_j": [-0.5, 0.5],
        "driver.tfinal": 5.0,
        "driver.checkpoint.cadence": 0.1,
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

inst = []
for k in it_range:
    Popen('./bin/sailfish run ' + str(round(k, 2)) + '.json',
                 shell=True)
    for item in checkpoint_reader():
        vy = item["primitive"][:,2]
        t = item["time"]
        vy2 = np.square(np.abs(v))
        avg_vy = np.average(vy2)
        inst.append(avg_vy)
    plt.scatter(t, inst)

plot.show()



