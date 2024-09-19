from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, SelectField, StringField
from wtforms.validators import NumberRange, InputRequired, DataRequired, ValidationError, Optional

import pyckles
import numpy as np

from spextra import SpecLibrary, Spextrum, libraries

from spextra import DEFAULT_DATA
    
    
def preset(name):
    
    presets = [('', 'Blackbody (default)')]
    
    lib = SpecLibrary(name)
    contents = list(lib)
    
    for val in contents:
        
        if '-' not in val and '+' not in val:
            presets.append( (val, val) )
    
    return presets


def presetExt(name):
    
    presets = [('', 'Required')]
    
    lib = SpecLibrary(name)
    contents = list(lib)
    
    
    
    for val in contents:
        
        if '-' not in val and '+' not in val:
            presets.append( (val, val) )
    
    return presets



def filters():
    
    filters = [('', 'Required')]
    
    
    contents = DEFAULT_DATA.filters
    
    for val in contents:
        
        if '-' not in val and '+' not in val:
            filters.append( (val, val) )
            print(val)
    
    return filters





def filtersNew():
    
    test = libraries.FilterSystem(name="etc")
    contents = test.filters
    


    banned = ['L', 'M', 'N', 'Q']

    contents.insert(0, ('', 'Required'))

    for val in list(contents):
        if val[0] in banned:
            contents.remove(val)

    print(contents)
    return contents
         
    

class InputForm(FlaskForm):    
     
    fields = { "camera": 9, "telescope": 3, "filter": 3, "point": 2, "extended": 3, "conditions": 2, "snr": 1 }
    total_fields = sum(fields.values())
    
    # total field count
    #total_fields = camera_fields + telescope_fields + filter_fields + target_fields + conditions_fields + snr_fields
    
    # camera parameters 
    sensor_x = FloatField('Sample Length', validators=[InputRequired(), NumberRange(min=0, max=1000)], render_kw={"placeholder": 50})
    sensor_y = FloatField('Sample Width', validators=[InputRequired(), NumberRange(min=0, max=1000)], render_kw={"placeholder": 50})
    
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
    
        
    # point source parameters
    star_temp = FloatField('Temperature', validators=[Optional(), NumberRange(min=1000, max=100000)], render_kw={"required": "true"})
    star_ab_mag = FloatField('AB Magnitude', validators=[Optional(), NumberRange(min=-30, max=30)], render_kw={"required": "true"})
    
    
    # track type of source
    source_type = StringField('Source Type')
    
    
    
    #extended source parameters
    ext_mag = FloatField('Surface Brightness', validators=[Optional(), NumberRange(min=-100000, max=100000)], render_kw={"required": "false"})
    
    
    # TODO?
    # display_point = StringField('Source')
    
    
    
   

    # weather conditions
    seeing = FloatField('Seeing', validators=[InputRequired(), NumberRange(min=0, max=8)])
    sqm = FloatField('Sky Quality', validators=[InputRequired(), NumberRange(min=0, max=22)])
    
    # desired signal to noise ratio
    desired_snr = FloatField('Desired SNR', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    
    # submit data
    submit = SubmitField('Calculate')
    
    
    
    
  
    


    


class SelectForm(FlaskForm):
    
    camera = SelectField('Select Camera', choices=[('', 'Custom'), ('asi6200mm', 'ASI6200MM'), ('asi2600mm', 'ASI2600MM'), ('asi533mm', 'ASI533MM')])
    telescope = SelectField('Select Telescope', choices=[('', 'Custom'), ('cdk350', 'AG Optical FA12 12.5" H. Wynne'), ('c8', 'Celestron C8')])
    filter = SelectField('Select Filter', choices=filtersNew(), validators=[InputRequired()] )    
    conditions = SelectField('Select Conditions', choices=[('', 'Custom'), ('0.4', '0.4 (Excellent)'), ('1', '1') , ('2', '2'), ('3', '3 (Average)'), ('4', '4'), ('5', '5'), ('6', '6 (Poor)')])
    sky_bright = SelectField('Select Sky Bright', choices=[('', 'Custom'), ('goa', 'Current Glenlea Conditions')])
    
    point_src = SelectField('Select Target', choices=preset("pickles"))
    extended_src = SelectField('Select Target', choices=presetExt("brown")) # validators=[InputRequired()]
    
    suggested_snr = SelectField('Select SNR', choices=[('', 'Custom'), ('3', '3'), ('5', '5'), ('10', '10'), ('50', '50'), ('100', '100')])

    

