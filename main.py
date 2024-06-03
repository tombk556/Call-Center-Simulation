import random
import numpy as np
import simpy
import logging

# Time is in minutes!!!

NUM_EMPLOYEES = 2
AVG_SUPPORT_TIME = 5
CUSTOMER_INTERVAL = 3
SIM_TIME = 60

# Configure logging
LOGGING_ENABLED = True
if LOGGING_ENABLED:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CallCenterSimulator")

customer_handled = 0
impatient_customers = 0


def log_info(logger: logging.Logger = logger, text: str = ""):
    if LOGGING_ENABLED:
        logger.info(text)


def log_warning(logger: logging.Logger = logger, text: str = ""):
    logger.warning(text)


class CallCenter:
    def __init__(self, env: simpy.Environment, num_employees, avg_support_time):
        self.env = env
        self.staff = simpy.Resource(env, num_employees)
        self.avg_support_time = avg_support_time

    def support(self, customer):
        random_time = max(1, np.random.normal(self.avg_support_time, 4))
        yield self.env.timeout(random_time)
        log_info(text=f"Support finished for {customer} at {self.env.now:.2f}")


def customer(env: simpy.Environment, name, call_center: CallCenter):
    global customer_handled
    global impatient_customers
    patience = np.random.uniform(1, 3)
    arrival_time = env.now
    log_info(
        text=f"Customer {name} enters waiting queue at {env.now:.2f} with patience {patience:.2f} minutes")
    with call_center.staff.request() as request:
        results = yield request | env.timeout(patience)
        wait_time = env.now - arrival_time
        if request in results:
            log_info(
                text=f"Customer {name} enters call at {env.now:.2f} after waiting {wait_time:.2f} minutes")
            yield env.process(call_center.support(name))
            log_info(text=f"Customer {name} leaves call at {env.now:.2f}")
            customer_handled += 1
        else:
            log_warning(
                text=f"Customer {name} leaves queue after waiting more than {wait_time:.2f} minutes")
            impatient_customers += 1


def setup(env: simpy.Environment, num_employees, avg_support_time, customer_interval):
    call_center = CallCenter(env, num_employees, avg_support_time)

    for i in range(1, 6):
        env.process(customer(env, i, call_center))

    while True:
        yield env.timeout(random.randint(customer_interval - 1, customer_interval + 1))
        i += 1
        env.process(customer(env, i, call_center))


env = simpy.Environment()
env.process(setup(env, NUM_EMPLOYEES, AVG_SUPPORT_TIME, CUSTOMER_INTERVAL))
env.run(until=SIM_TIME)

print(f"Total customers handled: {customer_handled}")
print(f"Total impatient customers: {impatient_customers}")
