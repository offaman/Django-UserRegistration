from django.urls import path
from accounts import views
urlpatterns =[
    path('register', views.register, name = 'register'),
    path('verify/<auth_token>', views.verify , name = 'verify'),
    path('login', views.login, name = 'login'),
    path('delete', views.delete, name = 'delete'),
    path('delete/<auth_token>', views.confirmdelete, name = 'confirm deletion'),
    path('forget', views.forgetpassword, name = 'forgetpassword'),
    path('changepassword/<auth_token>', views.changepassword, name = 'changepassword'),
    path('logout', views.logout, name = 'logout'),
    path('getcookie', views.authlogin, name = 'getcookie'),
    # path('event', views.createEventObject),
    path('oneminute', views.delete_after_particular_minutes)
]