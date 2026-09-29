"""Shared chart styling so every figure in results/ looks consistent."""

import matplotlib.pyplot as plt

# Fixed colour per group: control is always blue, treatment always orange
COLORS = {"gate_30": "#2a78d6", "gate_40": "#eb6834"}
INK = "#0b0b0b"
INK_MUTED = "#52514e"
GRID = "#e4e3df"


def apply_style():
    plt.rcParams.update({
        "figure.dpi": 110,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": INK_MUTED,
        "axes.labelcolor": INK,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "xtick.color": INK_MUTED,
        "ytick.color": INK_MUTED,
        "legend.frameon": False,
    })
