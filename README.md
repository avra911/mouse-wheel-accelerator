# 🚀 Linux Scroll Accelerator (Triggered Mode)

This Python script emulates accelerated/infinite scrolling behavior (similar to Logitech SmartShift or MagSpeed) on Linux systems running Xorg/XWayland.

The acceleration mode is enabled only while an extra mouse button (default: Button 9) is held down.

---

## ⚙️ How It Works

1. The script listens for mouse events.
2. When **Button 9** (Forward Button) is pressed, the script enters acceleration mode.
3. In this mode, any mouse wheel movement is converted into a continuous injection of scroll events, accelerating scrolling.
4. **The mode stops only when the user performs a scroll in the opposite direction of the current acceleration.**

---

## 📋 Prerequisites

The script requires two main dependencies:

1. **`pynput`**: To listen to mouse events.
2. **`xdotool`**: To inject scroll events back into the system (works on Xorg and XWayland).

### 1. Installing the System Tool (`xdotool`)

Open a terminal and install `xdotool`:

```bash
# For Debian/Ubuntu-based distributions
sudo apt update
sudo apt install xdotool
```

### 2. Setting Up a Python Environment (`venv`)

It is recommended to use a virtual environment (`venv`):

```bash
# Create and activate the virtual environment
python3 -m venv venv
source venv/bin/activate
```

### 3. Installing Python Dependencies

Install `pynput` in the activated virtual environment:

```bash
pip install pynput
```

---

## 🖱️ Usage and Running

### 1. Running the Script

Run:

```bash
./start_scroll.sh
```

### 2. Operation Logic

* **Activate:** Press and hold **Button 9** (Forward Button).
* **Scroll:** Turn the mouse wheel. Scrolling will be much faster.
* **Deactivate:** Release **Button 9**. Scrolling returns to normal speed.

---

## ⚠️ IMPORTANT NOTE ABOUT XORG AND WAYLAND

This script uses **`xdotool`** to inject events, so it depends on the X11 protocol.

* **Best on Xorg:** For full functionality across all windows, make sure you log into an **Xorg** session (for example, "GNOME on Xorg") when starting the system.
* **Limited on Wayland:** On Wayland, the script will only work for applications running under the **XWayland** compatibility layer.

### Checking the Button (Debugging)

If the Forward button doesn't work or you use a different mouse, check which button code your system reports:

1. Run **`xev`** in a terminal.
2. Move the mouse cursor into the `xev` window and press the desired button.
3. If `xev` reports a different number than **9** (for example, **8**), you must manually change the `FORWARD_BUTTON_CODE` line in the script.


### Adding to Startup Applications (Ubuntu)

You can make the script start automatically when you log in on Ubuntu by adding it to the GUI Startup Applications:
- Make sure `start_scroll.sh` is executable:
  ```bash
  chmod +x /home/razvan/Projects/mouse-wheel-accelerator/start_scroll.sh
  ```
- Open "Startup Applications" (press Super, type "Startup Applications" and open it).
- Click "Add".
  - Name: Mouse Wheel Accelerator
  - Command: /home/razvan/Projects/mouse-wheel-accelerator/start_scroll.sh
  - Comment: Start scroll accelerator at login
- Save and log out/in to test.
