import os
import random
import time
from numba import jit
from threading import Thread
from math import e

class EstimatingEuler:
    def __init__(self):
        self.n = []

    @staticmethod
    @jit(nopython=True, nogil=True)
    def exceeds_one_static(trials_input: int = 1_000_000):
        n = []

        for _ in range(trials_input):
            s = 0
            i = 0  # Count the number of times random number added to s

            while s <= 1:  # If s smaller than one, continue to add random numbers
                s += random.random()
                i += 1
            n.append(i)
        return n

    def exceeds_one(self, trials_input):
        self.n = self.exceeds_one_static(trials_input)


    def show_estimation(self):
        estimation = sum(self.n) / len(self.n)
        return estimation


if __name__ == "__main__":
    start = time.time()
    trials_input = 50_000_000

    instance_array = []
    threads = []

    for k in range(os.cpu_count()):
        instance_array.append(EstimatingEuler())  # Creating multiple instances
        threads.append(Thread(target=instance_array[k].exceeds_one, args=(trials_input,)))  # Creating threads

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    n = []
    for instance in instance_array:
        n = instance.n

    estimated_e = sum(n) / len(n)

    end = time.time()
    print(f"ESTIMATED E: {estimated_e} | REAL E: {e} | ERROR: {((estimated_e-e)/e) * 100} ELAPSED TIME: {end - start}")
