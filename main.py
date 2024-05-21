from flask import Flask, render_template, request, redirect, make_response, url_for
import os
import services.ETC as ETC
from forms import InputForm, CameraSelectForm, TelescopeSelectForm, FilterSelectForm, TargetSelectForm, ConditionsSelectForm


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
    
    
    #TODO remove file after generating
    
    if os.path.exists("static/my_plot.png"):
                os.remove("static/my_plot.png")
    else:
        print("The file does not exist")
    
    
    
    in_form = InputForm()
    camera_select = CameraSelectForm()
    telescope_select = TelescopeSelectForm()
    filter_select = FilterSelectForm()
    
    target_select = TargetSelectForm()
    conditions_select = ConditionsSelectForm()
    
   
    
    
    # #--- read preset data ---#
    presets = readPresets()
    
    #TODO: just pass presets[i] below instead
    camera_presets = presets[0]
    telescope_presets = presets[1]
    filter_presets = presets[2]
    target_presets = presets[3]
    
    
    
    
        
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
            
            
            # #create instances of the calculator script classes
            # cam = ETC.Camera(params[0])
            # scope = ETC.Telescope(params[1])
            
            # create instance of calcualtor class
            # etc = ETC.Calculator(cam, scope)
            
            # print(str(etc))
            
            
            
            #......
            etc = ETC.Calculator(params)
            etc.plot_light_curve_SB()
            
            
            


            #camera = ETC.camera(params)
            #ETC.plot_light_curve_SB()
            #ETC.print_data(camera)

            return render_template('input.html', valid=valid, in_form=in_form, 
                                   camera_select=camera_select, telescope_select=telescope_select, filter_select=filter_select, target_select=target_select, conditions_select=conditions_select,
                                    camera_presets=camera_presets, telescope_presets=telescope_presets, filter_presets=filter_presets, target_presets=target_presets,
                                    plot_url="static/my_plot.png")
            
            
        # An error message will be displayed in the HTML
        else: valid = False
            
        

    
    # returns HTML to be displayed
    return render_template('input.html', valid=valid, in_form=in_form, 
                           camera_select=camera_select, telescope_select=telescope_select, filter_select=filter_select, target_select=target_select, conditions_select=conditions_select,
                           camera_presets=camera_presets, telescope_presets=telescope_presets, filter_presets=filter_presets, target_presets=target_presets)





def readPresets() -> tuple:

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
    
    
    #--- read filter preset data ---#
    filter_csv = open("./static/presets/filter_presets.csv", "+r")
    filter_presets = []
    
    # skip the instructions
    filter_csv.readline()
    filter_csv.readline()
    filter_csv.readline()
    
    for line in filter_csv:
        
        line = line.strip().split(":")
        name = line[0]
        values = line[1].split(',')
        
        if( len(values) == InputForm.filter_fields ):
            filter_presets.append( (name, values) )
    
    filter_csv.close()
    
    
    #--- read target preset data ---#
    target_csv = open("./static/presets/target_presets.csv", "+r")
    target_presets = []
    
    # skip the instructions
    target_csv.readline()
    target_csv.readline()
    target_csv.readline()
    
    for line in target_csv:
        
        line = line.strip().split(":")
        name = line[0]
        values = line[1].split(',')
        
        if( len(values) == InputForm.target_fields ):
            target_presets.append( (name, values) )
    
    target_csv.close()    
    


    return (camera_presets, telescope_presets, filter_presets, target_presets)











def loadInput(data: dict) -> tuple:


    camera_params = list()
    telescope_params = list()
    filter_params = list()
    target_params = list()
    conditions_params = list()
    
    
    
    
    field = 0
    cam_fields = InputForm.camera_fields
    tel_fields = InputForm.telescope_fields
    fil_fields = InputForm.filter_fields
    tar_fields = InputForm.target_fields
    con_fields = InputForm.conditions_fields
    
    
    for key in data:
        
        # skip first key, this is the 'csrf_token' and is not used for calculation
        
        if field > 0 and field <= cam_fields:
            camera_params.append( float(data[key]) )
            
        elif field > cam_fields and field <= (cam_fields + tel_fields):
            telescope_params.append( float(data[key]) )
            
        elif field > (cam_fields + tel_fields) and field <= (cam_fields + tel_fields + fil_fields):
            filter_params.append( float(data[key]) )
            
        elif field > (cam_fields + tel_fields + fil_fields) and field <= (cam_fields + tel_fields + fil_fields + tar_fields):
            target_params.append( float(data[key]) )
            
        elif field > (cam_fields + tel_fields + fil_fields + tar_fields) and field <= (cam_fields + tel_fields + fil_fields + tar_fields + con_fields):
            conditions_params.append( float(data[key]) )
            
            
        field +=1
        
    
    print(camera_params)
    print(telescope_params)
    print(filter_params)
    print(target_params)
    print(conditions_params)

    
    return (camera_params, telescope_params, filter_params, target_params, conditions_params)






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