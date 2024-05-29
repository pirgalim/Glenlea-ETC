from flask import Flask, render_template, request, redirect, make_response, url_for
import os
import services.ETC as ETC
from forms import InputForm, SelectForm



# Flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'd42c51f24733b869a5916a8c09043624'



@app.route('/', methods=['GET', 'POST'])
def calculator():
    
    #TODO remove file after generating
    
    if os.path.exists("static/plot_light_curve_SB.png"):
                os.remove("static/plot_light_curve_SB.png")
    else:
        print("The file does not exist")
        
    if os.path.exists("static/spread_counts.png"):
                os.remove("static/spread_counts.png")
    else:
        print("The file does not exist")
    
    
    # create forms
    in_form = InputForm()
    select_form = SelectForm()
  
    
    #--- read preset data ---#
    presets = readPresets()
    
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
            
            if(params is None):
                return render_template("error.html")
            
            else:
                        
                # create instances of the calculator script classes
                etc = ETC.Calculator(params)
                etc.plot_light_curve_SB()
                peak, minimum = etc.aperture()
                                
                fov = int( etc.computeFOV() )            
                counts = etc.countsPerSecond()
                
                
                ref_SNR = etc.SNR_ref()
                print(ref_SNR)
                
                desired_SNR = 250
                exposure =  etc.calculateReqTime(desired_SNR, ref_SNR, 1)
                
                
                #return(render_template('output.html', plot_url="static/my_plot.png"))
                return render_template('output.html', valid=valid, in_form=in_form, select_form=select_form,
                                        camera_presets=presets, telescope_presets=telescope_presets, filter_presets=filter_presets, target_presets=target_presets,
                                        SB_url="static/plot_light_curve_SB.png", counts_url="static/spread_counts.png",
                                        fov=fov, counts=counts, peak=peak, minimum=minimum, exposure=exposure)
                
            
        # An error message will be displayed in the HTML
        else: valid = False
            
        

    
    # returns HTML to be displayed
    return render_template('input.html', valid=valid, in_form=in_form, select_form=select_form,
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


    camera_params = []
    telescope_params = []
    filter_params = []
    target_params = []
    conditions_params = []
        
    field = 0
    cam_fields = InputForm.camera_fields
    tel_fields = InputForm.telescope_fields
    fil_fields = InputForm.filter_fields
    tar_fields = InputForm.target_fields
    con_fields = InputForm.conditions_fields
    
    
    try:
    
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
            
        return (camera_params, telescope_params, filter_params, target_params, conditions_params)

    except:
        print("oops")
        return None
   
        




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)