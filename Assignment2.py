from copyreg import pickle
import numpy as np
from pickle import load
from matplotlib import pyplot as plt

v = 1.0


def rho_true(x, t):
    return 1.0 + 0.5 * np.sin(2 * np.pi * (x - v * t))


with open("/Users/clyburn/Work/Codes/sailfish/chkpt.final.pk", "rb") as infile:
    chkpt = load(infile)

rho = chkpt["primitive"][:, 0]
t = chkpt["time"]
domain = chkpt["config"]["domain"]
ni = domain["num_zones"][0]
x0 = domain["extent_i"][0]
x1 = domain["extent_i"][1]
dx = (x1 - x0) / ni
x = np.linspace(x0 + 0.5 * dx, x1 - 0.5 * dx, ni)
y = 0
for i in range(np.size(x)):
    y += (rho_true(x[i], t) - rho[i]) ** 2 * dx

L_2 = y ** (1 / 2)

# First Order
L_array1 = [
    0.3259651441998514,
    0.1409299880975562,
    0.07997989554181487,
    0.05586393843012944,
    0.01803895540995553,
    0.009181128135462428,
    0.004633462604548579,
    0.001864039270723246,
    0.001244297905295023,
    0.0009338273401875888,
]

# Second Order
L_array2 = [
    0.14219404058367854,
    0.00854806464459276,
    0.0025003304917292045,
    0.0012060301728924869,
    0.000139598238351513,
    4.112168157165685e-05,
    1.2302860881600903e-05,
    2.541611086385144e-06,
    1.270877568347926e-06,
    7.782594826640115e-07,
]


x_array = [10, 50, 100, 150, 500, 1000, 2000, 5000, 7500, 10000]
delta_x = []
for i in range(np.size(x_array)):
    delta_x.append(1 / x_array[i])

slope1 = (np.log(L_array1[-1]) - np.log(L_array1[1])) / (
    np.log(delta_x[-1]) - np.log(delta_x[1])
)
m_1 = "{:.3}".format(slope1)

slope2 = (np.log(L_array2[-1]) - np.log(L_array2[1])) / (
    np.log(delta_x[-1]) - np.log(delta_x[1])
)
m_2 = "{:.3}".format(slope2)

w = []
for i in range(np.size(delta_x)):
    w.append(
        np.exp(
            slope1 * np.log(delta_x[i])
            + np.log(L_array1[1])
            - slope1 * np.log(delta_x[1])
        )
    )

z = []
for i in range(np.size(delta_x)):
    z.append(
        np.exp(
            slope2 * np.log(delta_x[i])
            + np.log(L_array2[1])
            - slope2 * np.log(delta_x[1])
        )
    )


# plt.scatter(delta_x, L_array1, fc="none", ec="black", label="1st Order")
# plt.plot(delta_x, w, ":", color="black", label=f"m = {m_1}")
# plt.scatter(delta_x, L_array2, fc="black", ec="black", label="2nd Order")
# plt.plot(delta_x, z, "--", color="black", label=f"m = {m_2}")
# plt.xscale("log")
# plt.yscale("log")
# plt.legend()
# plt.xlabel(rf"log($\Delta x$)")
# plt.ylabel(rf"log($L_2$)")

plt.plot(x, rho, label=r"$\rho$", color="black")
plt.plot(x, rho_true(x, t), ":", color="red", label=r"$\rho_{true}$")
plt.grid(True)
plt.ylabel(r"f(x) = 1 +0.5 $\sin(2\pi x)$")
plt.xlabel("x")
plt.legend()
plt.show()
