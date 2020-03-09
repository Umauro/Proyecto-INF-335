
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    query = StringField('Username', validators=[DataRequired(), Length(min=2, max =50)])
    submit = SubmitField('Search')