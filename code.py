import usb_hid
import time
import struct

# Wait for HID to become available
while not usb_hid.devices:
    time.sleep(0.1)

# Grab the joystick device we enabled in boot.py
joystick = usb_hid.devices[0]

def send_joystick(x, y):
    """Send 2-axis joystick report. x and y must be between -127 and 127."""
    x = max(-127, min(127, x))
    y = max(-127, min(127, y))
    report = struct.pack("<bb", x, y)
    joystick.send_report(report)

# Example: move in square loop
positions = [
    (0, 0),
    (127, 0),
    (127, 127),
    (0, 127),
    (-127, 127),
    (-127, 0),
    (-127, -127),
    (0, -127),
    (127, -127),
    (0, 0),
]

while True:
    for x, y in positions:
        send_joystick(x, y)
        time.sleep(0.5)