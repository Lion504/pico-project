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

# Rotary encoder GPIO pins
C_LEFT = 10  # Rotary encoder pin for left rotation
C_RIGHT = 11  # Rotary encoder pin for right rotation
C_SWITCH = 12  # Rotary encoder button (optional)

# Initialize rotary encoder pins with pull-up resistors
rot_left = Pin(C_LEFT, Pin.IN, Pin.PULL_UP)
rot_right = Pin(C_RIGHT, Pin.IN, Pin.PULL_UP)
rot_switch = Pin(C_SWITCH, Pin.IN, Pin.PULL_UP)

#get numbers of line
LINE_HEIGHT = 10
MAX_LINE = OLED_HEIGHT // LINE_HEIGHT

#create a list to store text
lines = []
start_qnum = 0

# Rotary encoder state variables
last_state_a = rot_left.value()
last_state_b = rot_right.value()

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
    
# Function to read rotary encoder state and determine direction
def read_rotary_encoder():
    global last_state_a, last_state_b
    
    current_state_a = rot_left.value()
    current_state_b = rot_right.value()
    
    if current_state_a != last_state_a:  # Detect change on pin A (rotation event)
        if current_state_a == current_state_b:  # Determine direction (left rotation)
            scroll_up()
        else:  # Right rotation
            scroll_down()
    
    # Update last states for next comparison
    last_state_a = current_state_a
    
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
       
 # Poll rotary encoder state in each iteration of the loop
    read_rotary_encoder()

