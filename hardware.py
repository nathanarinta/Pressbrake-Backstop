# hardware.py
from gpiozero import DigitalOutputDevice

# Try the newer libgpiod backend (no /dev/gpiomem needed)
try:
    from gpiozero.pins.libgpiod import LibgpiodFactory
    DigitalOutputDevice.pin_factory = LibgpiodFactory()
    BACKEND = "libgpiod"
except ImportError:
    # Fall back to the RPi.GPIO backend
    try:
        from gpiozero.pins.rpigpio import RPiGPIOFactory
        DigitalOutputDevice.pin_factory = RPiGPIOFactory()
        BACKEND = "RPi.GPIO"
    except ImportError:
        BACKEND = None

# Now instantiate once
try:
    STEP_PIN = DigitalOutputDevice(8)
    DIR_PIN  = DigitalOutputDevice(10)
    ON_PI    = True
    print(f"gpiozero initialized via {BACKEND}: STEP=8, DIR=10")
except Exception as e:
    ON_PI    = False
    STEP_PIN = None
    DIR_PIN  = None
    print("gpiozero not available; running in test mode", e)
