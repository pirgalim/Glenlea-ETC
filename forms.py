from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, NumberRange, ValidationError, InputRequired


class InputForm(FlaskForm):
    
    # input field count
    camera_fields = 9
    telescope_fields = 3
    filter_fields = 3
    target_fields = 3
    conditions_fields = 2
    snr_fields = 1
    
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
    
    # target parameters
    star_dist = FloatField('Distance', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    star_temp = FloatField('Temperature', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    star_dia_solar = FloatField('Solar Diameter', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    
    # weather conditions
    seeing = FloatField('Conditions', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    sqm = FloatField('Sky Quality', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    
    # desired signal to noise ratio
    desired_snr = FloatField('Desired SNR', validators=[InputRequired(), NumberRange(min=0, max=100000)])
    
    # submit data
    submit = SubmitField('Calculate')
    
    
    
    
    
    


class SelectForm(FlaskForm):
    camera = SelectField('Select Camera', choices=[('', 'Custom'), ('asi6200mm', 'ASI6200MM'), ('asi2600mm', 'ASI2600MM'), ('asi533mm', 'ASI533MM')])
    telescope = SelectField('Select Telescope', choices=[('', 'Custom'), ('cdk350', 'PlaneWave CDK350 - FIX'), ('c8', 'Celestron C8')])
    filter = SelectField('Select Filter', choices=[('', 'Custom'), ('test', 'Test - narrower'), ('test2', 'Test - wider')])
    target = SelectField('Select Target', choices=[('', 'Custom'), ('test', 'Test')])
    conditions = SelectField('Select Conditions', choices=[('', 'Custom'), ('1', '1 (Poor)'), ('2', '2'), ('3', '3 (Average)'), ('4', '4'), ('5', '5 (Excellent)')])
    sky_bright = SelectField('Select Target', choices=[('', 'Custom'), ('goa', 'Current Glenlea Conditions')])
