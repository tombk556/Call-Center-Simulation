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


NUM_CHECKOUT_AUTOMATES: int = 13
AMOUNT_OF_PRODUCTS: list = [1, 12]
AVG_SCAN_TIME: float = 0.2 # in minutes
PAY_TIME: list = [0.4, 0.8]
CUSTOMER_INTERVAL: int = 1

customer_handled = 0

class Rewe:
    def __init__(self, env: simpy.Environment, num_checkouts: int, avg_scan_time):
        self.env = env
        self.checkouts = simpy.Resource(env, capacity=num_checkouts)
        self.avg_scan_time = avg_scan_time
        
    def scan_buy(self, customer):
        random_time_to_scan_one_product = random.uniform(self.avg_scan_time - 0.1, 
                                                         self.avg_scan_time + 0.1)
        num_products = random.randint(AMOUNT_OF_PRODUCTS[0], AMOUNT_OF_PRODUCTS[1])
        time_to_buy = random.uniform(PAY_TIME[0], PAY_TIME[1])
        total_time = num_products * random_time_to_scan_one_product + time_to_buy
        
        yield self.env.timeout(total_time)
        
        print(f"Customer {customer} finished scanning and buying (products = {num_products}, time = {total_time:.2f}) at {self.env.now:.2f}")
        
def customer(env: simpy.Environment, name, rewe: Rewe):
    global customer_handled
    print(f"Customer {name} enters waiting queue at {env.now:.2f}")
    with rewe.checkouts.request() as request:
        yield request
        print(f"Customer {name} enters checkout at {env.now:.2f}")
        yield env.process(rewe.scan_buy(name))
        print(f"Customer {name} leaves checkout at {env.now:.2f}")
        customer_handled += 1
        
def setup(env: simpy.Environment, num_checkouts, avg_scan_time, customer_interval):
    rewe = Rewe(env, num_checkouts, avg_scan_time)
    
    for i in range(1, 6):
        env.process(customer(env, i, rewe))
        
    while True:
        yield env.timeout(random.randint(customer_interval - 1, customer_interval + 1))
        i += 1
        env.process(customer(env, i, rewe))

print("Rewe Self-Checkout Simulation")
env = simpy.Environment()
env.process(setup(env, num_checkouts=NUM_CHECKOUT_AUTOMATES, 
                  avg_scan_time=AVG_SCAN_TIME, 
                  customer_interval=CUSTOMER_INTERVAL))
env.run(until=60)
print("Customer handled: ", customer_handled)