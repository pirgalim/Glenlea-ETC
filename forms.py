from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Length


# class SelectForm(FlaskForm):
    
#     camera = SelectField(u"Select Camera", choices=[('asi6200mm', 'ASI6200MM'), ('asi2600mm', 'ASI2600MM'), ('asi533mm', 'ASI533MM')])
#     submit = SubmitField('Autofill')


class InputForm(FlaskForm):
    
    camera_fields = 9
    telescope_fields = 3
    
    
    # camera parameters 
    sensor_x = StringField('X-dimension', validators=[DataRequired()])
    sensor_y = StringField('Y-dimension', validators=[DataRequired()])
    px_size = FloatField('Pixel Size', validators=[DataRequired()])
    q_efficiency = StringField('Quantum Efficiency', validators=[DataRequired()])
    read_noise = StringField('Read Noise', validators=[DataRequired()])
    gain = StringField('Gain', validators=[DataRequired()])
    offset = StringField('Offset', validators=[DataRequired()])
    dark_noise = StringField('Dark Noise', validators=[DataRequired()])
    full_well = StringField('Full Well', validators=[DataRequired()])
    
       
    #telescope parameters
    scope_dia = StringField('Diameter', validators=[DataRequired()])
    scope_focal = StringField('Focal Length', validators=[DataRequired()])
    plate_scale = StringField('Plate Scale', validators=[DataRequired()])
    
    # filter parameters
    
    # target parameters
    
    # weather conditions
      
    submit = SubmitField('Calculate')






class CameraSelectForm(FlaskForm):
    camera = SelectField('Select Camera:', choices=[('', 'Custom'), ('asi6200mm', 'ASI6200MM'), ('asi2600mm', 'ASI2600MM'), ('asi533mm', 'ASI533MM')])
    submit = SubmitField('Insert Template')
    

class TelescopeSelectForm(FlaskForm):
    telescope = SelectField('Select Telescope:', choices=[('', 'Custom'), ('cdk350', 'PlaneWave CDK350'), ('c8', 'Celestron C8')])
    submit = SubmitField('Insert Template')
    

class FilterSelectForm(FlaskForm):
    filter = SelectField('Select Filter:', choices=[('', 'Custom'), ('x', 'X')])
    submit = SubmitField('Insert Template')