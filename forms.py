from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, SelectField, StringField
from wtforms.validators import NumberRange, InputRequired

import pyckles
import numpy as np

from spextra import SpecLibrary, Spextrum


# def picklesOLD(): 
    
#     # file = open("./static/presets/pickles.csv")
#     presets = [('', 'Custom')]
    
#     # for line in file:    
#     #     csvs = line.strip().split(",")
#     #     presets.append( (csvs[0], csvs[1]) )
        
#     # file.close()
    
#     spec_lib = pyckles.SpectralLibrary("pickles")
#     preset = np.asarray(spec_lib.available_spectra)
    
    
#     for val in preset:
#         presets.append( (val, val) )
    
#     presets 
    
    
#     return presets



def pickles():
    
    presets = [('', 'Custom')]
    
    lib = SpecLibrary("pickles")
    contents = list(lib)
    
    for val in contents:
        presets.append( (val, val) )
    
    return presets
    
    
    
def preset(name):
    
    presets = [('', 'Custom')]
    
    lib = SpecLibrary(name)
    contents = list(lib)
    
    for val in contents:
        presets.append( (val, val) )
    
    return presets
    
    
    

def validate_filters():
    pass 


class InputForm(FlaskForm):
       
    
    fields = { "camera": 9, "telescope": 3, "filter": 3, "target-point": 3, "conditions": 2, "snr": 1 }
    total_fields = sum(fields.values())
    
    # total field count
    #total_fields = camera_fields + telescope_fields + filter_fields + target_fields + conditions_fields + snr_fields
    
    # camera parameters 
    sensor_x = FloatField('Sensor Length', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    sensor_y = FloatField('Sensor Width', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    px_size = FloatField('Pixel Size', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    q_efficiency = FloatField('Quantum Efficiency', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    read_noise = FloatField('Read Noise', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    gain = FloatField('Gain', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    offset = FloatField('Offset', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    dark_noise = FloatField('Dark Noise', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    full_well = FloatField('Full Well', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    
    #telescope parameters
    scope_dia = FloatField('Diameter', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    scope_focal = FloatField('Focal Length', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    plate_scale = FloatField('Plate Scale', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    
    # filter parameters
    filter_low = FloatField('Filter Low', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    filter_high = FloatField('Filter High', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    filter_zero = FloatField('Zero Point Flux', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    

    
    # point source parameters
    star_dist_p = FloatField('Distance Pt.', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    star_lum = FloatField('Luminosity', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    star_temp = FloatField('Temperature', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    
    #extended source parameters
    star_dist_e = FloatField('Distance Ext.', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    surf_brightness = FloatField('Surface Brightness', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    magnitude = FloatField('Magnitude', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    
   
    # pickle = StringField('Source')
    
    # extended source parameters
    
    
    source_type = StringField('Source Type')
   
    
    
    
    # weather conditions
    seeing = FloatField('Seeing', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    sqm = FloatField('Sky Quality', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    
    # desired signal to noise ratio
    desired_snr = FloatField('Desired SNR', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    
    # submit data
    submit = SubmitField('Calculate')
    


class SelectForm(FlaskForm):
    
    camera = SelectField('Select Camera', choices=[('', 'Custom'), ('asi6200mm', 'ASI6200MM'), ('asi2600mm', 'ASI2600MM'), ('asi533mm', 'ASI533MM')])
    telescope = SelectField('Select Telescope', choices=[('', 'Custom'), ('cdk350', 'PlaneWave CDK350 - FIX'), ('c8', 'Celestron C8')])
    filter = SelectField('Select Filter', choices=[('', 'Custom'), ('test', 'Test - narrower'), ('test2', 'Test - wider')])
    # target = SelectField('Select Target', choices=[('', 'Custom'), ('test', 'Test')])
    
    conditions = SelectField('Select Conditions', choices=[('', 'Custom'), ('1', '1 (Poor)'), ('2', '2'), ('3', '3 (Average)'), ('4', '4'), ('5', '5 (Excellent)')])
    sky_bright = SelectField('Select Target', choices=[('', 'Custom'), ('goa', 'Current Glenlea Conditions')])
    
    point_src = SelectField('Select Target', choices=preset("pickles"))
    extended_src = SelectField('Select Target', choices=preset("brown"))
    
    