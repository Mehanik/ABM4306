#!/usr/bin/env python3
import serial
import threading

class ABM4306():
  """Read data from Aktakom ABM-4306 using serial interface

  RS-232 "Print" mode must be enabled,
  Shift -> Setup -> Shift -> Lo -> Lo -> Lo -> Lo -> Lo -> Hold -> Shift -> 2nd -> 2nd
  """


  def __init__(self, port_name: str = None, baudrate: int = 9600):
    """port_name -- for example '/dev/ttyS0'"""
    self.ser = serial.Serial()
    self.ser.port = port_name
    self.ser.baudrate = baudrate
    self.ser.open()

    self.__last_val = None
    self.__data_receivrd = threading.Event()

    self.__t = threading.Thread(target=self.__RcvData)
    self.__t.start()

  def ReadValue(self):
    self.__data_receivrd.clear()
    self.__data_receivrd.wait()
    return self.__last_val

  def __Bytes2Float(self, data: bytes):
    """Decode data received from multimeter"""
    s = data.decode('UTF-8')
    s = s[:-2]
    return float(s)

  def __RcvData(self):
    while(1):
      try:
        d = self.ser.readline()
        v = self.__Bytes2Float(d)
      except:
        v = None
      finally:
        self.__last_val = v
        self.__data_receivrd.set()
