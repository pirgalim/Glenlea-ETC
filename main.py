from flask import Flask, render_template, request
import os
# import services.ETC_old as ETC_old

import services.etc as etc
# import services.counts as cts
import services.observation as observation

import services.scrape_sqm as sqm
from forms import InputForm, SelectForm

import numpy as np


# Flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'd42c51f24733b869a5916a8c09043624'



OMIT_KEY = "   01.  "



@app.route('/', methods=['GET', 'POST'])
def calculator():
    
    
    #pickles
    # pickles()
    
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
            
            print("----------\nmain section:\n-------------")
            print(params)
            
            
            
            # create parameter tuple to be sent to the calculator script
            # params = readInput(data)
                        
            # validate number of parameters
            if(params is None):
                return render_template("error.html", message="There is a problem with the number of parameters being passed from the form to the script.")
            
            else:
                # create instances of the calculator script classes
                # etc = ETC.Calculator(params)
                # error = etc.validate()
                
                obs = observation.Observation(params)
                
                # error = etc.validate(obs)
                error = None #TODO
                
                # validate some parameters                
                if error == None:
                
                    # plot... TODO
                    # etc.plot_light_curve_SB()
                    
                    test_exposure = 1  # seconds
         
                    counts = etc.calc_counts(obs)
                    
                    signal_values = etc.spreadCounts(obs, counts, 1)
                    noise_values = etc.generateNoise(obs ,test_exposure)
                    bg_values = etc.generateBG_TEST(obs)
                    
                    final_sensor_array = etc.overfullCheck(signal_values+noise_values+bg_values, obs)
                    
                    print("signal values array: ", signal_values)
                    print("noise values array: ", noise_values)
                    print("bg values array: ", bg_values)
                    print("final sensor array: ", final_sensor_array)
                    
                    peak_cts = np.max(final_sensor_array)
                    min_cts = np.min(final_sensor_array)
                    
                    SNR_ref = etc.get_snr_ref(counts, test_exposure, bg_values, obs)
                    print("The SNR of the reference image is: ", SNR_ref)   
                    
                    exposure_time = etc.calculateReqTime(obs.snr, SNR_ref, test_exposure, counts, obs, bg_values)

                    # exposure_time = "The exposure time is {x:.2f}".format(x=exposure_time)
                    
                    
                    # cts.aperture(obs, final_sensor_array)
                    fov = obs.computeFOV()
                    
                    
                    # rounding
                    
                    try:
                        counts = round(counts)
                        peak_cts = round(peak_cts)
                        min_cts = round(min_cts)
                        fov = round(fov)
                    except:
                        pass
                    
                    
                    
                    # table formatting
                    table_1a = []
                    table_1b = []
                    table_2a = []
                    table_2b = []
                    
                    i = 0
                    for key in params:  
                        if i % 2 == 0:
                            table_1a.append(key)
                            table_1b.append(params[key]) 
                        else:
                            table_2a.append(key)
                            table_2b.append(params[key]) 
                        i += 1
                                                               
                   
                    
                    # render output template
                    return render_template('output_v2.html', valid=valid, in_form=in_form, select_form=select_form,
                                            camera_presets=camera_presets, telescope_presets=telescope_presets, filter_presets=filter_presets,
                                            target_presets=target_presets, gao_sqm=gao_sqm,
                                            SB_url="static/plot_light_curve_SB.png", 
                                            counts=counts, exposure=exposure_time, peak=peak_cts, minimum=min_cts, fov=fov, 
                                            col1a=table_1a, col1b=table_1b, col2a=table_2a, col2b=table_2b)
                                            #fov=fov, counts=counts, peak=peak, minimum=minimum, exposure=exposure, error=None)
                                            # counts_url="static/spread_counts.png"
                
                else: 
                    # display error in HTML
                    return render_template('input.html', valid=False, in_form=in_form, select_form=select_form,
                                            camera_presets=camera_presets, telescope_presets=telescope_presets, filter_presets=filter_presets,
                                            target_presets=target_presets, gao_sqm=gao_sqm, error=error)
                
        # An error message will be displayed in the HTML
        else: valid = False
                
    # render HTML to be displayed
    return render_template('input.html', valid=valid, in_form=in_form, select_form=select_form,
                           camera_presets=camera_presets, telescope_presets=telescope_presets, filter_presets=filter_presets, 
                           target_presets=target_presets,gao_sqm=gao_sqm, 
                           error="Invalid Parameter(s) Below - Must Be Numeric (0 - 100,000)")



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





# TODO: add validation

def process_input(input: dict) -> dict:
        
    params = {}
    
    for key in input: 
        if key != "csrf_token" and key != "submit":
            try:   
                if(input[key] == OMIT_KEY):   
                    print("omitted")
                    print(key)
                    params[key] = "omit"
                else:
                    params[key] = float( input[key] )
            except:
                params[key] = input[key]   
           
                
    # post condition
    
    # source_name = params["source_type"]
    
    # omit_counts = {"point": 3, "extended": 3}
    
    
    # omit_count = InputForm.fields[source_name]
    
    # # omit_counts[source_name]
     
    
    # count = 0
    
    # for val in params.values():
        
    #     if val == "omit":
    #         count += 1
    
    # if omit_count != count:
        
    #     print("counted omits: ", count)
    #     print("expected omits: ", omit_count)
    #     return None
    
                
    # print(params)
    # print("counted omits: ", count)
    # print("expected omits: ", omit_count)
    
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