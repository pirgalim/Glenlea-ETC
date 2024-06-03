from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired


def validate_sqm(form, field):
        if not (field.data).isnumeric():
            raise ValidationError('Must be numeric')



class InputForm(FlaskForm):
    
    # input field count
    camera_fields = 9
    telescope_fields = 3
    filter_fields = 3
    target_fields = 3
    conditions_fields = 2
    snr_fields = 1
    
    # camera parameters 
    sensor_x = FloatField('Sensor Length', validators=[DataRequired()])
    sensor_y = FloatField('Sensor Width', validators=[DataRequired()])
    px_size = FloatField('Pixel Size', validators=[DataRequired()])
    q_efficiency = FloatField('Quantum Efficiency', validators=[DataRequired()])
    read_noise = FloatField('Read Noise', validators=[DataRequired()])
    gain = FloatField('Gain', validators=[DataRequired()])
    offset = FloatField('Offset', validators=[DataRequired()])
    dark_noise = FloatField('Dark Noise', validators=[DataRequired()])
    full_well = FloatField('Full Well', validators=[DataRequired()])
    
    #telescope parameters
    scope_dia = FloatField('Diameter', validators=[DataRequired()])
    scope_focal = FloatField('Focal Length', validators=[DataRequired()])
    plate_scale = FloatField('Plate Scale', validators=[DataRequired()])
    
    # filter parameters
    filter_low = FloatField('Filter Low', validators=[DataRequired()])
    filter_high = FloatField('Filter High', validators=[DataRequired()])
    filter_zero = FloatField('Zero Point Flux', validators=[DataRequired()])
    
    # target parameters
    star_dist = FloatField('Distance', validators=[DataRequired()])
    star_temp = FloatField('Temperature', validators=[DataRequired()])
    star_dia_solar = FloatField('Solar Diameter', validators=[DataRequired()])
    
    # weather conditions
    seeing = FloatField('Conditions', validators=[DataRequired()])
    sqm = StringField('Sky Quality', validators=[InputRequired(), validate_sqm])
    
    # desired signal to noise ratio
    desired_snr = FloatField('Desired SNR', validators=[DataRequired()])
    
    # submit data
    submit = SubmitField('Calculate')
    
    
    
    
    
    


class SelectForm(FlaskForm):
    camera = SelectField('Select Camera', choices=[('', 'Custom'), ('asi6200mm', 'ASI6200MM'), ('asi2600mm', 'ASI2600MM'), ('asi533mm', 'ASI533MM')])
    telescope = SelectField('Select Telescope', choices=[('', 'Custom'), ('cdk350', 'PlaneWave CDK350 - FIX'), ('c8', 'Celestron C8')])
    filter = SelectField('Select Filter', choices=[('', 'Custom'), ('test', 'Test - narrower'), ('test2', 'Test - wider')])
    target = SelectField('Select Target', choices=[('', 'Custom'), ('test', 'Test')])
    conditions = SelectField('Select Conditions', choices=[('', 'Custom'), ('1', '1 (Poor)'), ('2', '2'), ('3', '3 (Average)'), ('4', '4'), ('5', '5 (Excellent)')])
    sky_bright = SelectField('Select Target', choices=[('', 'Custom'), ('goa', 'Current Glenlea Conditions')])
