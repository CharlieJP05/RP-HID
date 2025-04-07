import usb_hid
import time
import struct


# upÁ
# Wait for HID to become available
while not usb_hid.devices:
    time.sleep(0.1)
    print("Waiting for HID devices...")

# Grab the joystick device we enabled in boot.py
joystick = usb_hid.devices[0]

def send_joystick(x, y):
    report = bytearray(2)
    # Convert -127..127 to 0..255 range
    report[0] = (x + 127) & 0xFF  # X axis
    report[1] = (y + 127) & 0xFF  # Y axis
    
    try:
        joystick.send_report(report)
    except OSError:
        pass

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