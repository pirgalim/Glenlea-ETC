from flask import Flask
from flask import render_template
from flask import request
from flask import make_response

import os
import services.ETC as ETC



app = Flask(__name__)



@app.route("/")
def index():
    
    resp = make_response(render_template('index.html'))
    
    if os.path.exists("static/my_plot.png"):
        os.remove("static/my_plot.png")
        
        return resp
    else:
        print("The file does not exist")

    return resp




@app.route("/autofill",  methods = ['GET', 'POST'])
def fill():
    if request.method == "POST":
        
        data = request.form
        
        print("The data: ")
        print(data)
         
        return render_template('index.html')
    
    else: 
        render_template('index.html')






@app.route("/plot", methods = ['GET', 'POST'])
def get_plot():
    
    if request.method == "POST":
        
        params = [request.form['sen_x'], request.form['sen_y'], request.form['px_size'], request.form['q_eff'], request.form['read_noise'],
                  request.form['gain'], request.form['dark_noise'], request.form['full_well']]

        
        
        if os.path.exists("static/my_plot.png"):
            os.remove("static/my_plot.png")
        else:
            print("The file does not exist")
        
        ETC.plot_light_curve_SB()

        
        return render_template('index.html', plot_url = "static/my_plot.png")
    
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
        

    


@app.route("/hello")
def run():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)