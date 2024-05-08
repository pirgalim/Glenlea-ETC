from flask import Flask
from flask import render_template

import test



import base64
from io import BytesIO
from matplotlib.figure import Figure

from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import numpy as np



app = Flask(__name__)




@app.route("/")
def index():
    return 'Index Page'

@app.route("/script")
def dynamic_page():
    
    text = test.run()
    
    return text + 'ttt'



@app.route("/figure")
def plot_png():
    
   
    
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1,2])
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template('main.html') + f"<img src='data:image/png;base64,{data}'/>" + render_template('main.html')



@app.route("/hello")
def run():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)