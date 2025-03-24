import machine
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import utime

# Microbuttons connections to Pico's GPIOs
SW_2 = 7
SW_1 = 8
SW_0 = 9

# Microbuttons
but0 = Pin(SW_0, Pin.IN, Pin.PULL_UP)
but1 = Pin(SW_1, Pin.IN, Pin.PULL_UP)
but2 = Pin(SW_2, Pin.IN, Pin.PULL_UP)

# OLED I2C connection to Pico's GPIOS
OLED_SDA = 14
OLED_SCL = 15

# Initialize I2C to control the OLED
i2c = I2C(1, scl=Pin(OLED_SCL), sda=Pin(OLED_SDA), freq=400000)
OLED_WIDTH, OLED_HEIGHT = 128, 64
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

# Global variables for OLED position
a = 0  # x
b = 50  # Y


# Button interrupt handlers
def button_0(pin):
    global a
    print("Button 0 pressed: move right")
    a += 5
    if a > OLED_WIDTH - 28:  # prevent text from going off-screen
        a = OLED_WIDTH - 28


def button_2(pin):
    global a
    print("Button 2 pressed: move left")
    a -= 5
    if a < 0:
        a = 0


# Set interrupts
but0.irq(button_0, Pin.IRQ_FALLING)
but2.irq(button_2, Pin.IRQ_FALLING)

# Main loop:
while True:
    oled.fill(0)  # Clear display first!
    oled.text("<=>", a, b)
    oled.show()

    utime.sleep(0.5)
