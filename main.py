import time
import os
import datetime
import pandas as pd
import statistics

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

if brewingDay:
    """working dir"""
    dateString = F.datetimeNowString().split('-')[0]
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
                pass
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


