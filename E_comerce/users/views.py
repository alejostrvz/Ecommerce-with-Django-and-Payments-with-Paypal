from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, authenticate, login

from wishlist.models import WishlistItem
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# forms
from .forms import UserRegisterForm, UserUpdateForm,UpdatePasswordForm
# email
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

import uuid
#cart
from cart.models import Cart
from wishlist.models import Wishlist
# Create your views here.

# Sign up users


def register_user(request):
    # get all the values from the form
    if request.method == 'POST':
        # Create a instance of the form
        form = UserRegisterForm(request.POST)
        # valid the form
        if form.is_valid():
            if not User.objects.filter(email=form.cleaned_data['email']):
                user = User.objects.create_user(
                    username=form.cleaned_data['names'] +
                    " " + form.cleaned_data['last_names'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    names=form.cleaned_data['names'],
                    last_names=form.cleaned_data['last_names'],
                    gender=form.cleaned_data['gender'],
                    age=form.cleaned_data['age'],
                    country=form.cleaned_data['country'],
                    direction=form.cleaned_data['direction'], 
                    is_active = True
                )
                

                email_uuid = str(uuid.uuid4())
                user.emailValidationUUID = email_uuid
                cart = Cart()
                cart.user = user
                wishlist = Wishlist()
                wishlist.user = user
                cart.save()
                wishlist.save()
                user.save()

                #Welcome email
                subject = "Bienvenid@ a GTShop"
                message = "Hola "  + user.names + " " + user.last_names + "!! \n" + "Bienvenid@ a  GTShop \n Gracias por registrarte en GTShop \n Tambien te hemos enviado un correo electronico de confirmacion \n Por favor confirme su direccion de correo electronico, para activar su cuenta en GTShop \n\n Agradeciendote \n El equipo de GTShop "
                from_email = settings.EMAIL_HOST_USER
                to_list = [user.email]
                send_mail(subject, message, from_email, to_list, fail_silently=True)

                #confirm email    
                send_mail(
                    'Verificación de correo',
                    'Por favor verifica tu correo electrónico: http://localhost:8000/user/verify/' + email_uuid,
                    'shopcargt@gmail.com', #cambiar a correo shopcart - crear cuenta shopcar sendgrid
                    [user.email],
                    fail_silently=False,
                )

                

                messages.success(request,'Se ha enviado un correo de verificación')
                return redirect('login_user')
            else:
                messages.error(
                    request, 'Este correo electronico ya esta registrado!')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})

# Login user


def login_user(request):
    # get the values
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Verified if the user is active
            if user.is_active:
                login(request, user)  # start the session
                return redirect('home')
            else:
                return render(request, 'user/login.html', {
                    'error': True,
                    'message': 'Error'
                })
        else:
            return render(request, 'user/login.html', {
                'error': True,
                'message': 'Datos invalidos'
            })
    return render(request, 'user/login.html')



# Logout
@login_required(login_url='login_user')
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

# Email Validation xddd
def validate_email(request, email_uuid):
    try:
        user = User.objects.get(emailValidationUUID=email_uuid)
        user.emailValidationUUID = None
        user.isEmailValid = True
        user.save()

        return render(request, "user/email/emailvalidation.html", {
            "message": "Correo Electronico Confirmado Correctamente :) "
        })

    except ObjectDoesNotExist:
        return render(request, "user/email/emailvalidation.html", {
            "message": "Talvez este correo ya fue validado :("
        })

#info user
@login_required(login_url='login_user')
def info_user(request,username,id):
    #get the user and wishlit
    user = get_object_or_404(User,pk=id)
    #update
    if request.method == 'POST':
        form = UserUpdateForm(request.POST,instance=user)
        if form.is_valid:
            form.save()
            return redirect('home')
    else:
        form = UserUpdateForm(instance=user)
    return render(request,'user/info_user.html',{'form':form})

#update password
@login_required(login_url='login_user')
def update_password(request,id):
    if request.method == 'POST':
        #Traer el form
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            usuario = get_object_or_404(User,pk = id)
            user = authenticate(
                email = usuario.email,
                password = form.cleaned_data['password'],
            )
            if user:
                new_pass = form.cleaned_data['password_new']
                usuario.set_password(new_pass)
                usuario.save()
            logout(request)
            return redirect('home')
    else:
        form = UpdatePasswordForm()
    return render(request,'user/update.html',{"form":form})
