# SPDX-FileCopyrightText: 2022 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import board

from adafruit_neotrellis.neotrellis import NeoTrellis

# create the i2c object for the trellis
i2c_bus = board.I2C()  # uses board.SCL and board.SDA
# i2c_bus = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# create the trellis
trellis = NeoTrellis(i2c_bus)

# Set the brightness value (0 to 1.0)

# some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

led_state = [0] * 16


# this will be called when button events are received
def blink(event):
    
    if event.edge == NeoTrellis.EDGE_RISING:
        if led_state[event.number] == 1:
            trellis.pixels[event.number] = OFF
            led_state[event.number] = 0
        else:    
            trellis.pixels[event.number] = CYAN
            led_state[event.number] = 1
    #trellis.sync()
    # turn the LED off when a falling edge is detected
    #elif event.edge == NeoTrellis.EDGE_FALLING:
    #    trellis.pixels[event.number] = OFF

def init():
   trellis.brightness = 0.5
   for i in range(16):
        # activate rising edge events on all keys
        trellis.activate_key(i, NeoTrellis.EDGE_RISING)
        # activate falling edge events on all keys
        trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
        # set all keys to trigger the blink callback
        trellis.callbacks[i] = blink

def fill(color):
    for i in range(16):
        trellis.pixels[i] = PURPLE
    

def main():
    init()
    fill(GREEN)
    time.sleep(1)
    #fill(RED)
    #time.sleep(1)
    fill(OFF)
    time.sleep(1)

    while True:
        # call the sync function call any triggered callbacks
        trellis.sync()
        # the trellis can only be read every 17 millisecons or so
        time.sleep(0.02)

main()