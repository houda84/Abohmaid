import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('macosx')
import numpy as np

plt.ion

def reader_csv_gh_points(filepath="filepath"):
    # Read curve points from  grasshopper
    gh_points_csv = np.loadtxt(fname=filepath)
    # Parse data for x and y values
    x_curve_gh = gh_points_csv[0::3]
    y_curve_gh = gh_points_csv[1::3]
    return x_curve_gh, y_curve_gh


def plotter_plot_a4_q1(fig, ax, plotx, ploty, plot_label="example"):
    # figure settings
    figure_width = 28.7  # cm
    figure_height = 20  # cm
    left_right_margin = 1  # cm
    top_bottom_margin = 1  # cm

    # Don't change
    left = left_right_margin / figure_width  # Percentage from height
    bottom = top_bottom_margin / figure_height  # Percentage from height
    width = 1 - left * 2
    height = 1 - bottom * 2
    cm2inch = 1 / 2.54  # inch per cm

    # specifying the width and the height of the box in inches
    fig = plt.figure(figsize=(figure_width * cm2inch, figure_height * cm2inch))
    ax = fig.add_axes((left, bottom, width, height))

    # limits settings (important)
    plt.xlim(0, figure_width * width)
    plt.ylim(0, figure_height * height)

    # Ticks settings
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(5))
    ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(5))
    ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))

    # Grid settings
    ax.grid(color="gray", which="both", linestyle=':', linewidth=0.5)

    # your Plot (consider above limits)
    ax.plot(plotx, ploty, label=plot_label)
    ax.legend()

    # save figure ( printing png file had better resolution, pdf was lighter and better on screen)
    plt.show()
    fig.savefig(f'{plot_label}.png', dpi=1000)
    fig.savefig(f'{plot_label}.pdf')

    return fig, ax


def plotter_plot_a4_q1_q2(fig, ax, plotx, ploty, plot_label="example"):
    # figure settings
    figure_width = 28.7  # cm
    figure_height = 20  # cm
    left_right_margin = 1  # cm
    top_bottom_margin = 1  # cm

    # Don't change
    left = left_right_margin / figure_width  # Percentage from height
    bottom = top_bottom_margin / figure_height  # Percentage from height
    width = 1 - left * 2
    height = 1 - bottom * 2
    cm2inch = 1 / 2.54  # inch per cm

    # specifying the width and the height of the box in inches
    fig = plt.figure(figsize=(figure_width * cm2inch, figure_height * cm2inch))
    ax = fig.add_axes((left, bottom, width, height))

    # limits settings (important)
    plt.xlim((figure_width * width) / 2 * -1, (figure_width * width) / 2)
    plt.ylim(0, figure_height * height)

    # Ticks settings
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(5))
    ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(5))
    ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))

    # Grid settings
    ax.grid(color="gray", which="both", linestyle=':', linewidth=0.5)

    # your Plot (consider above limits)
    ax.plot(plotx, ploty, label=plot_label)
    ax.legend()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('center')

    # save figure ( printing png file had better resolution, pdf was lighter and better on screen)
    plt.show()
    fig.savefig(f'{plot_label}.png', dpi=1000)
    fig.savefig(f'{plot_label}.pdf')

    return fig, ax


def plotter_plot_a4_q1_to_q4(fig, ax, plotx, ploty, plot_label="example"):
    # figure settings
    figure_width = 28.7  # cm
    figure_height = 20  # cm
    left_right_margin = 1  # cm
    top_bottom_margin = 1  # cm

    # Don't change
    left = left_right_margin / figure_width  # Percentage from height
    bottom = top_bottom_margin / figure_height  # Percentage from height
    width = 1 - left * 2
    height = 1 - bottom * 2
    cm2inch = 1 / 2.54  # inch per cm

    # specifying the width and the height of the box in inches
    fig = plt.figure(figsize=(figure_width * cm2inch, figure_height * cm2inch))
    ax = fig.add_axes((left, bottom, width, height))

    # limits settings (important)
    plt.xlim((figure_width * width) / -2, (figure_width * width) / 2)
    plt.ylim((figure_height * height) / -2, (figure_height * height) / 2)

    # Ticks settings
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(5))
    ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(5))
    ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))

    # Grid settings
    ax.grid(color="gray", which="both", linestyle=':', linewidth=0.5)

    # your Plot (consider above limits)
    ax.plot(plotx, ploty, label=plot_label)
    ax.legend()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position('center')
    ax.spines['left'].set_position('center')

    # save figure ( printing png file had better resolution, pdf was lighter and better on screen)
    plt.show()
    fig.savefig(f'{plot_label}.png', dpi=1000)
    fig.savefig(f'{plot_label}.pdf')

    return fig, ax


x_half_circle, y_half_circle = reader_csv_gh_points("Test_examples/csv/Half_circle.csv")
plotter_plot_a4_q1_q2("fig_half_circle", "ax_half_circle", x_half_circle, y_half_circle, "Half_circle")

x_reverse_curve, y_reverse_curve = reader_csv_gh_points("Test_examples/csv/Reverse_curve.csv")
plotter_plot_a4_q1_to_q4("fig_reverse_curve", "ax_reverse_curve", x_reverse_curve, y_reverse_curve, "Reverse_curve")

x_saddle_curve, y_saddle_curve = reader_csv_gh_points("Test_examples/csv/Saddle_curve.csv")
plotter_plot_a4_q1_q2("fig_saddle_curve", "ax_saddle_curve", x_saddle_curve, y_saddle_curve, "Saddle_curve")

x_introp, y_introp = reader_csv_gh_points("Test_examples/csv/Interpolation_test.csv")
plotter_plot_a4_q1_q2("fig_introp", "ax_introp", x_introp, y_introp, "Interpolation_test")
