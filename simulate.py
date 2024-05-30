# Simulation des Rewe Selbstbedienungssystems

# Ziel : Wartezeit der Kunden in der Schlange zu minimieren

# Prozesse:
# 1. Kunde kommt an mit n (U~(1,12)) Produkten
# 2. Kunde geht zu einem freien Selbstbedienungssystems (8 Stück)
# 3. Kunde scannt die Produkte, pro Produkt dauert es 1-3 Sekunden (U~(1,3))
# 4. Kunde bezahlt und packt seine Sachen, dauert 5-10 Sekunden (U~(5,10))
# 5. Kunde verlässt das System und geht weg

import simpy
import random
import numpy as np


NUM_CHECKOUT_AUTOMATES: int = 8
AMOUNT_OF_PRODUCTS: list = [1, 12]
SCAN_TIME: list = [1, 3]
PAY_TIME: list = [5, 10]
CUSTOMER_INTERVAL: int = 8


class Rewe:
    def __init__(self, env, num_checkouts: int, scan_time: list, pay_time: list):
        self.env = env
        self.num_checkouts = simpy.Resource(env, capacity=num_checkouts)
        self.scan_time = scan_time
        self.pay_time = pay_time
        
    def scan(self, customer):
        random_time = random.randint(SCAN_TIME[0], SCAN_TIME[1])