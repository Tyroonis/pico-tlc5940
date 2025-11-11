from tlc5940_pio import TLC5940
import time

tlc = TLC5940(num_chips=2, gsclk_hz=1_000_000)
print("Two-chip chase demo (32 channels)...")

vals = [0] * tlc.channels

def write_single(index, level=4095):
    for i in range(tlc.channels):
        vals[i] = level if i == index else 0
    tlc.write(vals)

for _ in range(3):
    for i in range(tlc.channels):
        write_single(i, 4095)
        time.sleep(0.08)
    for i in range(tlc.channels - 1, -1, -1):
        write_single(i, 4095)
        time.sleep(0.08)

print("Done.")
