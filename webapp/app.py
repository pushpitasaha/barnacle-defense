import matplotlib
#non-GUI backend for flask render
matplotlib.use('Agg') 

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request
from simulations import sim1_mendelian, sim2_es_bitflip, sim3_es_gaussian, sim3_es_gaussian_optimized, sim4_within_patch, sim5_nearest_neighbor
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

SIMULATIONS = {
    "sim1": sim1_mendelian.run,
    "sim2": sim2_es_bitflip.run,
    "sim3": sim3_es_gaussian.run,
    "sim3_optimized": sim3_es_gaussian_optimized.run,
    "sim4": sim4_within_patch.run,
    "sim5": sim5_nearest_neighbor.run
}

# create plot as base64 string to embed in HTML
def generate_plot(metrics):
    fig, ax = plt.subplots()
    ax.plot(metrics)
    ax.set_title("% Bent Morphs Over Generations")
    ax.set_xlabel("Generation")
    ax.set_ylabel("% Bent")
    fig.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_bytes = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return img_bytes

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    plot_url = None
    if request.method == "POST":
        model = request.form.get("model")
        generations = int(request.form.get("generations"))

        progress = []

        def track_callback(value):
            progress.append(value)

        SIMULATIONS[model](generations=generations, track_callback=track_callback)
        result = f"✅ Model '{model}' ran for {generations} generations."

        plot_url = generate_plot(progress)

    return render_template("index.html", result=result, plot_url=plot_url)

if __name__ == "__main__":
    app.run(debug=True)
