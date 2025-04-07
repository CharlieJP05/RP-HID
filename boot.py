import board
import digitalio
import usb_hid
import storage
import supervisor
import usb_cdc
import time

# updater: sssssssssdfsssssss
# Modified joystick descriptor with minimal controls
DEVICE_TYPE = 0x04  # 0x04 (Joystick) 0x05 (Gamepad)
JOYSTICK_DESCRIPTOR = bytes((
    0x05, 0x01,        # Usage Page (Generic Desktop)
    0x09, DEVICE_TYPE,        # Usage (Joystick or Gamepad)
    0xA1, 0x01,        # Collection (Application)
    0x85, 0x01,        #   Report ID (1)
    0x09, 0x30,        #   Usage (X)
    0x09, 0x31,        #   Usage (Y)
    0x15, 0x00,        #   Logical Minimum (0)
    0x26, 0xFF, 0x00,  #   Logical Maximum (255)
    0x75, 0x08,        #   Report Size (8 bits)
    0x95, 0x02,        #   Report Count (2 values: X and Y)
    0x81, 0x02,        #   Input (Data, Var, Abs)
    0xC0               # End Collection
))

# Set up the pin you want to use as jumper checks (e.g., GP15)
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
        usage_page=0x01,
        usage=DEVICE_TYPE,             # Joystick
        report_ids=(1,),
        in_report_lengths=(2,),
        out_report_lengths=(0,)
    ),)
)
else:
    # Jumper not connected => allow editing
    print("Edit mode (CIRCUITPY + serial enabled) Time: ", time.time())

    # Disable all HID devices first
    usb_hid.disable()
    
    # Enable everything for debugging
    storage.enable_usb_drive()
    usb_cdc.enable(console=True, data=True)