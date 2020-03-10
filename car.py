import math
from rail import Rail

class Car:
  def __init__(self, start_speed: float, name, start_time=0, accells=None):
    self.start_speed = start_speed
    self.name = name
    # Each element is a tuple containing the end position of the car after accelerating
    # and the acceleration of that car during that interval.
    self.accells = accells or [0,0.1] # [(ending_position, acceleration from current position to ending position)]
    self.accellsI = 0
    self.radius = 25
    self.start_time = start_time
  
