import machine
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
import utime

# OLED I2C connection to Pico's GPIOS
OLED_SDA = 14
OLED_SCL = 15

# Initialize I2C to control the OLED
i2c = I2C(1, scl=Pin(OLED_SCL), sda=Pin(OLED_SDA), freq=400000)
OLED_WIDTH, OLED_HEIGHT = 128, 64
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

# Button GPIO pins
SW_0 = 9  # Down button
SW_2 = 7  # Up button

# Initialize buttons with pull-up resistors
but_up = Pin(SW_2, Pin.IN, Pin.PULL_UP)
but_down = Pin(SW_0, Pin.IN, Pin.PULL_UP)

#get numbers of line
LINE_HEIGHT = 10
MAX_LINE = OLED_HEIGHT // LINE_HEIGHT

#create a list to store text
lines = []
start_qnum = 0

def over_width(text):
    character_width = 8
    MAX_TEXT = OLED_WIDTH // character_width
    
    if len(text) > MAX_TEXT:
        return text[:MAX_TEXT - 3] + '...'
    else:
        return text

#Function to update the OLED display with current lines
def update_display():
    oled.fill(0)
     # Display lines from history starting at `display_start_index`
    for i in range(MAX_LINE):
        line_index = start_qnum + i
        
        if line_index < len(lines):
            oled.text(lines[line_index], 0, i * LINE_HEIGHT)
    oled.show() 

def scroll_up (pin):
    global start_qnum
    if start_qnum > 0:
        start_qnum -= 1
        
    update_display()  
    
def scroll_down (pin):
    global start_qnum
    if start_qnum + MAX_LINE < len(lines):
        start_qnum += 1
        
    update_display()
    
# Attach interrupts for buttons (falling edge triggers)
but_up.irq(trigger=Pin.IRQ_FALLING, handler=scroll_up)
but_down.irq(trigger=Pin.IRQ_FALLING, handler=scroll_down)
    
#instractions   
print("Enter text in the Shell. Type 'q' to exit.")

# Main loop:
while True:
    #show typed text
    user_input = input("> ")
    #exit type
    if user_input.lower() == "q":
        print("Exiting.....")
        break
        
    LINE_WIDTH = over_width(user_input)
    lines.append(LINE_WIDTH)
    
    #handle over height
    if len(lines) > MAX_LINE :
        start_qnum = len(lines) - MAX_LINE
    
    update_display()
