import usb_hid
import analogio
import board
import digitalio
import time
import struct

# Setup analog inputs for joystick
x_pin = analogio.AnalogIn(board.A0)  # GP26
y_pin = analogio.AnalogIn(board.A1)  # GP27

# Wait for HID to become available
while not usb_hid.devices:
    time.sleep(0.1)
    print("Waiting for HID devices...")

# Grab the joystick device we enabled in boot.py
joystick = usb_hid.devices[0]

def send_joystick(x, y):
    report = bytearray(2)
    # Convert 16-bit (0-65535) to 8-bit centered (0-255)
    # 32768 (center) becomes 128
    x_centered = (x * 255) // 65535
    y_centered = (y * 255) // 65535
    
    report[0] = x_centered & 0xFF  # X axis
    report[1] = y_centered & 0xFF  # Y axis
    
    try:
        joystick.send_report(report)
    except OSError:
        pass



while True:
    send_joystick(x_pin.value, y_pin.value)
    time.sleep(0.01)