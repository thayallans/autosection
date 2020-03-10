import math
from rail import Rail


class Car:
    def __init__(self, start_speed: float, rail: Rail, name, start_time=0, accells=None):
        self.start_speed = start_speed
        self.rail = rail
        self.name = name
        # Each element is a tuple containing the end position of the car after accelerating
        # and the acceleration of that car during that interval.
        # [(ending_position, acceleration from current position to ending position)]
        self.accells = accells or [0, 0.1]
        self.accellsI = 0
        self.radius = 25
        self.start_time = start_time

    def get_locatio(self, time):
        """
        Returns the (x, y) location of the car at a certain time.
        """
        return self.rail.get(self.get_pos(time))

    def get_interval(self, time):
        """
        This takes a single time argument.
        This returns a bunch of internal information about the *start of the acceleration range the car is in at a given
        time*.
        This does *not* account for the car's position within the acceleration range.
        It returns: 
          the index of the range (or None if the car has passed out of all ranges, in which case it is assumed to have
            zero acceleration)
          the distance covered by the range
          the speed the car starts the range with
          the acceleration during the range
          the time the car has spent in the range
        """
        # if the current time is less than the start time then return nothing
        if time < self.start_time:
            return 0, 0, 0, 0, 0
            time -= self.start_time
            speed = self.start_speed
            accells = self.accells
            i = 0
            while True:
                if i == len(accells):
                    return None, 0, speed, 0, time
                a = accells[i][1]
                if i == 0:
                    d = accells[i][0]
                else:
                    d = accells[i][0] - accells[i - 1][0]
                inside_stuff = (speed**2 + 2*a*d)
                v2 = math.sqrt(inside_stuff)
                t = 2*d/(speed+v2)
                if t > time:
                    return i, d, speed, a, time
                else:
                    time -= t
                    speed = speed + a*t
                i += 1

    def get_pos(self, time):
      """
      This function takes a time and returns the scalar value of the car along its rail at that time.
      """
      if time < self.start_time:
          return 0
      i, d, speed, a, time = self.get_interval(time)
      if i is None:
          scalar = self.accells[-1][0]
      elif i > 0:
          scalar = self.accells[i-1][0]
      else:
          scalar = 0
      v2 = math.sqrt(speed ** 2 + 2 * a * d)
      scalar += (speed + v2) / 2 * time
      return scalar
