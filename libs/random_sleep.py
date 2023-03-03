from time import sleep
import random

RANGE = 3
def random_sleep(min):
    sleep(random.randint(min, min + RANGE))