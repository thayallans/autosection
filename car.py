import math
from rail import Rail

max_acceleration = 1


class Car:
    def __init__(self, start_speed: float, rail: Rail, name, start_time=0, accells=None):
        self.start_speed = start_speed
        self.rail = rail
        self.name = name
        # Each element is a tuple containing the end position of the car (i.e. when the car changes its acceleration),
        # and the acceleration of the car during that interval.
        self.accells = accells or [(self.rail.total_distance, 0.1)] # [(ending_position, acceleration from current position to ending position)]
        self.accellsI = 0
        self.radius = 25   # TODO:  Change this if necessary
        self.start_time = start_time
## got up to here
    def get_location(self, time):
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
            # if you've looped through all the accells, just return nullesque info
            if i == len(accells):
                return None, 0, speed, 0, time
            # acceleration of the car during an interval
            a = accells[i][1]
            #calculating distance to travel with the acceleration calculated above
            if i == 0:
                # if looping through first value in accels list then make distance to travel the end position
                # because it would be going from 0 to end position so the distance travelled is just the end position
                d = accells[i][0]
            else:
                # else if any other indice other than the first, just subtract hte last end position from the current end 
                # position. So like if the current end position is 200 and the previous was 100. Then 200 - 100 would be the 
                # distance to travel at the current acceleration
                d = accells[i][0] - accells[i - 1][0]
            inside_stuff = (speed**2 + 2 * a * d) # inside_stuff = speed^2 + 2*current_acceleration*distance_to_travel
            # calculating final velocity here
            v2 = math.sqrt(inside_stuff)
            # rearrange kinematic equations ot calculate for time
            t = 2 * d / (speed + v2)
            # if time to perform acceleration is greater than time left then return information
            # time is time left ??
            if t > time:
                return i, d, speed, a, time
            else:
                # if time for acceleration is less than the time left, subtract time for acceleration from time left
                time -= t
                # set current speed to previous final speed since the action has already been performe
                # first kinematic formula
                speed = speed + a * t
            # add 1 and move onto the next indice
            i += 1

    def get_pos(self, time):
        """
        This function takes a time and returns the scalar value of the car along its rail at that time.
        """
        # if time for some reason is less than the start time then the car hasn't moved so return 0
        if time < self.start_time:
            return 0
        # With current time left call method get_interval to get more information
        i, d, speed, a, time = self.get_interval(time)
        if i is None:
            # will return null if current indice is none (non existent)
            scalar = self.accells[-1][0]
        elif i > 0:
            # will return the last position
            scalar = self.accells[i - 1][0]
        else:
            # car hasn't move yet so set position to 0
            scalar = 0
        # calculate the final velocity
        v2 = math.sqrt(speed**2 + 2 * a * d)
        # Current position + distance travelled = new current position
        scalar += (speed + v2) / 2 * time
        # return current position
        return scalar

    def get_time(self):
        """
        This function returns the time at which the car has completed all of its acceleration ranges, and is 
        assumed to be cruising at a constant velocity after leaving the intersection.
        """
        time = self.start_time
        speed = self.start_speed
        oldD = 0
        # Go through all values in accells list and calculate time to go through intersection
        for d, a in self.accells:
            d -= oldD
            v2 = math.sqrt(speed**2 + 2 * a * d)
            t = 2 * d / (speed + v2)
            time += t
            speed = v2
        return time

    def copy(self):
        """
        This copies a car
        """
        return Car(self.start_speed, self.rail, self.name, start_time=self.start_time, accells=self.accells.copy())

    def __repr__(self):
        res = self.name + "[("
        for d, a in self.accells:
            res += str(round(d)) + "," + str(a) + ")("
        return res + "]"
