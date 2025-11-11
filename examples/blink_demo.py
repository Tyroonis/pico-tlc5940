from tlc5940_pio import TLC5940
import time

tlc = TLC5940(num_chips=1, gsclk_hz=1_000_000)

print("Blink demo...")
tlc.blink_all(times=10, on_ms=150, off_ms=200, level=4095)

print("Done.")
