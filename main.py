from flask import Flask, render_template, request, redirect, make_response, url_for
import os
import services.ETC as ETC
from forms import InputForm, CameraSelectForm, TelescopeSelectForm


# remove later
from wtforms import Form, SelectField, SubmitField
import numpy as np


app = Flask(__name__)

app.config['SECRET_KEY'] = 'd42c51f24733b869a5916a8c09043624'


# @app.route("/")
# def my_redirect():   
#     return redirect(url_for('/'))
    




@app.route('/', methods=['GET', 'POST'])
def test():
    
    in_form = InputForm()
    camera_select = CameraSelectForm()
    telescope_select = TelescopeSelectForm()
    
       
       
    #--- read camera preset data ---#
    camera_csv = open("./static/presets/camera_presets.csv", "+r")
    camera_presets = []
    
    # skip the instructions
    camera_csv.readline()
    camera_csv.readline()
    camera_csv.readline()
    
    for line in camera_csv:
        
        line = line.strip().split(":")
        name = line[0]
        values = line[1].split(',')
        
        if( len(values) == InputForm.camera_fields ):
            camera_presets.append( (name, values) )
    
    camera_csv.close()
    
    
    
    
     #--- read telescope preset data ---#
    telescope_csv = open("./static/presets/telescope_presets.csv", "+r")
    telescope_presets = []
    
    # skip the instructions
    telescope_csv.readline()
    telescope_csv.readline()
    telescope_csv.readline()
    
    for line in telescope_csv:
        
        line = line.strip().split(":")
        name = line[0]
        values = line[1].split(',')
        
        if( len(values) == InputForm.telescope_fields ):
            telescope_presets.append( (name, values) )
    
    telescope_csv.close()
    

    
    #--- read ... preset data ---#
    
    
    
    
    
    
        
    #--- fetch input data ---#
    
    
    # Used for input validation
    valid = True
    
    # detect if form has been submitted
    if in_form.submit.data:
            
        # check for valid input fields
        if in_form.validate():
        
            # retrieve form data
            data = request.form
            
            # create parameter tuple to be sent to the calculator script
            params = loadInput(data)
            
            
            #create instances of the calculator script classes
            cam = ETC.Camera(params[0])
            scope = ETC.Telescope(params[1])
            
            # create instance of calcualtor class
            etc = ETC.Calculator(cam, scope)
            
            print(str(etc))
            
            
            if os.path.exists("static/my_plot.png"):
                os.remove("static/my_plot.png")
            else:
                print("The file does not exist")


            #camera = ETC.camera(params)
            ETC.plot_light_curve_SB()
            #ETC.print_data(camera)

            return render_template('input.html', valid=valid, in_form=in_form, camera_select=camera_select, telescope_select=telescope_select,
                           camera_presets=camera_presets, telescope_presets=telescope_presets, plot_url = "static/my_plot.png")
            
            
        # An error message will be displayed in the HTML
        else: valid = False
            
        

    
    # returns HTML to be displayed
    return render_template('input.html', valid=valid, in_form=in_form, camera_select=camera_select, telescope_select=telescope_select,
                           camera_presets=camera_presets, telescope_presets=telescope_presets)





def loadInput(data: dict) -> tuple:


    camera_params = list()
    telescope_params = list()
    
    field = 0
    c_fields = InputForm.camera_fields
    t_fields = InputForm.telescope_fields
    
    
    for key in data:
        
        # skip first key, this is the 'csrf_token' and is not used for calculation
        
        if field > 0 and field <= c_fields:
            camera_params.append( float(data[key]) )
            
        elif field > c_fields and field <= c_fields + t_fields:
            telescope_params.append( float(data[key]) )
            
        field +=1
        
    
    print(camera_params)
    print(telescope_params)

    
    return (camera_params, telescope_params)






@app.route("/plot", methods = ['GET', 'POST'])
def get_plot():

    

        

    if os.path.exists("static/my_plot.png"):
        os.remove("static/my_plot.png")
    else:
        print("The file does not exist")


    #camera = ETC.camera(params)
    ETC.plot_light_curve_SB()
    #ETC.print_data(camera)


    return render_template('index.html', plot_url = "static/my_plot.png")







if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)