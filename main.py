from flask import Flask, render_template, request
import os
import services.ETC as ETC
import services.scrape_sqm as sqm
from forms import InputForm, SelectForm

import pyckles


# Flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'd42c51f24733b869a5916a8c09043624'


@app.route('/', methods=['GET', 'POST'])
def calculator():
    
    
    #pickles
    pickles()
    
    #TODO remove file after generating
    
    if os.path.exists("static/plot_light_curve_SB.png"):
                os.remove("static/plot_light_curve_SB.png")

    if os.path.exists("static/spread_counts.png"):
                os.remove("static/spread_counts.png")
    
    # create forms
    in_form = InputForm()
    select_form = SelectForm()
    # Used for input validation message
    valid = True
      
    #load presets from templates
    camera_presets = readPresets("camera")
    telescope_presets = readPresets("telescope")
    filter_presets = readPresets("filter")
    # target_presets = readPresets("target")
    
    target_presets = pickles()
        
    # retrieve current GAO SQM value
    gao_sqm = sqm.get_sqm()   
    
    # detect if form has been submitted
    if in_form.submit.data:
            
        # check for valid input fields
        if in_form.validate():
        
            # retrieve form data
            data = request.form
            
            
            #TODO testing
            # print(data)
            
            params = process_input(data)
            
            
            
            
            # create parameter tuple to be sent to the calculator script
            # params = readInput(data)
                        
            # validate number of parameters
            if(params is None):
                return render_template("error.html", message="There is a problem with the number of parameters being passed from the form to the script.")
            
            else:
                # create instances of the calculator script classes
                etc = ETC.Calculator(params)
                
                error = etc.validate()
                
                # validate some parameters                
                if error == None:
                
                    # plot... TODO
                    etc.plot_light_curve_SB()
                    
                    # output values displayed in HTML
                    peak, minimum = etc.aperture()    
                    fov = int( etc.computeFOV() )            
                    counts = etc.countsPerSecond()
                    exposure = etc.calculateReqTime(1) #TODO what is the 1???
                    
                    # use this for file output
                    # print(params) 
                    
                    # render output template
                    return render_template('output_v2.html', valid=valid, in_form=in_form, select_form=select_form,
                                            camera_presets=camera_presets, telescope_presets=telescope_presets, filter_presets=filter_presets, target_presets=target_presets, 
                                            gao_sqm=gao_sqm,
                                            SB_url="static/plot_light_curve_SB.png", counts_url="static/spread_counts.png",
                                            fov=fov, counts=counts, peak=peak, minimum=minimum, exposure=exposure, error=None)
                
                else: 
                    # display error in HTML
                    return render_template('input.html', valid=False, in_form=in_form, select_form=select_form,
                           camera_presets=camera_presets, telescope_presets=telescope_presets, filter_presets=filter_presets, target_presets=target_presets,
                           gao_sqm=gao_sqm, error=error)
                
        # An error message will be displayed in the HTML
        else: valid = False
                
    # render HTML to be displayed
    return render_template('input.html', valid=valid, in_form=in_form, select_form=select_form,
                           camera_presets=camera_presets, telescope_presets=telescope_presets, filter_presets=filter_presets, target_presets=target_presets,
                           gao_sqm=gao_sqm, error="Invalid Parameter(s) Below - Must Be Numeric (0 - 100,000)")



def readPresets(file_name: str) -> list:
    """    
    Read data from template csv files
    
    Args:
        file_name (str): name of parameter category (i.e. 'camera', 'telescope', etc.)

    Returns:
        list: parameters from template
        None: error reading template
    """
    
    try:
        csv = open("./static/presets/" + file_name + "_presets.csv", "+r")
        presets = []
        
        # skip the preset template instructions
        csv.readline()
        csv.readline()
        csv.readline()
        
        # iterate through lines in file
        for line in csv:
            
            line = line.strip().split(":")
            name = line[0]
            values = line[1].split(',')
            
            # validate parameter count 
            if( len(values) == InputForm.fields[file_name] ):
                presets.append( (name, values) )
        
        csv.close()
        return presets
    
    except: return None



def readInput(input: dict) -> list:
    """
    Copies dictionary data into a list while omitting 'csrf_token' and 'submit' keys

    Args:
        input (dict): dictionary of data to be copied

    Returns:
        list: data from dictionary
        None: length of parameters does not match what is expected
    """
    
    
    # print(input)
    
    # data list
    data = []
    
    # read dict to data list
    for val in input.values():
        
        # ignore non-data parameters
        if val != input["csrf_token"] and  val != input["submit"]:

            try:
                data.append( float(val) )
            except:
                data.append(val)

    # validate length of data list
    if len(data) != InputForm.total_fields: #TODO update this
        return None
    
    return data
    
    
    
def process_input(input: dict) -> dict:
    
    print(len(input))
    
    params = {}
    
    for key in input:
        
        if key != "csrf_token" and key != "submit":
            
            try:
               
                params[key] = float( input[key] )
                
                
            except:
                params[key] = input[key]
            
            print(key, params[key])
            
    
    print(params)
    
    return params
    
        
    
    
    
    
    


    
def pickles(): 
    
    file = open("./static/presets/pickles.csv")
    presets = []
    
    for line in file:    
        csvs = line.strip().split(",")
        
        
        presets.append( (csvs[1], [csvs[2]]) )
        
    file.close()
    return presets
        
    



if __name__ == '__main__':

    app.run(host='0.0.0.0', port=3000)