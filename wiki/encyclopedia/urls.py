from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("resultat/<str:task>/", views.resultat, name="resultat"),
    path("modify/<str:title>/", views.modify, name="modify"),
    path("modifytransition/", views.modifytransition, name="modifytransition"),
    path("savearticle/", views.savearticle, name="savearticle"),
    path("randompage/", views.randompage, name="randompage"),
    path("<str:title>/", views.title, name="title")

]

