import time
import os
import datetime
import pandas as pd
import statistics

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotSettings

import logging
import json
import logging.config

from brewingData import *
from displayData import *
import someFuncions as F


"""Display aktualisieren"""
def displayUpdate(a, b, c, d):
    """Draw a black filled box to clear the image."""
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    draw.text((x, top), a, font=font, fill=255)
    draw.text((x, top + 8), b, font=font, fill=255)
    draw.text((x, top + 16), c, font=font, fill=255)
    draw.text((x, top + 25), d, font=font, fill=255)

    """Display image."""
    disp.image(image)
    disp.display()


def getFiles(sdir):
    #check if exist!!!
    csvList = []
    for root, dirs, files in os.walk(DIR):
        for filename in files:
            csvList.append(DIR + '/' + filename)
    return csvList


def getChart(DIR):
    """Plotsettings laden - Farben und co."""
    plotSet = plotSettings.getPlotSetting()
    fig, ax = plt.subplots(1, 1, sharex=True, figsize=(29, 13))

    """Daten einlesen"""
    # Ordner festlegen
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
        # label=csvList[i].split('/')[-1].split('_')[1] + '-1'
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
    plt.savefig(DIR + '/chart.png', dpi=200, bbox_inches='tight')


if brewingDay:
    """working dir"""
    dateString = F.datetimeNowString()
    if not os.path.exists(dateString):
        os.makedirs(dateString)

    """"Letzte Variablen definieren"""
    """
     state:
       -1=aufheizen
        0=einmaischen
        1=1.Rast
        2=2.Rast
        ...
        3=abmaischen
    """
    stateNow = -1
    stateNext = 0

    """Listen für Temperatur und Zeit der beiden Temperatursensoren"""
    temp1 = []
    temp2 = []
    time1 = []
    time2 = []

    timeStart = []
    timeEnd = []
    abmaischen = False

    """MAIN LOOP"""
    while True:

        """Durchschnittliche Temperaturwerte während der aktuellen Rast"""
        temp1_avg = 0
        temp2_avg = 0

        """aktuelle Temperatur"""
        temp1_str = F.readTemperature('28-031643da9eff')
        temp1_float = float(temp1_str)
        temp2_str = F.readTemperature('28-041643e073ff')
        temp2_float = float(temp2_str)

        """Temperaturen in Listen speichern (falls gebraut wird --> brewingDay == True)"""
        if brewingDay and not abmaischen:
            temp1.append(temp1_float)
            time1.append(datetime.datetime.now())
            temp2.append(temp2_float)
            time2.append(datetime.datetime.now())
            temp1_avg = statistics.mean(temp1)
            temp2_avg = statistics.mean(temp2)


        #####################################################
        """Zustandswechsel von -1 (aufheizen) zu stateNext"""
        #####################################################
        if stateNow == -1 and max(temp1_float, temp2_float) >= temp_all[stateNext]:
            """Datem in einem df speichern"""
            df = pd.DataFrame(
                {'temp1': temp1,
                 'time1': time1,
                 'temp2': temp2,
                 'time2': time2
                 })
            timeString = F.datetimeNowString().split('-')[1]
            df.to_csv(dateString + '/' + dateString + '_' + timeString + '_aufheizen.csv')

            """Listen leeren"""
            temp1.clear()
            temp2.clear()
            time1.clear()
            time2.clear()

            """Zustand ändern"""
            stateNow = stateNext

            """timeStart --> Start-Zeitpunkt der Rast"""
            timeStart.append(datetime.datetime.now())
            F.logger.info('Zustandswechsel von aufheizen zu {}'.format(stateNow))

            if stateNow > rastCount:
                abmaischen = True

        if len(timeStart) > 0:
            timeRast_Now = (datetime.datetime.now() - timeStart[stateNow]).seconds
        #####################################################
        """Zustandswechsel von eienr Rast zu aufheizen"""
        #####################################################
        if stateNow >= 0 and timeRast_Now >= time_all[stateNow]:
            """Daten in einem df speichern"""
            df = pd.DataFrame(
                {'temp1': temp1,
                 'time1': time1,
                 'temp2': temp2,
                 'time2': time2
                 })
            if len(df.index) > 1:
                timeString = F.datetimeNowString().split('-')[1]
                df.to_csv(dateString + '/' + dateString + '_' + timeString + '_rast' + str(stateNow) + '.csv')

            """Listen leeren"""
            temp1.clear()
            temp2.clear()
            time1.clear()
            time2.clear()

            if abmaischen:
                """Falls abgemaischt wird muss nicht weiter aufgeheizt werden"""
                getChart(dateString)
                exit('Maischen fettich')
            else:
                F.logger.info('Zustandswechsel von {} zu aufheizen'.format(stateNow))
                stateNext = stateNow + 1
                stateNow = -1
                """timeEnd --> End-Zeitpunkt der Rast"""
                timeEnd.append(datetime.datetime.now())


        """Display aktualisieren"""
        firstLine = '---> PIXELBRAEU <---'
        secondLine = '-->' + str(temp1_str) + ' |' + str(temp2_str) + ' <--'
        if stateNow == -1:
            thridLine = str('Aufheizen bis: {} *C'.format(temp_all[stateNext]))
            fourthLine = '---> PIXELBRAEU <---'
        else:
            thridLine = 'AVG:' + "%.2f" % temp1_avg + ' | ' + "%.2f" % temp2_avg
            fourthLine = str(time_all[stateNow] - (datetime.datetime.now() - timeStart[stateNow]).seconds) + str('s | Ziel: ') + str(temp_all[stateNow]) + '°C'

        displayUpdate(firstLine, secondLine, thridLine, fourthLine)

        time.sleep(2)
else:
    F.logger.info('brewingDay == False --> Nothing to do...')
    """Display aktualisieren"""
    firstLine = '---> PIXELBRAEU <---'
    secondLine = 'no brewing day :('
    thridLine = 'no brewing day :('
    fourthLine = '---> PIXELBRAEU <---'

    displayUpdate(firstLine, secondLine, thridLine, fourthLine)


