from flask import Flask, render_template, request, jsonify
from src.model import run_simulation

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/submit", methods=["POST"])
def run_model():
    data = request.json
    NUM_EMPLOYEES = int(data.get("num_employees"))
    AVG_SUPPORT_TIME = int(data.get("avg_support_time"))
    CUSTOMER_INTERVAL = int(data.get("customer_interval"))
    SIM_TIME = int(data.get("sim_time"))
    PATIENCE = list(map(int, data.get("patience")))

    customer_handled, impatient_customers = run_simulation(num_employees=NUM_EMPLOYEES, 
                                                           avg_support_time=AVG_SUPPORT_TIME, 
                                                           customer_interval=CUSTOMER_INTERVAL,
                                                           sim_time=SIM_TIME, patience=PATIENCE)
    
    with open('call_center_log.log', 'r') as file:
        logs = file.read()

    return jsonify({"customer_handled": customer_handled, "impatient_customers": impatient_customers, "logs": logs})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)