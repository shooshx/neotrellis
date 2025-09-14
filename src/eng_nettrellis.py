# SPDX-FileCopyrightText: 2022 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import util

import board
import supervisor

from adafruit_neotrellis.multitrellis import MultiTrellis
from adafruit_neotrellis.neotrellis import NeoTrellis

# Create the I2C object for the NeoTrellis
i2c_bus = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

WIDTH = 8
HEIGHT = 8
trelli = [
    [NeoTrellis(i2c_bus, False, addr=0x2E, auto_write=False), NeoTrellis(i2c_bus, False, addr=0x2F, auto_write=False)],
    [NeoTrellis(i2c_bus, False, addr=0x30, auto_write=False), NeoTrellis(i2c_bus, False, addr=0x31, auto_write=False)],
    ]


class TrellisEng(util.EngBase, MultiTrellis):
    def __init__(self):
        util.EngBase.__init__(self, WIDTH, HEIGHT)
        MultiTrellis.__init__(self, trelli)
        self.brightness = 0.5
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                # Activate rising edge events on all keys
                self.activate_key(x, y, NeoTrellis.EDGE_RISING)
                # Activate falling edge events on all keys
                self.activate_key(x, y, NeoTrellis.EDGE_FALLING)
                self.set_callback(x, y, self.key_event)
                self.color(x, y, util.OFF)
        self.show()

    def key_event(self, x, y, edge):
        if edge == NeoTrellis.EDGE_RISING:
            self.handler.on_key_up(x, y)
        elif edge == NeoTrellis.EDGE_FALLING:
            self.handler.on_key_down(x, y)

    def main(self, handler):
        self.handler = handler
        handler.eng = self
        while True:
            # The NeoTrellis can only be read every 17 milliseconds or so
            self.sync()
            time.sleep(0.02)
        