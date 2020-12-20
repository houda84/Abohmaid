import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use("Qt5Agg")

# This example fits a4 paper with 5mm margin printers

# figure settings
figure_width = 28.7  # cm
figure_height = 20     # cm
left_right_margin = 1  # cm
top_bottom_margin = 1  # cm

# Don't change
left = left_right_margin / figure_width     # Percentage from height
bottom = top_bottom_margin / figure_height  # Percentage from height
width = 1 - left*2
height = 1 - bottom*2
cm2inch = 1/2.54  # inch per cm

# specifying the width and the height of the box in inches
fig = plt.figure(figsize=(figure_width*cm2inch, figure_height*cm2inch))
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
ax.plot([1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 17])

# save figure ( printing png file had better resolution, pdf was lighter and better on screen)
plt.show()
fig.savefig('A4_grid_cm.png', dpi=1000)
fig.savefig('tA4_grid_cm.pdf')

# def plotter_plot_A4_q1(fig=fig, ax=ax, plotx, ploty):
#
#     # figure settings
#     figure_width = 28.7  # cm
#     figure_height = 20  # cm
#     left_right_margin = 1  # cm
#     top_bottom_margin = 1  # cm
#
#     # Don't change
#     left = left_right_margin / figure_width  # Percentage from height
#     bottom = top_bottom_margin / figure_height  # Percentage from height
#     width = 1 - left * 2
#     height = 1 - bottom * 2
#     cm2inch = 1 / 2.54  # inch per cm
#
#     # specifying the width and the height of the box in inches
#     fig = plt.figure(figsize=(figure_width * cm2inch, figure_height * cm2inch))
#     ax = fig.add_axes((left, bottom, width, height))
#
#     # limits settings (important)
#     plt.xlim(0, figure_width * width)
#     plt.ylim(0, figure_height * height)
#
#     # Ticks settings
#     ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(5))
#     ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
#     ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(5))
#     ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
#
#     # Grid settings
#     ax.grid(color="gray", which="both", linestyle=':', linewidth=0.5)
#
#     # your Plot (consider above limits)
#     ax.plot(plotx, ploty)
#
#     # save figure ( printing png file had better resolution, pdf was lighter and better on screen)
#     plt.show()
#     fig.savefig('A4_grid_cm.png', dpi=1000)
#     fig.savefig('tA4_grid_cm.pdf')
