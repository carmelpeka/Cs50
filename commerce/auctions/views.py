from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import *
from .models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
categories=["Fashion", "Toys", "Electronics", "Home"]

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model=AuctionListing
        fields=["title","description","price"]
def index(request):
    return render(request, "auctions/index.html",{"Auction_liste": AuctionListing.objects.all()})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)

            return redirect("index")# HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def createlisting(request):
    if request.method=="POST":
        form =AuctionListingForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            description=form.cleaned_data["description"]
            price=form.cleaned_data["price"]
            url=request.POST["url"]

            category_index = request.POST["categorie"]

            if category_index == "" or category_index is None:
                category="another"
            else:
                category = categories[int(category_index)]

            AuctionListing.objects.create(
                title=title,
                description=description,
                price=price,
                author=request.user,
                url=url,
                category=category,
                time=timezone.now()
            ).save()
            return redirect("index")
        else:
            return redirect("createlisting")


    return render(request, "auctions/createlisting.html",{"Auction_liste": AuctionListing.objects.all(),
                  "categories":categories})

@login_required
def listingpage(request,auction_id):
    auction = AuctionListing.objects.get(id=auction_id)
    highest_bid=auction
    comment_list=[]
    is_auction_author = (request.user == AuctionListing.objects.get(id=auction_id).author)
    is_highest_bid=False
    if request.method == "POST":
        if "add" in request.POST:
            if auction_id not in [watchlist.auction.id for watchlist in Watchlist.objects.all() if watchlist.author==request.user]:
                Watchlist.objects.create(
                    auction=AuctionListing.objects.get(id=auction_id),
                    author=request.user
                )
        elif "remove" in request.POST:
            qs = Watchlist.objects.filter(
                auction_id=auction_id,
                author=request.user
            )
            if qs.exists():
                qs.delete()
        elif "close" in request.POST:

            AuctionListing.objects.filter(id=auction_id).update(status=False)


        elif "bid" in request.POST:

            return redirect("bid", auction_id=auction_id)
        elif "comment" in request.POST:
            description=request.POST["comment"]
            Comment.objects.create(
                author=request.user,
                auction=auction,
                description=description
            )


        else:
            pass
    if not auction.status:
        highest_bid = Bid.objects.filter(auction=auction).order_by('-price').first()
        if highest_bid is None:
            return HttpResponse("no bid")
        is_highest_bid = (request.user == highest_bid.author)

    comment_list = [comment.description for comment in Comment.objects.filter(auction=auction).all()]
    return render(request,"auctions/listingpage.html",{"auction":AuctionListing.objects.get(id=auction_id),
                                                       "is_auction_author":is_auction_author,
                                                       "highest_bid":highest_bid,
                                                       "is_highest_bid":is_highest_bid,
                                                       "comment_list":comment_list})
def watchlist(request):
    return render(request,"auctions/watchlist.html",{"Watchlists":request.user.Watchlist.all()})

def bid(request,auction_id):
    if request.method=="POST":
        price=float(request.POST["price"])
        if price <=AuctionListing.objects.get(id=auction_id).price:
            return HttpResponse (f" Error price muss be >{AuctionListing.objects.get(id=auction_id).price}")
        else:
            Bid.objects.create(
                auction=AuctionListing.objects.get(id=auction_id),
                price=price,
                author=request.user
            )

            AuctionListing.objects.filter(id=auction_id).update(price=price)
    return render(request,"auctions/bid.html",{"auction_id":auction_id})
def categorielist(request):
    return render(request,"auctions/categorielist.html",{"categories":categories})

def indexcategorie(request,categorie_id):
    Auction_liste = [auction for auction in list(AuctionListing.objects.all()) if auction.category == categories[categorie_id]]
    return render(request, "auctions/indexcategorie.html", {"Auction_liste": Auction_liste,
                                                            "taill":len(Auction_liste)})
@login_required
def closelisting(request):
    return render(request, "auctions/closelisting.html", {"Auction_liste": AuctionListing.objects.all()})