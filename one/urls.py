from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cinput/', views.cinput, name="input"),
    path('success/', views.success, name="success"),
    path('clogin/', views.clogin, name="clogin"),
    path('loginSuccess/', views.logins, name="logins"),
    path('cdash/', views.cdash, name="cdash"),
    path('logout/', views.logout_view, name='logout'),
    path('jinput/', views.jinput, name="jinput"),
    path('jlogin/', views.jlogin, name="jlogin"),
    path('jdash/', views.jdash, name="jdash"),
    path('jsuccess/', views.jsuccess, name="jsuccess"),
    path('resume/', views.baseresume, name="resume"),
]