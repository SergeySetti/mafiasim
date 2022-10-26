from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.pyplot import figure


def set_figure_pixel_size(width=700, height=500, ppi=100, f: Figure = None):
    if f:
        f.set_dpi(ppi)
        return f.set_size_inches(width / float(ppi), height / float(ppi))

    figure(figsize=(width / float(ppi), height / float(ppi)), dpi=ppi)


def set_ax_pixel_size(ax: Axes, width=700, height=500, ppi=100):
    f = ax.figure
    if f:
        f.set_dpi(ppi)
        return f.set_size_inches(width / float(ppi), height / float(ppi))
