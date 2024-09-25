from flask import Flask, render_template, request

from forms import InputForm, SelectForm
import services.etc as etc
import services.observation as observation
import services.scrape_sqm as sqm
import templates as tp

import base64
import numpy as np



# Flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'd42c51f24733b869a5916a8c09043624'



@app.route('/', methods=['GET', 'POST'])
def calculator():
       
    # create forms
    in_form = InputForm()
    select_form = SelectForm()
    
    # Used for input validation message
    valid = True
      
    # fetch presets
    camera_presets = tp.cameras
    telescope_presets = tp.telescopes
            
    # retrieve current GAO SQM value
    gao_sqm = sqm.get_sqm()   
    
    # detect if form has been submitted
    if in_form.submit.data:
                        
        # check for valid input fields
        if in_form.validate():
                    
            # retrieve form data
            data = request.form
            params = process_input(data)

            #TODO for testing
            print(params)
    
                        
            # validate number of parameters
            if(params is None):
                return render_template("error.html", message="There is a problem with the number of parameters being passed from the form to the script.")
            
            else:
                
                obs = observation.Observation(params)
                
                # error = etc.validate(obs)
                error = None #TODO
                
                # validate some parameters                
                if error == None:
                                    
                    test_exposure = 1  # seconds
         
                    counts = etc.calc_counts(obs)
                    
                    plot = etc.plot_bodies(obs)
                    encoded_image = base64.b64encode(plot).decode('utf-8')                   
                                     
                    signal_values = etc.spreadCounts(obs, counts, 1)
            
                    # Adjust counts to what the detector will see (circle)
                    counts = etc.countsInRad(obs, signal_values)
                   
                    noise_values = etc.generateNoise(obs ,test_exposure)
                    
                    #TODO rename
                    bg_values = etc.generateBG_TEST(obs)
                    
                    final_sensor_array = etc.overfullCheck(signal_values+noise_values+bg_values, obs)
                    
                    peak_cts = np.max(final_sensor_array)
                    min_cts = np.min(final_sensor_array)
                    
                    SNR_ref = etc.get_snr_ref(counts, test_exposure, bg_values, obs)
                    
                    exposure_time = etc.calculateReqTime(obs.snr, SNR_ref, test_exposure, counts, obs, bg_values)

                    # exposure_time = "The exposure time is {x:.2f}".format(x=exposure_time)
                    
                    aperture_plot = etc.aperturePlot(obs, final_sensor_array)
                    aperture_plot_encoded = base64.b64encode(aperture_plot).decode('utf-8')
                     
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
                    for key, value in params.items():  
                        
                        if params[key] == '':
                            value = 'n/a'
                        
                        if i % 2 == 0:
                            table_1a.append(key)
                            table_1b.append(value) 
                        else:
                            table_2a.append(key)
                            table_2b.append(value) 
                        i += 1
                                                               
                    
                    # render output template
                    return render_template('output.html', valid=valid, in_form=in_form, select_form=select_form,
                                            camera_presets=camera_presets, telescope_presets=telescope_presets,
                                            gao_sqm=gao_sqm, plot=encoded_image, aperture=aperture_plot_encoded,
                                            counts=counts, exposure=exposure_time, peak=peak_cts, minimum=min_cts, fov=fov, 
                                            col1a=table_1a, col1b=table_1b, col2a=table_2a, col2b=table_2b)
                                            #fov=fov, counts=counts, peak=peak, minimum=minimum, exposure=exposure, error=None)
                                            # counts_url="static/spread_counts.png"
                
                else: 
                    # display error in HTML
                    return render_template('input.html', valid=False, in_form=in_form, select_form=select_form,
                                            camera_presets=camera_presets, telescope_presets=telescope_presets,
                                            gao_sqm=gao_sqm, error=error)
                
        # An error message will be displayed in the HTML
        else: valid = False
                
    # render HTML to be displayed
    return render_template('input.html', valid=valid, in_form=in_form, select_form=select_form,
                           camera_presets=camera_presets, telescope_presets=telescope_presets, 
                           gao_sqm=gao_sqm, 
                           error="Invalid Parameter(s) Below")



# TODO: add validation

def process_input(input: dict) -> dict:
        
    params = {}
    
    for key in input: 
        if key != "csrf_token" and key != "submit":
            try:   
                # if(input[key] == OMIT_KEY):   
                #     print("omitted")
                #     print(key)
                #     params[key] = "omit"
                # else:
                params[key] = float( input[key] )
            except:
                params[key] = input[key]   
                
                #TODO should switch to isnumeric, not try-except
                
            # if( input[key].isdigit()) :
            #     params[key] = float( input[key] )
            # else:
            #     params[key] = input[key]

    return params
    
            

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=3000)