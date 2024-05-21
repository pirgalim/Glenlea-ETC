from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Length


# class SelectForm(FlaskForm):
    
#     camera = SelectField(u"Select Camera", choices=[('asi6200mm', 'ASI6200MM'), ('asi2600mm', 'ASI2600MM'), ('asi533mm', 'ASI533MM')])
#     submit = SubmitField('Autofill')


class InputForm(FlaskForm):
    
    camera_fields = 9
    telescope_fields = 3
    filter_fields = 3
    
    
    # camera parameters 
    sensor_x = FloatField('Sensor X', validators=[DataRequired()])
    sensor_y = FloatField('Sensor Y', validators=[DataRequired()])
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
    filter_zero = FloatField('Filter Zero', validators=[DataRequired()])
    
    
    # target parameters
    
    # weather conditions
      
    submit = SubmitField('Calculate')






class CameraSelectForm(FlaskForm):
    camera = SelectField('Select Camera', choices=[('', 'Custom'), ('asi6200mm', 'ASI6200MM'), ('asi2600mm', 'ASI2600MM'), ('asi533mm', 'ASI533MM')])
    

class TelescopeSelectForm(FlaskForm):
    telescope = SelectField('Select Telescope', choices=[('', 'Custom'), ('cdk350', 'PlaneWave CDK350'), ('c8', 'Celestron C8')])
    

class FilterSelectForm(FlaskForm):
    filter = SelectField('Select Filter:', choices=[('', 'Custom'), ('test', 'Test')])