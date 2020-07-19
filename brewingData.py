"""wird gebraut?"""
brewingDay = True

"""Speicherpfad des main Skripts"""
DIR = '/home/pi/BeerPiDisplay/'

"""
Listen für Maischeprozess
Zeit in Minuten
Temp in °C
"""
time_all = []
temp_all = []

"""Einmaischen"""
tempRast_0 = 24
timeRast_0 = 0.5
time_all.append(timeRast_0 * 60)
temp_all.append(tempRast_0)

"""1. Rast"""
tempRast_1 = 25
timeRast_1 = 0.6
time_all.append(timeRast_1 * 60)
temp_all.append(tempRast_1)

"""2. Rast"""
tempRast_2 = 26
timeRast_2 = 0.7
time_all.append(timeRast_2 * 60)
temp_all.append(tempRast_2)

"""3. Rast"""
#tempRast_3 = 27
#timeRast_3 = 0.8
#time_all.append(timeRast_3 * 60)
#temp_all.append(tempRast_3)

"""4. Rast"""
#tempRast_4 = 27
#timeRast_4 = 2
#time_all.append(timeRast_4 * 60)
#temp_all.append(tempRast_4)

"""Abmaischen"""
tempRast_end = 28
timeRast_end = 1
time_all.append(timeRast_end * 60)
temp_all.append(tempRast_end)

"""Anzahl an Rasten --> Einmaischen und Abmaischen ist keine Rast"""
rastCount = len(temp_all) - 2