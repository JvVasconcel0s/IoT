from machine import Pin
import time


class HX711:
    """Driver mínimo do HX711 pela interface serial DT/SCK."""

    def __init__(self, data_pin, clock_pin):
        self.data = Pin(data_pin, Pin.IN)
        self.clock = Pin(clock_pin, Pin.OUT)
        self.clock.value(0)

    def read_raw(self):
        """Lê os 24 bits do conversor e devolve um inteiro com sinal."""
        if self.data.value():
            return None

        value = 0

        # O HX711 envia 24 bits, do mais significativo para o menos significativo.
        for _ in range(24):
            self.clock.value(1)
            time.sleep_us(1)
            value = (value << 1) | self.data.value()
            self.clock.value(0)
            time.sleep_us(1)

        # O 25º pulso seleciona ganho 128 para a próxima conversão.
        self.clock.value(1)
        time.sleep_us(1)
        self.clock.value(0)
        time.sleep_us(1)

        # O bit 23 indica sinal negativo no formato de complemento de dois.
        if value & 0x800000:
            value -= 1 << 24

        return value
