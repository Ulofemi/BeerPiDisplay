# display libraries
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import someFuncions as F

"""Raspberry Pi pin configuration:"""
RST = None  # on the PiOLED this pin isnt used
"""Note the following are only used with SPI:"""
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

"""128x32 display with hardware I2C:"""
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

"""Initialize library."""
disp.begin()

"""Clear display."""
disp.clear()
disp.display()

"""Create blank image for drawing."""
"""Make sure to create image with mode '1' for 1-bit color."""
width = disp.width
F.logger.info('width: {}'.format(width))
height = disp.height
F.logger.info('height: {}'.format(height))
image = Image.new('1', (width, height))

"""Get drawing object to draw on image."""
draw = ImageDraw.Draw(image)

"""Draw a black filled box to clear the image."""
draw.rectangle((0, 0, width, height), outline=0, fill=0)

"""Draw some shapes."""
"""First define some constants to allow easy resizing of shapes."""
padding = -2
top = padding
bottom = height - padding
"""Move left to right keeping track of the current x position for drawing shapes."""
x = 0

"""Load default font."""
font = ImageFont.load_default()
"""
Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('Minecraftia.ttf', 8)
"""
#font = ImageFont.truetype(DIR + '04B30.TTF', 8)
