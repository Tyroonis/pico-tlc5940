# Examples for Multi-Chip Daisy Chain (pico-tlc5940)

This folder contains demo scripts for using **multiple TLC5940 chips in daisy-chain mode** with the Raspberry Pi Pico / Pico W.

## Files

### 🧪 `daisy_two_chips_chase.py`
Demonstrates a two-chip configuration (32 channels total) with a chasing light effect across all outputs.

### 🌗 `daisy_two_chips_split_fade.py`
Shows independent fades for two TLC5940 chips: the first chip fades up while the second fades down.

### 🌈 `daisy_two_chips_rgb_groups.py`
Uses two TLC5940 chips to control up to **10 RGB LEDs (30 channels)** with HSV rainbow color transitions.

## Wiring Notes

- Connect **SOUT** of the first TLC5940 → **SIN** of the second TLC5940.  
- Connect **SCLK**, **XLAT**, **BLANK**, and **GSCLK** in parallel to all chips.  
- Set `num_chips=2` in the constructor:
  ```python
  tlc = TLC5940(num_chips=2, gsclk_hz=1_000_000)
  ```
- Power, ground, and IREF resistor per chip must be properly connected.

