from flask_wtf import FlaskForm
from wtforms import DateField
from wtforms.fields.core import BooleanField, FloatField, SelectField, StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import date

def fecha_en_pasado(form, campo):
    hoy = date.today()
    if campo.data > hoy:
        raise ValidationError("La Fecha no puede ser mayor que hoy")


class MovimientosForm(FlaskForm):
    fecha = DateField("Fecha", validators=[DataRequired(message="Debe introducir una fecha válida"), fecha_en_pasado])
    concepto = StringField("Concepto", validators=[DataRequired(), Length(min=10)])
    categoria = SelectField("Categoria", choices=[  ("00", ""),
                                                    ("SU", "Supervivencia"),
                                                    ("OV", "Ocio/Vicio"),
                                                    ("CU", "cultura"),
                                                    ("EX", "Extras")])    
    cantidad = FloatField("Cantidad", validators = [DataRequired()])
    esGasto = BooleanField("Es gasto")
    submit = SubmitField("Aceptar")
    Nosubmit = SubmitField("Anular")