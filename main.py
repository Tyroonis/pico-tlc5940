from tlc5940_pio import TLC5940
import time

tlc = TLC5940(num_chips=1, gsclk_hz=1_000_000)

# 1) Blink 
tlc.blink_all(times=8, on_ms=150, off_ms=200, level=4095)

# 2) Fade 
tlc.fade_all(duration_s=15.0, fps=120, gamma=1.8, repeats=2)

# 3) Chase 
tlc.test_chase(delay=0.10, repeats=3, level=4095)

# 4) Statisches Muster
vals = [0]*16
vals[0], vals[1], vals[2] = 4095, 2048, 512
tlc.write(vals)
time.sleep(2)