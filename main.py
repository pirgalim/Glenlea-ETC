from flask import Flask, render_template, request, redirect, make_response, url_for
import os
import services.ETC as ETC
from forms import InputForm, CameraSelectForm, TelescopeSelectForm


# remove later
from wtforms import Form, SelectField, SubmitField

import numpy as np


app = Flask(__name__)

app.config['SECRET_KEY'] = 'd42c51f24733b869a5916a8c09043624'


@app.route("/")
def my_redirect():   
    return redirect(url_for('test'))
    


# class MyForm(Form):
#     camera = SelectField('Select Camera:', choices=[('', 'Custom'), ('asi6200mm', 'ASI6200MM'), ('asi2600mm', 'ASI2600MM')])

selected_option = ''
telescope_option = ''



@app.route('/test', methods=['GET', 'POST'])
def test():
    
    in_form = InputForm()
    camera_select = CameraSelectForm()
    telescope_select = TelescopeSelectForm()
    
       
       
    #--- read camera preset data ---#
    camera_csv = open("./static/presets/camera_presets.csv", "+r")
    camera_presets = []
    
    #skip the instructions
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
    
    
    
    
     #--- read camera preset data ---#
    telescope_csv = open("./static/presets/telescope_presets.csv", "+r")
    telescope_presets = []
    
    #skip the instructions
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
    
    
    
    
    #--- read telescope preset data ---#
    
    
    
    
    
    
        
      
    # need to somehow pull information from here
    if in_form.submit.data and in_form.validate():
            
            result = request.form
            #print(result)
            loadInput(result)
  
    #TODO handle valid tag
    return render_template('input.html', valid=True, in_form=in_form, camera_select=camera_select, telescope_select=telescope_select,
                           camera_presets=camera_presets, telescope_presets=telescope_presets)





def loadInput(result: dict) -> ETC:






    # camera data

    camera_params = list()
    telescope_params = list()
    
    field = 0
    
    c_fields = InputForm.camera_fields
    t_fields = InputForm.telescope_fields
    
    
    for key in result:
        
        
        # skip field = 0, this is the 'csrf_token' key
        
        if field > 0 and field <= c_fields:
            camera_params.append( float(result[key]) )
            
        elif field > c_fields and field <= c_fields + t_fields:
            telescope_params.append( float(result[key]) )
            
        field +=1
        
    
    print(camera_params)
    print(telescope_params)



    #camera_params = [r['sensor_x'], r['sensor_y'], r['px_size']]


    #[float(param) for param in camera_params]

    #list(np.float_(camera_params))


    print(camera_params[0]/7)

    #etc_camera = ETC.Camera(camera_params)

    





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)