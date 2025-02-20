from wtforms import  Form, validators
from wtforms import  StringField, PasswordField, EmailField, BooleanField, SubmitField, IntegerField

class UserForm(Form):
    matricula=IntegerField("Matricula", [ 
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=3, max=10, message='3-10 caracteres')
    ])
    nombre=StringField("Nombre", [ 
        validators.DataRequired(message='El campo es requerido')
    ])
    apellido=StringField("Apellido"[ 
        validators.DataRequired(message='El campo es requerido')
    ])
    correo=EmailField("Correo"[ 
        validators.email(message='Correo invalido')
    ])
    