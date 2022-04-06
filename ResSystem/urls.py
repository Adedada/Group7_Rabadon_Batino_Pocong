from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

#paths arranged alphabetically by name
app_name = 'ResSystem'
urlpatterns = [ 
    path('home', views.homeView.as_view(), name="home_view"),  
    path('about', views.aboutView.as_view(), name="about_view"),         
    path('contact', views.contactView.as_view(), name="contact_view"),   
    path('room', views.roomView.as_view(), name="room_view"),
    path('addroom', views.addroomView.as_view(), name="addroom_view"),
    path('user', views.userView.as_view(), name="user_view"),
    path('login', auth_view.LoginView.as_view(template_name='login.html'),name="login_view"),
    path('logout', auth_view.LogoutView.as_view(template_name='logout.html'),name="logout_view"),
    path('register', views.registerView.as_view(), name="register_view"),
    path('reservation', views.reservationView.as_view(), name="reservation_view"),
]
