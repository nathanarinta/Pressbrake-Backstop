# test_motor.py
from hardware import STEP_PIN, DIR_PIN, ON_PI
import time

if not ON_PI:
    raise SystemExit("Not running on Pi / GPIO disabled")

print("200 steps forward?")
DIR_PIN.on()   # forward
for _ in range(200):
    STEP_PIN.on()
    time.sleep(0.01)
    STEP_PIN.off()
    time.sleep(0.01)

time.sleep(1)

print("200 steps backward?")
DIR_PIN.off()  # backward
for _ in range(200):
    STEP_PIN.on()
    time.sleep(0.01)
    STEP_PIN.off()
    time.sleep(0.01)

print("Test complete")
