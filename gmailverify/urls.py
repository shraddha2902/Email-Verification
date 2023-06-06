from django.urls import path
from gmailverify import views 


urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login',views.user_login),
    path('verifyscreen/<rid>',views.verifyscreen),
    path('verifyotp/<rid>',views.verifyotp),

]
