from tlc5940_pio import TLC5940
import time

tlc = TLC5940(num_chips=2, gsclk_hz=1_000_000)
vals = [0] * tlc.channels

RGB_COUNT = 10
rgb_groups = [(i*3 + 0, i*3 + 1, i*3 + 2) for i in range(RGB_COUNT)]

def set_rgb(idx, r, g, b):
    r = max(0, min(4095, int(r)))
    g = max(0, min(4095, int(g)))
    b = max(0, min(4095, int(b)))
    ri, gi, bi = rgb_groups[idx]
    vals[ri], vals[gi], vals[bi] = r, g, b

def hsv2rgb(h, s, v):
    i = int(h*6) % 6
    f = h*6 - i
    p = v*(1-s)
    q = v*(1-f*s)
    t = v*(1-(1-f)*s)
    if i == 0: r,g,b = v,t,p
    elif i == 1: r,g,b = q,v,p
    elif i == 2: r,g,b = p,v,t
    elif i == 3: r,g,b = p,q,v
    elif i == 4: r,g,b = t,p,v
    else: r,g,b = v,p,q
    return r,g,b

print("RGB group demo on two TLC5940 chips (10 RGB LEDs)...")

for cycle in range(3):
    for step in range(180):
        hue = (step % 180) / 180.0
        for i in range(RGB_COUNT):
            h = (hue + i / RGB_COUNT) % 1.0
            r,g,b = hsv2rgb(h, 1.0, 1.0)
            set_rgb(i, r*4095, g*4095, b*4095)
        tlc.write(vals)
        time.sleep(0.02)

print("Done.")
