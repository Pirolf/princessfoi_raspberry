# Copyright Pololu Corporation.  For more information, see https://www.pololu.com/
import smbus
import struct
import time

class AStar:
  def __init__(self):
    self.bus = smbus.SMBus(1)

  def read_unpack(self, address, size, format):
    # Ideally we could do this:
    #    byte_list = self.bus.read_i2c_block_data(20, address, size)
    # But the AVR's TWI module can't handle a quick write->read transition,
    # since the STOP interrupt will occasionally happen after the START
    # condition, and the TWI module is disabled until the interrupt can
    # be processed.
    #
    # A delay of 0.0001 (100 us) after each write is enough to account
    # for the worst-case situation in our example code.

    self.bus.write_byte(20, address)
    time.sleep(0.0001)
    byte_list = [self.bus.read_byte(20) for _ in range(size)]
    return struct.unpack(format, bytes(byte_list))

  def write_pack(self, address, format, *data):
    data_array = list(struct.pack(format, *data))
    self.bus.write_i2c_block_data(20, address, data_array)
    time.sleep(0.0001)

  # [0, 2], R Y G lights
  # [3, 5] buttons
  # [6, 9] 2 bytes each for motors
  # [10, 11] mv
  # [12, 23] 6 analog signals
  # [24, 38] 15 bytes for notes
  # [39, 46] left and right encoder
  # [47] whether to clear encoder values
  def read_bytes(self, address=0, size=64):
    self.bus.write_byte(20, address)
    time.sleep(0.01)
    li = [self.bus.read_byte(20) for _ in range(size)]
    byte_array = list(map(lambda x: format(x, '02x'), bytes(li)))
    print('raw bytes = {}, list = {}'.format(byte_array, li))

  # [0, 2], R Y G lights
  def leds(self, red, yellow, green):
    self.write_pack(0, 'BBB', red, yellow, green)

  # [24, 38] 15 bytes for notes
  def play_notes(self, notes):
    self.write_pack(24, 'B15s', 1, notes.encode("ascii"))

  # [6, 9] 2 bytes each for motors
  def motors(self, left, right):
    self.write_pack(6, 'hh', left, right)

  # [3, 5] buttons
  def read_buttons(self):
    return self.read_unpack(3, 3, "???")

  # [10, 11] mv
  def read_battery_millivolts(self):
    return self.read_unpack(10, 2, "H")

  # [12, 23] 6 analog signals
  def read_analog(self):
    return self.read_unpack(12, 12, "HHHHHH")

  # [39, 46] left and right encoder
  def read_encoders(self):
    return self.read_unpack(39, 8, 'hhhh')

  # [47] whether to clear encoder values
  def reset_encoders(self, reset):
    return self.write_pack(47, 'B', reset)

  def test_read8(self):
    self.read_unpack(0, 8, 'cccccccc')

  def test_write8(self):
    self.bus.write_i2c_block_data(20, 0, [0,0,0,0,0,0,0,0])
    time.sleep(0.0001)