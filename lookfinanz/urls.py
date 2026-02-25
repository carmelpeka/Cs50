from django.urls import path
from .models import *

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login",views.login_view,name="login"),
    path("register",views.register,name="register"),
    path("logout", views.logout_view, name="logout"),
    path("newtransaction/", views.newtransaction, name="newtransaction"),
    path("random_data_upload", views.random_data_upload, name="random_data_upload"),
    path("filter_data_of_index_page", views.filter_data_of_index_page, name="filter_data_of_index_page"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("delete_transaction", views.delete_transaction, name="delete_transaction"),
    path("update_transaction", views.update_transaction, name="update_transaction"),
]
