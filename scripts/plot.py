#!/usr/bin/env python3

import argparse
import pickle
import sys

sys.path.insert(1, ".")


def main(args):
    import matplotlib.pyplot as plt
    import sailfish

    fig, ax1 = plt.subplots()

    for checkpoint in args.checkpoints:
        with open(checkpoint, "rb") as f:
            chkpt = pickle.load(f)

        mesh = chkpt["mesh"]
        x = mesh.zone_centers(chkpt["time"])
        rho = chkpt["primitive"][:, 0]
        # vel = chkpt["primitive"][:, 1]
        # pre = chkpt["primitive"][:, 2]
        ax1.plot(x, rho, label=r"$\rho$")
        # ax1.plot(x, vel, label=r"$\Gamma \beta$")
        # ax1.plot(x, pre, label=r"$p$")

    if type(mesh) == sailfish.mesh.LogSphericalMesh:
        ax1.set_xscale("log")
        ax1.set_yscale("log")

    ax1.legend()
    plt.show()


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("checkpoints", type=str, nargs="+")
    main(args.parse_args())