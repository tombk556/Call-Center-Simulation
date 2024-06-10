from src.model import run_simulation


NUM_EMPLOYEES = 5
AVG_SUPPORT_TIME = 5
CUSTOMER_INTERVAL = 1
SIM_TIME = 8 * 60
PATIENCE = [1, 3]

#### ---------- Example 1: Single Mode ---------- ####

customer_handled, impatient_customers = run_simulation(num_employees=NUM_EMPLOYEES, 
                                                       avg_support_time=AVG_SUPPORT_TIME, 
                                                       customer_interval=CUSTOMER_INTERVAL,
                                                       sim_time=SIM_TIME, patience=PATIENCE,
                                                       enable_terminal_logging=True,
                                                       time_factor=0.5)
print("------ Example 1: Single Mode ------")
print(f"Customer handled: {customer_handled}")
print(f"Impatient customers: {impatient_customers} \n")

sum_handled_customers = []
sum_impatient_customers = []

#### ---------- Example 2: Experiment Mode ---------- ####
for _ in range(20):
    customer_handled, impatient_customers = run_simulation(num_employees=NUM_EMPLOYEES, 
                                                       avg_support_time=AVG_SUPPORT_TIME, 
                                                       customer_interval=CUSTOMER_INTERVAL,
                                                       sim_time=SIM_TIME, patience=PATIENCE)
    sum_handled_customers.append(customer_handled)
    sum_impatient_customers.append(impatient_customers)
print("------ Example 2: Experiment Mode ------")
print(f"Average customer handled: {sum(sum_handled_customers) / len(sum_handled_customers)}")
print(f"Average impatient customers: {sum(sum_impatient_customers) / len(sum_impatient_customers)}")