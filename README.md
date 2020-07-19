# BeerPiDisplay
## Die Idee
* Temperaturüberwachung während des Maischeprozesses
* Zeitmanagement während der Rasten
* Graphen erstellen nach Abmaischen

## Die Umsetzung
* Raspberry Pi 3
* OLED Display I2C
* Temperatursensoren ds18b20 
* Python3

## Das Prozedere
* In der Datei brewingData.py die Werte anpassen
* main.py ausführen 
* Nach Abschluss des Masichens kann man sich mit plot.py einen Graphen erstellen

## Die Installation
* Im Prinzip reicht es aus das repository zu clonen

## Voraussetzungen
* Der I2C Display sollte angeschlossen richtig angeschlossen sein [-->](https://indibit.de/raspberry-pi-oled-display-128x64-mit-python-ansteuern-i2c/)
 * $ sudo raspi-config
 * $ sudo apt-get install python-smbus i2c-tools git python-pil
 * $ sudo reboot
 * $ i2cdetect -y 1
 
* Die Temperataursensoren sollten angeschlossen sein und funktionieren [-->](https://tutorials-raspberrypi.de/raspberry-pi-temperatur-mittels-sensor-messen/)
 * cd /sys/bus/w1/devices/
* Pandas: sudo apt-get install python3-pandas
