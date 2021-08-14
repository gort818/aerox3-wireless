#!/usr/bin/env python3

import hid
import time
import sys

VENDOR_ID = 0x1038
PRODUCT_ID = 0x1838
ENDPOINT = 3

def open_device(vendor_id, product_id, endpoint):
    path = None
    device = hid.device()

    # Search the device
    for interface in hid.enumerate(vendor_id, product_id):
        if interface["interface_number"] == endpoint:
            path = interface["path"]
            break

    # Open the found device. This can raise an IOError.
    if path:
        device.open_path(path)
        return device

    # No matching device found
    raise Exception("Requested device or endpoint not found: %04x:%04x:%02x" % (  # noqa
        vendor_id, product_id, endpoint))

def write():
    
    try:
        device = open_device(VENDOR_ID, PRODUCT_ID, ENDPOINT)
    except IOError as ex:
       print(ex)
       print("Could not open Device.")
       sys.exit(1)
       


    # Write LEDs
    # Command 
    # [write led] [LED #] [RGB]
    # [61 01] [00] [FF FF FF] 
    #cmd=\x61\x01
    #led1=\x00
    #led2=\x01
    #led3=\x02
    #off=\x00\x00\x00
    #white=\xFF\xFF\xFF
    #red=\xFF\x00\x00
    
    # enable non-blocking mode
    device.set_nonblocking(1)
    
    device.write(b"\x61\x01\x02\xFF\x00\x00") # Write to LED #3
    time.sleep(.05)
    device.write(b"\x61\x01\x01\x00\x00\x00") # Write to LED #2
    time.sleep(.05)
    device.write(b"\x61\x01\x00\x00\x00\x00") # Wtire to LED #1
    time.sleep(.05)
    #device.write(b"\x63\x01\x01\x01\x00\x30\x75") # SET LED intensity
    
    
        
    device.close()



if __name__ == "__main__":
    write()
    
