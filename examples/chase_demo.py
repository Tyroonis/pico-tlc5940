from tlc5940_pio import TLC5940

tlc = TLC5940(num_chips=1, gsclk_hz=1_000_000)

print("Chase demo...")
tlc.test_chase(delay=0.1, repeats=5, level=4095)
print("Done.")
