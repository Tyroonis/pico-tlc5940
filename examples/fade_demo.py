from tlc5940_pio import TLC5940

tlc = TLC5940(num_chips=1, gsclk_hz=1_000_000)

print("Starting fade demo...")
tlc.fade_all(duration_s=10.0, fps=120, gamma=1.8, repeats=3)
print("Done.")
