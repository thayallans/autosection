from typing import List, Tuple
import math

from car import Car, max_acceleration
from rail import Rail


class Intersection:
    def __init__(self, cars: List[Car], rails: List[Rail], clCars=True, cl=None):
        self.cars = cars
        self.rails = rails
        self.collisions_dict = cl or {}
        if not cl:
            self.init_collisions_dict()
            if clCars:
                self.split(self.cars)
    
    def init_collisions_dict(self):
        """
        Initializes the dictionary of collsion points between
        rails, setting each value to None.
        """
        for rail_a in self.rails:
            self.collisions_dict[rail_a] = {}
            for rail_b in self.rails:
                if rail_a != rail_b:
                    self.collisions_dict[rail_a][rail_b] = []
        
        for rail_a in self.rails:
            for rail_b in self.rails:
                if rail_a != rail_b:
                    if self.collisions_dict[rail_a][rail_b]:
                        # We have already filled in this dictionary entry
                        continue
                    ints = self.find_intersection(rail_a, rail_b)
                    for a, b in ints:
                        # if the rails don't colide, the dictionary value stays at 0.
                        self.collisions_dict[rail_a][rail_b].append(a)
                        self.collisions_dict[rail_b][rail_a].append(b)
    
    def split(self, cars):
        for car in cars:
            for rail_b, ds in self.collisions_dict[car.rail].items():
                if ds is not None:
                    for d in ds:
                        car.accells.append((d, 0.1))
            car.accells.sort(key=lambda x: x[0])
    
    
