import time
import subprocess
import threading
from pynput import mouse
import sys
import os

## ----------------------------------------------------
## Settings and Constants
## ----------------------------------------------------

# Set XWayland as the runtime environment for maximum compatibility with xdotool
os.environ['GDK_BACKEND'] = 'x11'

# Parameters for continuous automatic scrolling (Speed)
SCROLL_EVENTS_PER_STEP = 2  # Number of events injected every 50ms
DELAY_MS = 0.05             

# xdotool codes (X11 numeric codes for scroll)
SCROLL_UP_KEY = "4"   # Button 4 = Scroll Up
SCROLL_DOWN_KEY = "5" # Button 5 = Scroll Down

# ATTENTION: WE USE THE CORRECT CONSTANT IDENTIFIED VIA DEBUGGING
FORWARD_BUTTON_CODE = mouse.Button.button9 

## ----------------------------------------------------
## Global State Variables (Simplified)
## ----------------------------------------------------

LOCK = threading.Lock()

SCROLLING_AUTOMATICALLY = False
AUTO_SCROLL_DIRECTION = 0   
AUTO_SCROLL_THREAD = None


## ----------------------------------------------------
## Core Functions
## ----------------------------------------------------

def inject_scroll(direction, num_events):
    """ Inject scroll events using xdotool click. """
    key_code = SCROLL_UP_KEY if direction == 1 else SCROLL_DOWN_KEY
    
    try:
        for _ in range(num_events):
            subprocess.run(["xdotool", "click", key_code], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
    except subprocess.CalledProcessError:
        print("\n[FATAL ERROR] xdotool failed during injection. Check xdotool.")
        sys.exit(1)
    except FileNotFoundError:
        print("\n[FATAL ERROR] xdotool is not installed.")
        sys.exit(1)


def auto_scroll_loop():
    """ Background loop that runs and continuously injects scroll events. """
    global SCROLLING_AUTOMATICALLY, AUTO_SCROLL_DIRECTION
    
    while True:
        with LOCK:
            if not SCROLLING_AUTOMATICALLY:
                break
            
            if AUTO_SCROLL_DIRECTION != 0:
                inject_scroll(AUTO_SCROLL_DIRECTION, SCROLL_EVENTS_PER_STEP)
        
        time.sleep(DELAY_MS)
    
    print("Automatic scroll stopped.")


# ----------------------------------------------------
# Button Listener Function (Press/Release)
# ----------------------------------------------------
def on_click(x, y, button, pressed):
    """ Handles the pressing and releasing of the Forward button. """
    global SCROLLING_AUTOMATICALLY
    global AUTO_SCROLL_DIRECTION
    
    if button == FORWARD_BUTTON_CODE:
        if pressed:
            # Forward Press: Enter "Activate on Scroll" mode
            with LOCK:
                SCROLLING_AUTOMATICALLY = True
                print("⚡ Mode activated (Forward button pressed). Awaiting Scroll...")
                
                global AUTO_SCROLL_THREAD
                if AUTO_SCROLL_THREAD is None or not AUTO_SCROLL_THREAD.is_alive():
                    AUTO_SCROLL_THREAD = threading.Thread(target=auto_scroll_loop, daemon=True)
                    AUTO_SCROLL_THREAD.start()
        else:
            # Forward Release: Stop mode
            with LOCK:
                SCROLLING_AUTOMATICALLY = False
                AUTO_SCROLL_DIRECTION = 0 
                print("🛑 Mode deactivated (Forward button released).")


# ----------------------------------------------------
# Scroll Listener Function
# ----------------------------------------------------
def on_scroll(x, y, dx, dy):
    """ Handles scroll events. """
    global AUTO_SCROLL_DIRECTION
    
    if dy == 0:
        return 

    current_direction = 1 if dy > 0 else -1
    
    with LOCK:
        if SCROLLING_AUTOMATICALLY:
            # If the mode is active, update the scroll direction (starts injection)
            AUTO_SCROLL_DIRECTION = current_direction


def main():
    print("🚀 Controlled Scroll Script (Xorg/XWayland) started.")
    print(f"  -> Acceleration mode activates on pressing button {FORWARD_BUTTON_CODE}.")
    print("  -> Acceleration mode stops when the button is released.")
    print("  -> Please ensure you are logged into Xorg.")
    print("  -> Press Ctrl+C to stop the script completely.")
    
    try:
        listener_mouse = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
        listener_mouse.start()
        listener_mouse.join()
        
    except KeyboardInterrupt:
        with LOCK:
            global SCROLLING_AUTOMATICALLY
            SCROLLING_AUTOMATICALLY = False
        print("\nScript stopped by user request.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        
if __name__ == "__main__":
    main()