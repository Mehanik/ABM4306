#!/usr/bin/env python3
import serial

class ABM4306():
  """Communication with ABM-4306 using serial interface"""
  def __init__(self, port_name: str):
    self.port: str = port: str
    self.serial = serial.Serial()

