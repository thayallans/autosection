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

    def firstCollision(self, cars):
        for i in range(len(cars) - 1):
            # This will contain the indices of the rails that self.rails[i]
            # will collide with.
            collision_car_indices = []
            car_1 = cars[i]
            for j in range(i + 1, len(cars)):
                car_2 = cars[j]
                if car_1.rail != car_2.rail:
                    if self.collisions_dict[car_1.rail][car_2.rail]:
                        for d in self.collisions_dict[car_1.rail][car_2.rail]:
                            collision_car_indices.append((j, d))

            collision_car_indices.sort(key=lambda x: x[1])

            for j, _ in collision_car_indices:
                car_2 = cars[j]
                collision_time = self.collision(car_1, car_2)
                if collision_time >= 0:
                    print("Coll between", car_1, car_2)
                    return i, j, collision_time

        return None

    def update(self):
        """
        iterate and check with all other cars, handle() at first coll.
        """
        queue = [self.cars]
        while len(queue) > 0:
            cars = queue.pop(0)
            #print("C", cars)
            # i = Intersection(cars, self.rails, False)
            # real_actual_view = ZipperView(intersection=i,
            #                               window_size=(800, 600),
            #                               x_lanes=2,
            #                               y_lanes=2)
            # while not real_actual_view.quitting:
            #     real_actual_view.tick()
            res = self.firstCollision(cars)
            if res is None:
                self.cars = cars
                return
            i, j, time = res
            try:
                a, d = self.handleA(cars[i], cars[j], time)
                res = cars.copy()
                res[i] = a
                res[j] = d
                #print("A", res)
                queue.append(res)
            except ValueError:
                print("VE")
                pass
            try:
                a, d = self.handleA(cars[j], cars[i], time)
                res = cars.copy()
                res[j] = a
                res[i] = d
                #print("A", res)
                queue.append(res)
            except ValueError:
                print("VE")
                pass
            try:
                a, d = self.handleD(cars[i], cars[j], time)
                res = cars.copy()
                res[i] = a
                res[j] = d
                #print("A", res)
                queue.append(res)
            except ValueError:
                print("VE")
                pass
            try:
                a, d = self.handleD(cars[j], cars[i], time)
                res = cars.copy()
                res[j] = a
                res[i] = d
                #print("A", res)
                queue.append(res)
            except ValueError:
                print("VE")
                pass

    def handleA(self, carA, carD, time):
        """
        This function stops two cars from colliding.
        carA is the car to accelerate
        carD is the car to decelerate
        time is the time of the collision

        It works by first changing carAs last acceleration (before the collision) so it arrives on the intersection at
        the time.
        Next it iteratively slows carD until they do not hit at the intersection.

        TODO:
        This should then call update with the changed cars in order to propagate the changes.
        It should return the total amount of speed changes so its parent update can optimize which car slows
        down / speeds up.
        """

        didSomething = False

        i, dist, speed, a, dt = carA.get_interval(time)
        a2 = a
        newA = carA.copy()
        if i is not None:
            didSomething = True
            while a2 < max_acceleration and self.collision(carD, newA) != -1:
                a2 += 0.01
                for j in range(i, -1, -1):
                    if newA.accellsI <= j:
                        newA.accells[j] = (newA.accells[j][0], a2)
            newA.accellsI = i
        # print(newA)

        newD = carD.copy()
        #print(newD, time)
        i, dist, speed, a, dt = newD.get_interval(time)
        if i is not None:
            didSomething = True
            a2 = a
            while a2 >= -max_acceleration:
                newD.accells[i] = (newD.accells[i][0], a2)
                if self.collision(newD, newA) == -1:
                    break
                a2 -= 0.01

        if not didSomething:
            raise ValueError("Didn't do anything.")
        print("got cars:", newA, newD)

        return newA, newD

    def handleD(self, carA, carD, time):
        """
        This function stops two cars from colliding.
        carA is the car to accelerate
        carD is the car to decelerate
        time is the time of the collision

        It works by first changing carAs last acceleration (before the collision) so it arrives on the intersection at
        the time.
        Next it iteratively slows carD until they do not hit at the intersection.

        TODO:
        This should then call update with the changed cars in order to propagate the changes.
        It should return the total amount of speed changes so its parent update can optimize which car slows
        down / speeds up.
        """

        didSomething = False

        i, dist, speed, a, dt = carD.get_interval(time)
        a2 = a
        newD = carD.copy()
        if i is not None:
            didSomething = True
            while a2 >= -max_acceleration and self.collision(newD, carA) != -1:
                a2 -= 0.001
                for j in range(i, -1, -1):
                    if newD.accellsI <= j:
                        newD.accells[j] = (newD.accells[j][0], a2)
            newD.accellsI = i

        newA = carA.copy()
        i, dist, speed, a, dt = newA.get_interval(time)
        if i is not None:
            didSomething = True
            a2 = a
            while a2 < max_acceleration:
                newA.accells[i] = (newA.accells[i][0], a2)
                if self.collision(newD, newA) == -1:
                    break
                a2 += 0.001

        if not didSomething:
            raise ValueError("Didn't do anything.")
        print("got cars:", newA, newD)

        return newA, newD
