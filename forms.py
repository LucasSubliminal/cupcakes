from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import StringField, SelectField, FloatField
from wtforms.validators import InputRequired, Optional, NumberRange

class AddCupcakeForm(FlaskForm):

    flavor = StringField('Flavor', validators = [InputRequired()])

    image = StringField( 'Image URL', validators=[Optional()])
   

    rating = FloatField('Rating', validators=[InputRequired(), NumberRange(min=0, max=5)])

    size = SelectField('Size', choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')])

   

