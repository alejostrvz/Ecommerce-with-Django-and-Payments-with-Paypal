
from django import forms
from .models import User

#Forms 
#Register Form
class UserRegisterForm(forms.ModelForm):
    """Form definition for UserRegister."""
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget= forms.PasswordInput(
            attrs= {
                'placeholder':'Contraseña'
            }
        )
    )
    password2 = forms.CharField(
        label='Confirme contraseña',
        required=True,
        widget= forms.PasswordInput(
            attrs= {
                'placeholder':'Confirme contraseña'
            }
        )
    )
    class Meta:
        model = User
        fields = (
            'names',
            'last_names',
            'email',
            'gender',
            'age',
            'country',
            'direction',
        )
        widgets = {
            'names': forms.TextInput(attrs={'placeholder':'Ingrese sus nombres'}),
            'last_names': forms.TextInput(attrs={'placeholder':'Ingrese sus apellidos'}),
            'email': forms.EmailInput(attrs={'placeholder':'Ingrese un correo electronico'}),
            'country': forms.TextInput(attrs={'placeholder':'Ingrese su país'}),
            'direction':forms.TextInput(attrs={'placeholder':'Ingrese su dirección'}),
        }
        labels = {
            'names': 'Nombres',
            'last_names': 'Apellidos',
            'gender':'Genero',
            'country': 'País',
            'direction': 'Dirección',
        }
    #validations
    def clean_password2(self):
        #check if the both passwords are the same
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return pass2
    
class UserUpdateForm(forms.ModelForm):
    """Form definition for UserUpdate."""

    class Meta:
        """Meta definition for UserUpdateform."""

        model = User
        fields = ('names','last_names','age','country','direction',)


class UpdatePasswordForm(forms.Form):
    """Form definition for UpdatePassword."""
    password = forms.CharField(
        label='Contraseña:',
        required=True,
        widget= forms.PasswordInput(
            attrs= {
                'placeholder':'Ingrese su contraseña actual'
            }
        )
    )
    password_new = forms.CharField(
        label='Contraseña nueva:',
        required=True,
        widget= forms.PasswordInput(
            attrs= {
                'placeholder':'Ingrese su nueva contraseña'
            }
        )
    )

