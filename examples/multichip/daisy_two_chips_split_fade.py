from tlc5940_pio import TLC5940
import time

tlc = TLC5940(num_chips=2, gsclk_hz=1_000_000)
print("Split fade demo: chip#1 fades up, chip#2 fades down")

vals = [0] * tlc.channels
steps = 200

for _ in range(3):
    for s in range(steps):
        up = (s * 4095) // (steps - 1)
        down = 4095 - up
        for ch in range(0, 16):
            vals[ch] = up
        for ch in range(16, 32):
            vals[ch] = down
        tlc.write(vals)
        time.sleep(0.0045)

print("Done.")
