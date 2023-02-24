from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="FoodopsHome"),
    path("register", views.Register, name="Register"),
    path("login", views.Login, name="Login"),
    path("logout", views.Logout, name="Logout"),
    path("MainNGO", views.MainNGO, name="MainNGO"),
    path("MainPeople", views.MainPeople, name="MainPeople"),
    path("NgoDetail", views.NgoDetail, name="NgoDetail"),
    path("RequestNgo", views.RequestNgo, name="RequestNgo"),
    path("AcceptedRequest", views.AcceptedRequest, name="AcceptedRequest"),
    path("DoneRequest", views.DoneRequest, name="DoneRequest")
]

