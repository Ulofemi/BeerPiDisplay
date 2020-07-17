import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import random as rd

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

def getPlotSetting():
    plotSettings = []
    plotSettings.append(['tab:blue', 'deepskyblue', 'o'])
    plotSettings.append(['tab:red', 'lightcoral', 'H'])
    plotSettings.append(['tab:orange', 'bisque', 's'])
    plotSettings.append(['tab:green', 'lightgreen', '^'])
    plotSettings.append(['tab:purple', 'plum', '*'])
    plotSettings.append(['tab:brown', 'peachpuff', 'X'])
    plotSettings.append(['tab:pink', 'lightpink', 'p'])
    plotSettings.append(['tab:gray', 'lightgray', 'P'])
    plotSettings.append(['tab:olive', 'darkkhaki', 'v'])
    plotSettings.append(['tab:cyan', 'lightcyan', 'd'])
    return plotSettings


