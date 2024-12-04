from threading import Timer, Semaphore
from random import random


INTERVAL_BOUNDS = (2, 15)
NUM_SPACES = 5
NUM_CARS = 10


def random_float(minimum: float, maximum: float) -> float:
    return minimum + random() * (maximum - minimum)


class ParkingSpace:
    def __init__(self, available_spaces: int):
        self.entry_gate = Semaphore(1)
        self.available_spaces = available_spaces


class Car:
    def __init__(self, uid, parking_space: ParkingSpace):
        self.uid = uid
        self.parking_space = parking_space
        Timer(random_float(*INTERVAL_BOUNDS), self.enter).start()

    def enter(self):
        with self.parking_space.entry_gate:
            if self.parking_space.available_spaces > 0:
                self.parking_space.available_spaces -= 1
                print(f"{self}:\tparked ({self.parking_space.available_spaces} spaces left)")
                Timer(random_float(*INTERVAL_BOUNDS), self.leave).start()
            else:
                print(f"{self}:\tparking space full")
                Timer(random_float(*INTERVAL_BOUNDS), self.enter).start()

    def leave(self):
        with self.parking_space.entry_gate:
            self.parking_space.available_spaces += 1
            print(f"{self}:\tleft   ({self.parking_space.available_spaces} spaces left)")
            Timer(random_float(*INTERVAL_BOUNDS), self.enter).start()

    def __repr__(self):
        return f"Car {self.uid}"


parking = ParkingSpace(NUM_SPACES)
for i in range(NUM_CARS):
    Car(i, parking)
