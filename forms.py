from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length




class InputForm(FlaskForm):
    
    dim_x = StringField('X-dimension', validators=[DataRequired()])
    dim_y = StringField('Y-dimension', validators=[DataRequired()])
    px_size = StringField('Pixel Size', validators=[DataRequired()])
        
    submit = SubmitField('Calculate')