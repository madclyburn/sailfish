import argparse
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manimation

def plot_frame(ax, fname):
    chkpt = pickle.load(open(fname, "rb"))
    ax.imshow(
        chkpt["primitive"][:, :, 0].T,
        origin="lower",
        extent=[-0.5, 0.5, -0.5, 0.5],
        vmin=0.4,
        vmax=1.3,
        cmap="plasma",
    )
    print(fname)


parser = argparse.ArgumentParser()
parser.add_argument("filenames", nargs="+")
args = parser.parse_args()


FFMpegWriter = manimation.writers["ffmpeg"]
writer = FFMpegWriter(fps=15)


fig = plt.figure()
ax1 = fig.add_subplot(111)


with writer.saving(fig, "movie.mp4", dpi=200):
    for fname in args.filenames:
        plot_frame(ax1, fname)
        writer.grab_frame()
