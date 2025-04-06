import board
import digitalio
import usb_hid
import storage
import supervisor
import usb_cdc
import time

# Minimal joystick descriptor: 2 axes (X, Y)
JOYSTICK_DESCRIPTOR = bytes((
    0x05, 0x01,        # Usage Page (Generic Desktop)
    0x09, 0x04,        # Usage (Joystick)
    0xA1, 0x01,        # Collection (Application)
    0xA1, 0x00,        #   Collection (Physical)
    0x09, 0x30,        #     Usage (X)
    0x09, 0x31,        #     Usage (Y)
    0x15, 0x81,        #     Logical Minimum (-127)
    0x25, 0x7F,        #     Logical Maximum (127)
    0x75, 0x08,        #     Report Size (8)
    0x95, 0x02,        #     Report Count (2)
    0x81, 0x02,        #     Input (Data, Variable, Absolute)
    0xC0,              #   End Collection
    0xC0               # End Collection
))

# Set up the pin you want to use as jumper check (e.g., GP15)
pin = digitalio.DigitalInOut(board.GP15)
pin.switch_to_input(pull=digitalio.Pull.UP)



if not pin.value:
    # Jumper is connected (GP15 pulled LOW) => enable joystick mode only
    print("Joystick mode  Time: ",time.time())

    # Disable CIRCUITPY + serial
    storage.disable_usb_drive()
    usb_cdc.disable()

    # Enable custom HID (already enabled if set up in code.py)
    usb_hid.enable(
        (usb_hid.Device(
            report_descriptor=JOYSTICK_DESCRIPTOR,
            usage_page=0x1,
            usage=0x4,
            report_ids=(1,),
            in_report_lengths=(4,),
            out_report_lengths=(0,)
        ),)
    )
else:
    # Jumper not connected => allow editing
    print("Edit mode (CIRCUITPY + serial enabled), Time: ",time.time())

    # Enable everything for debugging
    storage.enable_usb_drive()
    usb_cdc.enable(console=True, data=True)