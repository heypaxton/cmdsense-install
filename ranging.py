#!/usr/bin/env python
"""
The Pozyx ready to range tutorial (c) Pozyx Labs
Please read the tutorial that accompanies this sketch: https://www.pozyx.io/Documentation/Tutorials/ready_to_range/Python

This demo requires two Pozyx devices and one Arduino. It demonstrates the ranging capabilities and the functionality to
to remotely control a Pozyx device. Place one of the Pozyx shields on the Arduino and upload this sketch. Move around
with the other Pozyx device.

This demo measures the range between the two devices. The closer the devices are to each other, the more LEDs will
light up on both devices.
"""
from pypozyx import *
import time
import requests
import json


class ReadyToRange(object):
    """Continuously performs ranging between the Pozyx and a destination and sets their LEDs"""

    def __init__(self, pozyx, destination_id, range_step_mm=1000, remote_id=None):
        self.pozyx = pozyx
        self.destination_id = destination_id
        self.range_step_mm = range_step_mm
        self.remote_id = remote_id

    def setup(self):
        """Sets up both the ranging and destination Pozyx's LED configuration"""
        print("------------POZYX RANGING V1.0 - -----------")
        print("NOTES: ")
        print(" - Change the parameters: ")
        print("\tdestination_id(target device)")
        print("\trange_step(mm)")
        print()
        print("- Approach target device to see range and")
        print("led control")
        print("- -----------POZYX RANGING V1.0 ------------")
        print()
        print("START Ranging: ")

        # make sure the local/remote pozyx system has no control over the LEDs.
        led_config = 0x0
        self.pozyx.setLedConfig(led_config, self.remote_id)
        # do the same for the destination.
        self.pozyx.setLedConfig(led_config, self.destination_id)

    def loop(self):
        """Performs ranging and sets the LEDs accordingly"""
        device_range = DeviceRange()
        status = self.pozyx.doRanging(self.destination_id, device_range, self.remote_id)
        if status == POZYX_SUCCESS:
            print(device_range)
            dweet = requests.post("https://dweet.io/dweet/for/cmdsense-tag", {
                "distance": device_range.distance
            })
	   
	
            if self.ledControl(device_range.distance) == POZYX_FAILURE:
                print("ERROR: setting (remote) leds")
        else:
            print("ERROR: ranging")

    def ledControl(self, distance):
        """Sets LEDs according to the distance between two devices"""
        status = POZYX_SUCCESS
        ids = [self.remote_id, self.destination_id]
        # set the leds of both local/remote and destination pozyx device
        for id in ids:
            status &= self.pozyx.setLed(4, (distance < range_step_mm), id)
            status &= self.pozyx.setLed(3, (distance < 2 * range_step_mm), id)
            status &= self.pozyx.setLed(2, (distance < 3 * range_step_mm), id)
            status &= self.pozyx.setLed(1, (distance < 4 * range_step_mm), id)
        return status

if __name__ == "__main__":
    port = get_serial_ports()[0].device
    # port = 'ttyAMA0'
    print(port)
    #port = 'COM12'                # COM port of the Pozyx device

    remote_id = 0x604E           # the network ID of the remote device
    remote = False               # whether to use the given remote device for ranging
    if not remote:
        remote_id = None

    destination_id = 0x6001      # network ID of the ranging destination
    range_step_mm = 500         # distance that separates the amount of LEDs lighting up.

    pozyx = PozyxSerial(port)
    # pozyx.getUWBChannel()
    r = ReadyToRange(pozyx, destination_id, range_step_mm, remote_id)
    r.setup()
    while True:
        r.loop()
        # time.sleep(1)
