from pypozyx import * 
from pypozyx.definitions.registers import POZYX_WHO_AM_I

port = get_serial_ports()[0].device
pozyx = PozyxSerial(port)

pozyx.getRead(POZYX_WHO_AM_I, data, remote_id=None)
print('who am i: 0x%0.2x' % data[0])
print('firmware version: 0x%0.2x' % data[1])
print('hardware version: 0x%0.2x' % data[2])
print('self test result: %s' % bin(data[3]))
print('error: 0x%0.2x' % data[4])
