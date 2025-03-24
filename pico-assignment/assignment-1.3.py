import machine
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import utime

# Microbuttons connections to Pico's GPIOs
SW_2 = 7
SW_1 = 8
SW_0 = 9

# Microbuttons
down = Pin(SW_0, Pin.IN, Pin.PULL_UP)
reset = Pin(SW_1, Pin.IN, Pin.PULL_UP)
up = Pin(SW_2, Pin.IN, Pin.PULL_UP)

# OLED I2C connection to Pico's GPIOS
OLED_SDA = 14
OLED_SCL = 15

# Initialize I2C to control the OLED
i2c = I2C(1, scl=Pin(OLED_SCL), sda=Pin(OLED_SDA), freq=400000)
OLED_WIDTH, OLED_HEIGHT = 128, 64
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

# Global variables for OLED position
a = 0  # x
b = OLED_HEIGHT // 2  # Y

# Main loop:
while True:
    a += 1
    if not up.value():
        b = max(0,b-1)
    if not down.value():
        b = min(OLED_HEIGHT - 1, b + 1)
    if not reset.value():
        oled.fill(0)
        a = 0
        b = OLED_HEIGHT // 2
        
    oled.pixel(a,b,1)
    oled.show()
    a = (a + 1) % oled.width
