import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request
from simulations import sim1_mendelian, sim2_es_bitflip, sim3_es_gaussian, sim3_es_gaussian_optimized

app = Flask(__name__)

SIMULATIONS = {
    "sim1": sim1_mendelian.run,
    "sim2": sim2_es_bitflip.run,
    "sim3": sim3_es_gaussian.run,
    "sim3_optimized": sim3_es_gaussian_optimized.run
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        model = request.form.get("model")
        generations = int(request.form.get("generations"))
        SIMULATIONS[model](generations=generations)
        result = f"✅ Model '{model}' ran for {generations} generations."
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
