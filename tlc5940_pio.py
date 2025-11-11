# tlc5940_pio.py  —  stabile MicroPython-Ansteuerung TLC5940 am RP2040
# Pins (Standard):
# GSCLK=GP15 (PIO), BLANK=GP17, XLAT=GP16, SCLK=GP18, SIN=GP19
# VPRG=DCPRG=GND, IREF-Widerstand nach GND, LED-Anoden an +5V

from machine import Pin, SPI
from rp2 import PIO, StateMachine, asm_pio
import time
import math

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
        self.num = int(num_chips)
        self.channels = 16 * self.num
        self.spi = SPI(0,
                       baudrate=int(spi_baud),
                       polarity=0,
                       phase=0,
                       sck=Pin(pin_sclk),
                       mosi=Pin(pin_sin))
        self.pin_xlat  = Pin(pin_xlat,  Pin.OUT, value=0)
        self.pin_blank = Pin(pin_blank, Pin.OUT, value=1)
        self.gsclk = StateMachine(0, gsclk_prog,
                                  freq=int(gsclk_hz) * 2,
                                  set_base=Pin(pin_gsclk))
        self.gsclk_hz = int(gsclk_hz)
        self.gsclk.active(1)

    # ------------------------------------------------------
    def _pack(self, vals):
        """Wandelt 16×12-bit-Werte in Bytestrom um (letzter Chip zuerst, ch15..0, MSB-first)"""
        if len(vals) != self.channels:
            raise ValueError("Expected %d channels, got %d" % (self.channels, len(vals)))
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
    def blink_all(self, times=5, on_ms=200, off_ms=300, level=4095):
        """Blinkt alle Kanäle mehrfach"""
        lvl = max(0, min(4095, int(level)))
        on  = [lvl] * self.channels
        off = [0]   * self.channels
        t_on, t_off = int(on_ms), int(off_ms)
        for _ in range(max(1, int(times))):
            self.write(on)
            time.sleep_ms(t_on)
            self.write(off)
            time.sleep_ms(t_off)

    # ------------------------------------------------------
    def fade_all(self, duration_s=12.0, fps=120, gamma=1.8, repeats=1):
        """Langer, weicher Fade """
        steps = max(2, int(duration_s * fps))
        frame_us = int(4096 / self.gsclk_hz * 1_000_000)
        ch = [0] * self.channels
        for _ in range(max(1, int(repeats))):
            next_us = time.ticks_us()
            for s in range(steps):
                t = s / (steps - 1)
                if gamma and gamma != 1.0:
                    t = math.pow(t, gamma)
                v = int(t * 4095)
                for i in range(self.channels):
                    ch[i] = v
                while time.ticks_diff(time.ticks_us(), next_us) < frame_us:
                    pass
                next_us = time.ticks_add(next_us, frame_us)
                self.write(ch)
        # Endwert bleibt stehen

    # ------------------------------------------------------
    def test_chase(self, delay=0.15, repeats=1, level=4095):
        """Lauflicht"""
        ch = [0] * self.channels
        lvl = max(0, min(4095, int(level)))
        for _ in range(max(1, int(repeats))):
            for i in range(self.channels):
                for j in range(self.channels):
                    ch[j] = lvl if j == i else 0
                self.write(ch)
                time.sleep(delay)
        self.pin_blank.value(1)  # aus

    # ------------------------------------------------------
    # Lagacy Code
    def test_fade_all(self, steps=100, t=3.0):
        """Alte API: behalte zur Sicherheit (einfacher linearer Fade)."""
        frame_us = int(4096 / self.gsclk_hz * 1_000_000)
        next_us = time.ticks_us()
        ch = [0] * self.channels
        for s in range(steps):
            v = (s * 4095) // (steps - 1)
            for i in range(self.channels):
                ch[i] = v
            while time.ticks_diff(time.ticks_us(), next_us) < frame_us:
                pass
            next_us = time.ticks_add(next_us, frame_us)
            self.write(ch)
        self.pin_blank.value(1)
