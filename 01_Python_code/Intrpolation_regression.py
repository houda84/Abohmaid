import json
import matplotlib as mpl
import matplotlib.axes._axes as axes
import matplotlib.figure as figure
import numpy as np
from scipy import linalg as la
from matplotlib import pyplot as plt
mpl.use("qt5agg")


def plotfigsize(figheight, ratio):
    cm2i = 1 / 2.54
    figehightcm = figheight * cm2i
    figwid = figheight * cm2i * ratio
    return figehightcm, figwid


print(plotfigsize(9, 3 / 4))
with open("/Users/khetamdouba/PycharmProjects/Pyserial_test/Read_Files/calibration/Brass 3mm R1.json", "r") as j:
    calib_j = json.load(j)


def parse_json_sub(lodedJsonVar, mv="mainValue", sv="subValue"):
    value = lodedJsonVar[mv]
    lis = []
    for i in value:
        x = dict(i)[sv]
        lis.append(x)
    return lis


calib_angels = np.array(parse_json_sub(calib_j, "PosData", "PinAngle"))[1:]
x_positive = calib_angels - np.array(parse_json_sub(calib_j, "PosData", "SpringBackAngle"))[1:]
x_Negative = calib_angels - np.array(parse_json_sub(calib_j, "NegData", "SpringBackAngle"))[1:]

x = np.linspace(3, 130, 200)
X = calib_angels
Y = x_positive
A = np.vstack([X ** 0, X ** 1, X ** 2, X ** 3])
sol, r, rank, sv = la.lstsq(A.T, Y)
y_fit = sol[0] + sol[1] * x + sol[2] * x ** 2 + sol[3] * x ** 3

print(sol)
print(r)

fig, ax = plt.subplots()  # type:figure.Figure, axes.Axes

# fig, ax = plt.subplots(figsize=plotfigsize(9, 3/4))
ax.plot(calib_angels, x_positive, ls="-", lw=1, color="r", label="Clockwise rotation")
ax.scatter(calib_angels, x_positive, color="r")

ax.plot(x, y_fit, ls=":", lw=1, color="b", label="Counter-clockwise rotation")
# ax.plot(calib_angels, x_Negative, ls="-", lw=1, color="b", label="Counter-clockwise rotation")
# ax.scatter(calib_angels, x_Negative, color="b")
ax.set_xlabel("Calibration angles")
ax.set_ylabel("Springback compensation")
ax.set_xlim(0, 135)
ax.set_ylim(3, 8.25)
ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(.5))
ax.grid(color="gray", which="both", linestyle=':', linewidth=0.5)
ax.set_title("Default manual calibration process")
ax.legend()

fig.savefig('/Users/khetamdouba/desktop/interpolation 1.png', dpi=1000)

# plt.plot(x, y)
plt.show()
