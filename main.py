from flask import Flask
from flask import render_template
from flask import request

# import matplotlib
# import matplotlib.pyplot as plt 




# import services.test as test
# import services.ETC as ETC





# currently rewriting Jupyter file
import matplotlib.pyplot as plt
import scipy.constants
plt.style.use('seaborn-poster')
import matplotlib.patches as patches
import scipy
import numpy as np
import math



# import base64
# from io import BytesIO
# from matplotlib.figure import Figure

#from flask import Response
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

#import numpy as np





app = Flask(__name__)



@app.route("/")
def hello():
    return render_template('index.html')



@app.route("/get_plot", methods = ['GET', 'POST'])
def get_plot():
    if request.method == "POST":
        
        params = [request.form['sen_x'], request.form['sen_y'], request.form['px_size'], request.form['q_eff'], request.form['read_noise'],
                  request.form['gain'], request.form['dark_noise'], request.form['full_well']]
    
        
        #ETC.plot_light_curve_SB()
        
        
        
        return render_template('index.html')
    
    else:
        return render_template('index.html')
        
        
        
        # sen_x = request.form['sen_x']
        # sen_y = request.form['sen_y']
        # px_size = request.form['px_size']
        # q_eff = request.form['q_eff']
        # read_noise = request.form['read_noise']
        # gain = request.form['gain']
        # sen_offset = request.form['sen_offset']
        # dark_noise = request.form['dark_noise']
        # full_well = request.form['full_well']
        

    
        















@app.route("/script")
def dynamic_page():
    
    text = test.run()
    
    return text + 'ttt'



@app.route("/figure")
def plot_png():
    
    data = test.run()
    return render_template('main.html') + f"<img src='data:image/png;base64,{data}'/>"









@app.route("/hello")
def run():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)