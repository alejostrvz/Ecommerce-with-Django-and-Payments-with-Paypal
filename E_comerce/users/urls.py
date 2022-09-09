from django.urls import path
#Views
from .views import register_user,login_user,logout_user,validate_email,info_user,update_password
urlpatterns = [
    path('register/',register_user,name="register_user"),
    path('login/',login_user,name='login_user'),
    path('logout/',logout_user,name='logout_user'),
    path("verify/<str:email_uuid>",validate_email, name="email_validation"),
    #user
    path('info/<str:username>/<int:id>',info_user,name='info_user'),
    path('update_password/<int:id>',update_password, name='update_password'),
]