from flask_wtf import FlaskForm
from wtforms import DateField
from wtforms.fields.core import SelectField, StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length

class MovimientosForm(FlaskForm):
    fecha = DateField("Fecha", validators=[DataRequired()])
    concepto = StringField("Concepto", validators=[DataRequired(), Length(min=10)])
    categoria = SelectField("Categoria", choices=[  ("SU", "Supervivencia"),
                                                    ("OV", "Ocio/Vicio"),
                                                    ("CU", "cultura"),
                                                    ("EX", "Extras")])
    submit = SubmitField("Aceptar")