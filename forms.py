from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class SelectForm(FlaskForm):
    
    camera = SelectField(u"Select Camera", choices=[('asi6200mm', 'ASI6200MM'), ('asi2600mm', 'ASI2600MM'), ('asi533mm', 'ASI533MM')])
    submit = SubmitField('Autofill')


class InputForm(FlaskForm):
    
    dim_x = StringField('X-dimension', validators=[DataRequired()])
    dim_y = StringField('Y-dimension', validators=[DataRequired()])
    px_size = StringField('Pixel Size', validators=[DataRequired()])
        
    submit = SubmitField('Calculate')