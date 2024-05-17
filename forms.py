from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length


# class SelectForm(FlaskForm):
    
#     camera = SelectField(u"Select Camera", choices=[('asi6200mm', 'ASI6200MM'), ('asi2600mm', 'ASI2600MM'), ('asi533mm', 'ASI533MM')])
#     submit = SubmitField('Autofill')


class InputForm(FlaskForm):
    
    # camera parameters 
    dim_x = StringField('X-dimension', validators=[DataRequired()])
    dim_y = StringField('Y-dimension', validators=[DataRequired()])
    px_size = StringField('Pixel Size', validators=[DataRequired()])
    read_noise = StringField('Read Noise', validators=[DataRequired()])
    gain = StringField('Gain', validators=[DataRequired()])
    offset = StringField('Offset', validators=[DataRequired()])
    dark_noise = StringField('Dark Noise', validators=[DataRequired()])
    full_well = StringField('Full Well', validators=[DataRequired()])
    
       
    #observatory parameters
    
    # filter parameters
    
    # target parameters
    
    # weather conditions
      
    submit = SubmitField('Calculate')






class CameraSelectForm(FlaskForm):
    camera = SelectField('Select Camera:', choices=[('', 'Custom'), ('asi6200mm', 'ASI6200MM'), ('asi2600mm', 'ASI2600MM')])
    submit = SubmitField('Insert')
    

class TelescopeSelectForm(FlaskForm):
    telescope = SelectField('Select Camera:', choices=[('', 'Custom'), ('cdk350', 'PlaneWave CDK350')])