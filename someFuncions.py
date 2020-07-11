import datetime
import os

import logging
import json
import logging.config

from brewingData import DIR

def datetimeNowString():
    now = datetime.datetime.now()
    y = now.year
    mo = now.month
    d = now.day
    h = now.hour
    mi = now.minute
    s = now.second

    y_str = str(y)

    if mo < 10:
        mo_str = '0' + str(mo)
    else:
        mo_str = str(mo)

    if d < 10:
        d_str = '0' + str(d)
    else:
        d_str = str(d)

    if h < 10:
        h_str = '0' + str(h)
    else:
        h_str = str(h)

    if mi < 10:
        mi_str = '0' + str(mi)
    else:
        mi_str = str(mi)

    if s < 10:
        s_str = '0' + str(s)
    else:
        s_str = str(s)

    now_str = y_str + mo_str + d_str + '-' + h_str + mi_str + s_str
    return now_str


def setup_logging(
        default_path=DIR + 'logging.json',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

setup_logging()
logger = logging.getLogger(__name__)
logger.info('Start Yo!')


"""readTemperature takes the ID of a DSds18b20"""
def readTemperature(x):
    """1-wire Slave Datei lesen"""
    file = open('/sys/bus/w1/devices/' + x + '/w1_slave')
    filecontent = file.read()
    file.close()

    """Temperaturwerte auslesen und konvertieren"""
    stringvalue = filecontent.split("\n")[1].split(" ")[9]
    temperature = float(stringvalue[2:]) / 1000

    """Temperatur ausgeben"""
    rueckgabewert = '%6.2f' % temperature
    return (rueckgabewert)

