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
    self.ser.timeout = 0.6

    self.__last_val = None
    self.__data_receivrd = threading.Event()
    self.__stop_request = threading.Event()
    self.__is_opened = False

  def open(self):
    if (not self.__is_opened):
      self.__is_opened = True
      self.ser.open()
      self.__stop_request.clear()
      self.__t = threading.Thread(target=self.__RcvData)
      self.__t.daemon = True
      self.__t.start()
    else:
      raise ABM4306Exception("Device is already open.")

  def close(self):
    if (self.__is_opened):
      self.__is_opened = False
      self.__stop_request.set()
      #self.__t.join()
      self.ser.close()
    else:
      raise ABM4306Exception("Device is not open.")

  def ReadValue(self):
    if (not self.__is_opened):
      raise ABM4306Exception("Device is not open.")
    self.__data_receivrd.clear()
    self.__data_receivrd.wait()
    return self.__last_val

  def __Bytes2Float(self, data: bytes):
    """Decode data received from multimeter"""
    s = data.decode('UTF-8')
    s = s[:-2]
    f = float(s)
    return f

  def __RcvData(self):
    while(not self.__stop_request.isSet()):
      try:
        d = self.ser.readline()
        v = self.__Bytes2Float(d)
      except:
        v = None
      finally:
        self.__last_val = v
        self.__data_receivrd.set()


class ABM4306Exception(RuntimeError):
  pass
