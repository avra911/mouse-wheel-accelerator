import time
import subprocess
import threading
from pynput import mouse
import sys
import os

# ----------------------------------------------------
# Settings and Constants
# ----------------------------------------------------

# Set XWayland as the runtime environment for maximum compatibility with xdotool
os.environ['GDK_BACKEND'] = 'x11'

# NEW: Toggle logging/debugging messages
VERBOSE = False

# Parameters for continuous automatic scrolling (Speed)
SCROLL_EVENTS_PER_STEP = 2
DELAY_MS = 0.05

# xdotool codes (X11 numeric codes for scroll)
SCROLL_UP_KEY = "4"
SCROLL_DOWN_KEY = "5"

# Button 9 (Forward button) constant
FORWARD_BUTTON_CODE = mouse.Button.button9

# ----------------------------------------------------
# Global State Variables
# ----------------------------------------------------

LOCK = threading.Lock()

SCROLLING_AUTOMATICALLY = False
AUTO_SCROLL_DIRECTION = 0
AUTO_SCROLL_THREAD = None

# ----------------------------------------------------
# Logging Function
# ----------------------------------------------------


def log(message):
    """Prints the message only if VERBOSE is True."""
    if VERBOSE:
        print(message)

# ----------------------------------------------------
# Core Functions
# ----------------------------------------------------


def inject_scroll(direction, num_events):
    """ Inject scroll events using xdotool click. """
    key_code = SCROLL_UP_KEY if direction == 1 else SCROLL_DOWN_KEY

    try:
        for _ in range(num_events):
            subprocess.run(["xdotool", "click", key_code], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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

    log("Automatic scroll stopped.")


# ----------------------------------------------------
# Button Listener Function
# ----------------------------------------------------
def on_click(x, y, button, pressed):
    """ Handles B9 Press (START MODE) and ignores B9 Release. """
    global SCROLLING_AUTOMATICALLY

    if button == FORWARD_BUTTON_CODE:
        if pressed:
            # START MODE: Activate on B9 Press
            with LOCK:
                SCROLLING_AUTOMATICALLY = True
                log("Acceleration Mode Activated (Requires opposite scroll to stop).")

                global AUTO_SCROLL_THREAD
                if AUTO_SCROLL_THREAD is None or not AUTO_SCROLL_THREAD.is_alive():
                    AUTO_SCROLL_THREAD = threading.Thread(
                        target=auto_scroll_loop, daemon=True)
                    AUTO_SCROLL_THREAD.start()

        # NOTE: The 'else' (release logic) is intentionally removed to keep the mode active.


# ----------------------------------------------------
# Scroll Listener Function (Handles Direction and STOP)
# ----------------------------------------------------
def on_scroll(x, y, dx, dy):
    """ Handles scroll events (dictates direction and stop). """
    global AUTO_SCROLL_DIRECTION, SCROLLING_AUTOMATICALLY

    if dy == 0:
        return

    current_scroll_direction = 1 if dy > 0 else -1

    with LOCK:
        if SCROLLING_AUTOMATICALLY:
            # 1. Check for STOP condition (Scroll in opposite direction after mode started)
            if current_scroll_direction != AUTO_SCROLL_DIRECTION and AUTO_SCROLL_DIRECTION != 0:
                SCROLLING_AUTOMATICALLY = False
                AUTO_SCROLL_DIRECTION = 0
                log("Mode deactivated (Opposite scroll detected).")
                return  # Stop processing this event

            # 2. Update/Set the active scroll direction (This starts/maintains the injection)
            AUTO_SCROLL_DIRECTION = current_scroll_direction


def main():
    print("Toggle Scroll Control Script (Xorg/XWayland) started.")
    print(f"  -> ACTIVARE: Apăsare buton {FORWARD_BUTTON_CODE}.")
    print("  -> OPRIRE: Scroll în direcția opusă.")
    print("  -> Vă rugăm să vă asigurați că sunteți logat în Xorg.")
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
