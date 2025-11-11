# tlc5940_pio.py  —  stabile MicroPython-Ansteuerung TLC5940 am RP2040
# Pins (Standard):
# GSCLK=GP15 (PIO), BLANK=GP17, XLAT=GP16, SCLK=GP18, SIN=GP19
# VPRG=DCPRG=GND, IREF-Widerstand nach GND, LED-Anoden an +5V

from machine import Pin, SPI
from rp2 import PIO, StateMachine, asm_pio
import time

# ----------------------------------------------------------
# PIO-Programm für GSCLK (50 % Duty)
# ----------------------------------------------------------
@asm_pio(set_init=PIO.OUT_LOW)
def gsclk_prog():
    wrap_target()
    set(pins, 1)
    set(pins, 0)
    wrap()

# ----------------------------------------------------------
# TLC5940-Klasse
# ----------------------------------------------------------
class TLC5940:
    def __init__(self,
                 num_chips=1,
                 spi_baud=8_000_000,
                 gsclk_hz=1_000_000,
                 pin_sin=19,
                 pin_sclk=18,
                 pin_xlat=16,
                 pin_blank=17,
                 pin_gsclk=15):
        self.num = num_chips
        self.channels = 16 * num_chips
        self.spi = SPI(0,
                       baudrate=spi_baud,
                       polarity=0,
                       phase=0,
                       sck=Pin(pin_sclk),
                       mosi=Pin(pin_sin))
        self.pin_xlat  = Pin(pin_xlat,  Pin.OUT, value=0)
        self.pin_blank = Pin(pin_blank, Pin.OUT, value=1)
        self.gsclk = StateMachine(0, gsclk_prog,
                                  freq=gsclk_hz * 2,
                                  set_base=Pin(pin_gsclk))
        self.gsclk_hz = gsclk_hz
        self.gsclk.active(1)

    # ------------------------------------------------------
    def _pack(self, vals):
        """Wandelt 16×12-bit-Werte in Bytestrom um"""
        out = bytearray()
        bitbuf = 0
        bitcount = 0
        for chip in range(self.num - 1, -1, -1):
            base = chip * 16
            for ch in range(15, -1, -1):
                v = vals[base + ch] & 0x0FFF
                for b in range(11, -1, -1):
                    bit = (v >> b) & 1
                    bitbuf = (bitbuf << 1) | bit
                    bitcount += 1
                    if bitcount == 8:
                        out.append(bitbuf)
                        bitbuf = 0
                        bitcount = 0
        if bitcount:
            out.append((bitbuf << (8 - bitcount)) & 0xFF)
        return out

    # ------------------------------------------------------
    def write(self, vals):
        """Daten latched sauber ohne Flackern"""
        data = self._pack(vals)
        self.spi.write(data)
        self.pin_blank.value(1)
        self.pin_xlat.value(1)
        self.pin_xlat.value(0)
        self.pin_blank.value(0)

    # ------------------------------------------------------
    def test_chase(self, delay=0.2):
        ch = [0] * self.channels
        for i in range(self.channels):
            for j in range(self.channels):
                ch[j] = 4095 if j == i else 0
            self.write(ch)
            time.sleep(delay)
        self.pin_blank.value(1)

    # ------------------------------------------------------
    def test_fade_all(self, steps=100, t=3.0):
        """Synchronisierter Fade über ganze Helligkeit"""
        frame_us = int(4096 / self.gsclk_hz * 1_000_000)
        next_us = time.ticks_us()
        ch = [0] * self.channels
        for s in range(steps):
            v = (s * 4095) // (steps - 1)
            for i in range(self.channels):
                ch[i] = v
            # auf Frameende warten, um Reset-Flackern zu vermeiden
            while time.ticks_diff(time.ticks_us(), next_us) < frame_us:
                pass
            next_us = time.ticks_add(next_us, frame_us)
            self.write(ch)
        self.pin_blank.value(1)
