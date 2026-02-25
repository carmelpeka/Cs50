from django.urls import path
from .models import AuctionListing

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),

    path("listingpage/<int:auction_id>/", views.listingpage, name="listingpage"),
    path("closelisting", views.closelisting, name="closelisting"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("bid/<int:auction_id>/", views.bid, name="bid"),
    path("categorielist", views.categorielist, name="categorielist"),
    path("indexcategorie/<int:categorie_id>/", views.indexcategorie, name="indexcategorie")

]
