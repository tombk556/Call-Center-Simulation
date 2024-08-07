"""Tom Bischopink © - HTWD 2024"""
import random
import numpy as np
import simpy
import logging
from simpy.rt import RealtimeEnvironment
import os


# Basic configuration for the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Call Center Simulator")
logger.propagate = False

# File handler setup
file_handler = logging.FileHandler("call_center_log.log", mode="w")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Stream handler setup (for terminal output)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

def log_info(logger: logging.Logger = logger, text: str = ""):
    logger.info(text)


def log_warning(logger: logging.Logger = logger, text: str = ""):
    logger.warning(text)


class CallCenter:
    def __init__(self, env: simpy.Environment, num_employees, avg_support_time):
        self.env = env
        self.staff = simpy.Resource(env, num_employees)
        self.avg_support_time = avg_support_time

    def support(self, customer):
        random_time = abs(np.random.normal(self.avg_support_time, self.avg_support_time / 10))
        yield self.env.timeout(random_time)
        log_info(text=f"Support finished for {customer} at {self.env.now:.2f}")


def customer(env: simpy.Environment, name, call_center: CallCenter, patience: list):
    global customer_handled
    global impatient_customers
    middle = (patience[0] + patience[1]) / 2
    random_patience = abs(np.random.normal(middle, middle/ 10))
    arrival_time = env.now
    log_info(text=f"Customer {name} enters waiting queue at {env.now:.2f} with patience {random_patience:.2f} minutes")
    with call_center.staff.request() as request:
        results = yield request | env.timeout(random_patience)
        wait_time = env.now - arrival_time
        if request in results:
            log_info(text=f"Customer {name} enters call at {env.now:.2f} after waiting {wait_time:.2f} minutes")
            yield env.process(call_center.support(name))
            log_info(text=f"Customer {name} leaves call at {env.now:.2f}")
            customer_handled += 1
        else:
            log_warning(text=f"Customer {name} leaves queue after at {env.now:.2f} waiting more than {wait_time:.2f} minutes")
            impatient_customers += 1


def setup(env: simpy.Environment, num_employees, avg_support_time, customer_interval, patience):
    call_center = CallCenter(env, num_employees, avg_support_time)

    for i in range(1, 6):
        env.process(customer(env, i, call_center, patience))

    while True:
        yield env.timeout(random.randint(customer_interval - 1, customer_interval + 1))
        i += 1
        env.process(customer(env, i, call_center, patience))


def run_simulation(num_employees: int, avg_support_time: int,
                   customer_interval: int, patience: list, sim_time: int, 
                   enable_terminal_logging: bool = False, time_factor: int = 0):
    global customer_handled
    global impatient_customers
    
    if enable_terminal_logging:
        logger.addHandler(stream_handler)
    else:
        logger.removeHandler(stream_handler)
        
    customer_handled = 0
    impatient_customers = 0
    
    file_handler.close()
    os.remove("call_center_log.log")

    env = RealtimeEnvironment(factor=time_factor, strict=False)
    env.process(setup(env, num_employees, avg_support_time,
                customer_interval, patience))
    env.run(until=sim_time)
    log_info(text=f"Simulation Results: {customer_handled} customers handled, {impatient_customers} impatient customers")
    return customer_handled, impatient_customers