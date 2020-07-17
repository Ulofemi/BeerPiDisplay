import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotSettings
import datetime
import os



def getFiles(sdir):
    #check if exist!!!
    csvList = []
    for root, dirs, files in os.walk(DIR):
        for filename in files:
            csvList.append(DIR + '/' + filename)
    return csvList

"""Plotsettings laden - Farben und co."""
plotSet = plotSettings.getPlotSetting()
fig, ax = plt.subplots(1, 1, sharex=True, figsize=(29, 13))

"""Daten einlesen"""
# Ordner festlegen
DIR = '20200711'
csvList = getFiles(DIR)

"""Listen für Temperatur und Zeit"""
temp1_list = []
time1_list = []
temp2_list = []
time2_list = []

"""Ordner csvList durcharbeiten"""
for csv in csvList:
    df = pd.read_csv(csv)
    df['time1'] = pd.to_datetime(df['time1'])
    df['time2'] = pd.to_datetime(df['time2'])

    # In x_dt64 sind die Datetimes als Datetime64, in x_dt werden sie als datetime gespeichert
    x_dt1_64 = df['time1'].values
    x_dt2_64 = df['time2'].values
    x_dt1 = []
    x_dt2 = []
    for i in range(len(x_dt1_64)):
        x_dt1.append(datetime.datetime.utcfromtimestamp(x_dt1_64[i].tolist() / 1e9))
        x_dt2.append(datetime.datetime.utcfromtimestamp(x_dt2_64[i].tolist() / 1e9))

    temp1 = df['temp1'].values
    temp2 = df['temp2'].values

    temp1_list.append(temp1)
    temp2_list.append(temp2)
    time1_list.append(x_dt1_64)
    time2_list.append(x_dt2_64)

"""Plotten"""
fs = 28

for i in range(len(temp1_list)):
    #label=csvList[i].split('/')[-1].split('_')[1] + '-1'
    ax.plot(time1_list[i], temp1_list[i], color=plotSet[i][0], marker='o', linestyle=':')
    ax.plot(time2_list[i], temp2_list[i], color=plotSet[i][1], marker='o', linestyle=':')


# Format der Zeitstempel
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# achsen Beschriftungen
ax.set_title('Kölsch', fontsize=fs)
ax.set_ylabel('Temperatur [°C]', fontsize=fs)
ax.set_xlabel('Zeit [HH:MM]', fontsize=fs)

ax.axes.tick_params(axis='both', labelsize=fs)
ax.grid(linestyle=':', zorder=0)
plt.savefig(DIR + '.png', dpi=200, bbox_inches='tight')