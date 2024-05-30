import random
import numpy as np
import simpy
import logging

# Time is in minutes!!!

NUM_EMPLOYEES = 3
AVG_SUPPORT_TIME = 5
CUSTOMER_INTERVAL = 2
SIM_TIME = 120

# Configure logging
LOGGING_ENABLED = False
if LOGGING_ENABLED:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('CallCenterSimulation')

customer_handled = 0

class CallCenter:
    def __init__(self, env: simpy.Environment, num_employees, avg_support_time):
        self.env = env
        self.staff = simpy.Resource(env, num_employees)
        self.avg_support_time = avg_support_time

    def support(self, customer):
        random_time = max(1, np.random.normal(self.avg_support_time, 4))
        yield self.env.timeout(random_time)
        if LOGGING_ENABLED:
            logger.info(f"Support finished for {customer} at {self.env.now:.2f}")

def customer(env: simpy.Environment, name, call_center: CallCenter):
    global customer_handled
    if LOGGING_ENABLED:
        logger.info(f"Customer {name} enters waiting queue at {env.now:.2f}")
    with call_center.staff.request() as request:
        yield request
        if LOGGING_ENABLED:
            logger.info(f"Customer {name} enters call at {env.now:.2f}")
        yield env.process(call_center.support(name))
        if LOGGING_ENABLED:
            logger.info(f"Customer {name} leaves call at {env.now:.2f}")
        customer_handled += 1

def setup(env: simpy.Environment, num_employees, avg_support_time, customer_interval):
    call_center = CallCenter(env, num_employees, avg_support_time)

    for i in range(1, 6):
        env.process(customer(env, i, call_center))

    while True:
        yield env.timeout(random.randint(customer_interval - 1, customer_interval + 1))
        i += 1
        env.process(customer(env, i, call_center))

    
for _ in range(100):
    env = simpy.Environment()
    env.process(setup(env, NUM_EMPLOYEES, AVG_SUPPORT_TIME, CUSTOMER_INTERVAL))
    env.run(until=SIM_TIME)

if LOGGING_ENABLED:
    logger.info(f"Customer handled on average: {customer_handled / 100}")
else:
    print(f"Customer handled on average at Call Center: {customer_handled / 100}")
