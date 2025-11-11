from tlc5940_pio import TLC5940
import time

tlc = TLC5940(num_chips=1, gsclk_hz=1_000_000)

print("Lauflicht...")
tlc.test_chase(0.50)

print("Faden...")
tlc.test_fade_all(steps=400, t=3.0)

# statisches Muster prüfen
vals = [0]*16
vals[0], vals[1], vals[2] = 4095, 2048, 512
tlc.write(vals)
time.sleep(2)

print("Fertig")
