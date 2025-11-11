# TLC5940 MicroPython Driver for Raspberry Pi Pico / Pico W

A lightweight and stable **MicroPython library** to drive one or more **TLC5940 constant-current LED driver ICs** from a **Raspberry Pi Pico or Pico W (RP2040)**.

This project uses **hardware SPI** and **PIO-based GSCLK generation** for smooth PWM and flicker-free fades.  
It’s ideal for testing TLC5940 chips, controlling LED matrices, or building your own lighting projects.

---

## ✨ Features

- 🧠 Written in pure **MicroPython**
- ⚡ Uses **PIO** for stable GSCLK up to 1 MHz (≈ 244 Hz PWM refresh)
- 🔄 Hardware SPI for high-speed grayscale data transfer
- 🌈 Smooth, flicker-free **fade**, **blink**, and **chase** effects
- 🔧 Configurable number of chained TLC5940 chips
- 💡 Compatible with both Pico and Pico W

---

## 🧰 Hardware Requirements

| Component | Description |
|------------|-------------|
| **Raspberry Pi Pico / Pico W** | MicroPython firmware v1.20 or newer |
| **TLC5940** | 16-channel constant-current LED driver |
| **LEDs** | Common-anode setup (anode → +5 V, cathode → OUTx) |
| **Resistor** | IREF resistor sets LED current (e.g. 3.3 kΩ → ≈ 12 mA) |
| **Power Supply** | 5 V for LEDs and TLC5940, common GND with Pico |

---

## ⚙️ Wiring

| TLC5940 Pin | Function | Pico GPIO | Notes |
|--------------|-----------|------------|-------|
| **SIN** | Serial data input | GP19 (SPI0 MOSI) | Data in |
| **SCLK** | Serial clock | GP18 (SPI0 SCK) | Data clock |
| **XLAT** | Latch | GP16 | Triggers new frame |
| **BLANK** | Output enable | GP17 | Active high (resets PWM counter) |
| **GSCLK** | Grayscale clock | GP15 (PIO) | Must be fast (≈ 1 MHz) |
| **VPRG** | Mode select | GND | Grayscale mode |
| **DCPRG** | Dot-correction source | GND | Disable EEPROM |
| **IREF** | Current reference | Resistor → GND | Sets per-channel current |
| **OUT0–15** | LED outputs | – | Current sinks |
| **VCC / GND** | Power | 5 V / GND | Common ground with Pico |

💡 **Note:** TLC5940 is a *current-sink* device – connect LED **anodes** to +5 V and **cathodes** to OUTx pins.

---

## 🧩 Installation

1. Flash the official **MicroPython firmware** for Raspberry Pi Pico  
   → [https://micropython.org/download/RPI_PICO/](https://micropython.org/download/RPI_PICO/)
2. Copy these files to your Pico:
   ```
   tlc5940_pio.py
   main.py
   ```
3. Connect via Thonny or VS Code + MicroPico, and run `main.py`.

---

## 🚀 Usage Examples

### Basic setup
```python
from tlc5940_pio import TLC5940
tlc = TLC5940(num_chips=1, gsclk_hz=1_000_000)
```

### Blink all LEDs
```python
tlc.blink_all(times=8, on_ms=150, off_ms=200, level=4095)
```

### Long smooth fade
```python
tlc.fade_all(duration_s=15.0, fps=120, gamma=1.8, repeats=2)
```

### LED chase
```python
tlc.test_chase(delay=0.10, repeats=3, level=4095)
```

### Static pattern
```python
vals = [0]*16
vals[0], vals[1], vals[2] = 4095, 2048, 512
tlc.write(vals)
```

---

## 🔬 Theory of Operation

- **GSCLK (Grayscale Clock)** – Advances the 12-bit PWM counter (4096 steps).  
  Must run continuously at high speed (recommended ≥ 500 kHz).
- **BLANK** – Active HIGH — resets PWM counter and temporarily disables outputs.  
  Set HIGH during latching, LOW for normal operation.
- **XLAT** – Rising edge latches the shifted grayscale data into output registers.
- **SIN/SCLK** – SPI interface for 192 bits × number of TLC5940 chips.

---

## 🔧 Configuration

Inside `TLC5940(...)` you can adjust:
```python
num_chips   # number of TLC5940 ICs in daisy-chain
spi_baud    # SPI speed (default 8 MHz)
gsclk_hz    # grayscale clock frequency (default 1 MHz)
pin_xlat    # XLAT pin (default GP16)
pin_blank   # BLANK pin (default GP17)
pin_sin     # SPI MOSI (default GP19)
pin_sclk    # SPI SCK (default GP18)
pin_gsclk   # GSCLK PIO pin (default GP15)
```

---

## 🧪 Example Setup

```
+5 V ──► LED Anodes
LED Cathodes ─► OUT0..OUT15
Pico GP19 ─► SIN
Pico GP18 ─► SCLK
Pico GP16 ─► XLAT
Pico GP17 ─► BLANK
Pico GP15 ─► GSCLK
GND ───► common ground
```

---

## 📄 License

MIT License  
© 2025 Tyroonis / Patrick Guß  

Feel free to modify, distribute, and use for personal or commercial projects.

---

## 💬 Future Work

- [ ] Dot-correction (6-bit DC data)  
- [ ] XERR monitoring for open/short detection  
- [ ] Multi-chip daisy-chain examples  
- [ ] Pattern and animation utilities  

---

### ⭐ If this project helped you, consider starring it on GitHub!
