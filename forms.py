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
    
    
    #FIXME: why does this cause problems?
    for val in contents:
        
        if '-' not in val and '+' not in val:
            presets.append( (val, val) )
    
    return presets


def presetExt(name):
    
    presets = [('', 'Required')]
    
    lib = SpecLibrary(name)
    contents = list(lib)
    
    
    #FIXME: why does this cause problems?
    for val in contents:
        
        if '-' not in val and '+' not in val:
            presets.append( (val, val) )
    
    return presets



#TODO: is this used at all?
def filters():
    
    filters = [('', 'Required')]
    
    
    #FIXME: change to .items()
    contents = DEFAULT_DATA.filters
    
    for val in contents:
        
        if '-' not in val and '+' not in val:
            filters.append( (val, val) )
            print(val)
    
    return filters




#TODO: can I just use PASSBAND.DEFAULT_FILTERS?
def filtersNew():
    
    contents = [('', 'Required')]
    
    # add specific filters
    contents.append( ('u', 'SDSS u') )
    contents.append( ('g', 'SDSS g') )
    contents.append( ('r', 'SDSS r') )
    contents.append( ('i', 'SDSS i') )
    
    # ESO filter set
    test = libraries.FilterSystem(name="etc")
    eso = test.filters
    
    # filters that currently cause issues
    banned = ['L', 'M', 'N', 'Q']

    # set filter path
    for val in list(eso):
        if val[0] != '' and val[0] not in banned:
            contents.append( ('etc/' + val[0], val[1]) )
        
    return contents
         
    

class InputForm(FlaskForm):    
     
    fields = { "camera": 9, "telescope": 3, "filter": 3, "point": 2, "extended": 3, "conditions": 2, "snr": 1 }
    total_fields = sum(fields.values())
    
    # total field count
    #total_fields = camera_fields + telescope_fields + filter_fields + target_fields + conditions_fields + snr_fields
    
    # camera parameters 
    sensor_x = FloatField('Sample Length', validators=[InputRequired(), NumberRange(min=10, max=400)], render_kw={"placeholder": 50})
    sensor_y = FloatField('Sample Width', validators=[InputRequired(), NumberRange(min=10, max=400)], render_kw={"placeholder": 50})
    
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
    plate_scale = FloatField('Plate Scale', validators=[InputRequired(), NumberRange(min=0.01, max=100000)])
    
        
    # point source parameters - required by default
    star_temp = FloatField('Temperature', validators=[Optional(), NumberRange(min=1000, max=100000)], render_kw={"required": "true"})
    star_ab_mag = FloatField('AB Magnitude', validators=[Optional(), NumberRange(min=-30, max=30)], render_kw={"required": "true"})
    
    
    # track type of source
    source_type = StringField('Source Type')
    
    
    
    #extended source parameters - not required by default
    ext_mag = FloatField('Surface Brightness', validators=[Optional(), NumberRange(min=-100000, max=100000)], render_kw={"required": "false"})
    
    
    # TODO?
    # display_point = StringField('Source')
    
    
    
   

    # weather conditions
    seeing = FloatField('Seeing', validators=[Optional(), NumberRange(min=0.001, max=8)], render_kw={"required": "true"})
    sqm = FloatField('Sky Quality', validators=[InputRequired(), NumberRange(min=0, max=22)])
    
    # desired signal to noise ratio
    desired_snr = FloatField('Desired SNR', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    
    # submit data
    submit = SubmitField('Calculate')
    
    
    
    
  
    


    

# TODO: add a constructor for templates?
class SelectForm(FlaskForm):
    
    camera = SelectField('Select Camera', choices=[('', 'Custom'), ('sbig', 'SBIG AC4040 BSI'), ('atik', 'ATIK 11000'), ('asi6200mm', 'ASI6200MM')])
    telescope = SelectField('Select Telescope', choices=[('', 'Custom'), ('cdk14', 'Planewave CDK14')])
    filter = SelectField('Select Filter', choices=filtersNew(), validators=[InputRequired()] )    
    conditions = SelectField('Select Conditions', choices=[('', 'Custom'), ('0.4', '0.4 (Excellent)'), ('1', '1') , ('2', '2'), ('3', '3 (Average)'), ('4', '4'), ('5', '5'), ('6', '6 (Poor)')])
    sky_bright = SelectField('Select Sky Bright', choices=[('', 'Custom'), ('goa', 'Current Glenlea Conditions')])
    
    point_src = SelectField('Select Target', choices=preset("pickles"))
    extended_src = SelectField('Select Target', choices=presetExt("brown")) # validators=[InputRequired()]
    
    suggested_snr = SelectField('Select SNR', choices=[('', 'Custom'), ('3', '3'), ('5', '5'), ('10', '10'), ('50', '50'), ('100', '100')])

    

