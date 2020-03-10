from typing import Callable
import math

class Rail:
  name = "Rail"

  def __init_(self, fun: Callable, distance):
    self.fun = fun
    self.total_distance = distance
    
  def get(self, position: float):
    return self.fun(position)
