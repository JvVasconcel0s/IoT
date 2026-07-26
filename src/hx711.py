from machine import Pin
import time


class HX711:
    def __init__(self, data_pin, clock_pin):
        self.data = Pin(data_pin, Pin.IN)
        self.clock = Pin(clock_pin, Pin.OUT)
        self.clock.value(0)

    def read_raw(self):
        if self.data.value():
            return None

        value = 0

        for _ in range(24):
            self.clock.value(1)
            time.sleep_us(1)
            value = (value << 1) | self.data.value()
            self.clock.value(0)
            time.sleep_us(1)

        self.clock.value(1)
        time.sleep_us(1)
        self.clock.value(0)
        time.sleep_us(1)

        if value & 0x800000:
            value -= 1 << 24

        return value