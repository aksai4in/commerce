from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bids, Comment, Category
class ListingForm(forms.Form):
    title = forms.CharField(label="Title")
    startingBid = forms.IntegerField()
    description = forms.CharField(max_length=2000, required = False, widget=forms.TextInput(attrs={}))
    imageURL = forms.CharField(required = False)
    category = forms.ModelChoiceField(queryset = Category.objects.all(), required = False)

class BidForm(forms.Form):
    bid = forms.IntegerField()

def index(request):
    return render(request, "auctions/index.html", {
        "listings":Listing.objects.filter(active = True)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
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

def listing(request, name):
    listing = Listing.objects.get(title = name)
    try:
        bids = Bids.objects.get(title = name)
    except:
        bids = None
    if request.method == "POST":
        if request.POST.get("authenticated") == "True":    
            try: 
                bid = Bids.objects.get(title = name)
                bid.owner = request.POST.get("owner")
            except:
                bid = Bids(title = name, owner = request.POST.get('owner'))
            if int(request.POST['bid']) <= bid.current or int(request.POST['bid']) < listing.startingBid :
                return render(request, "auctions/listing.html", {
                    "title":name,
                    "listing":listing, 
                    "bids": bids,
                    "bid_form":BidForm(),
                    "message": "Error: Your bid is too small.",
                    "comments": Comment.objects.filter(listing = listing)
                })
            else:
                bid.current = int(request.POST['bid'])
                bid.number += 1
                bid.save()
                listing.price = bid.current
                listing.save()
                return HttpResponseRedirect(reverse("listing", kwargs={'name':name}))
        else:
            return HttpResponseRedirect(reverse("login"))
    return render(request, "auctions/listing.html", {
        "title":name,
        "listing":listing,
        "bids": bids,
        "bid_form":BidForm(),
        "comments": Comment.objects.filter(listing = listing)
    })

def create(request):
    if request.method == "POST":
        listing = Listing(title = request.POST['title'], 
        startingBid = request.POST["startingBid"], 
        imageURL= request.POST['imageURL'], 
        category = Category.objects.get(pk=request.POST['category']), 
        description = request.POST['description'], 
        owner = request.POST['owner'] )
        listing.save()
    return render(request, "auctions/create.html", {
        "form":ListingForm()
    })

def close(request, name):
    if request.method == "POST":
        listing = Listing.objects.get(title = name)
        listing.active = False
        listing.category = None
        listing.save()
        try:
            bids = Bids.objects.get(title = name)
        except:
            bids = None
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("listing", kwargs={'name':name}))

def add(request, name):
    if request.method == "POST":
        user = User.objects.get(username = request.POST['owner'])
        listing = Listing.objects.get(title = name)
        user.watchlist.add(listing)
    return HttpResponseRedirect(reverse("listing", kwargs={'name':name}))

def watchlist(request, user):
    name = User.objects.get(username = user)
    return render(request, 'auctions/watchlist.html', {
        "watchlist":name.watchlist.all()
    })

def categories(request):
    return render(request, 'auctions/categories.html', {
        "categories": Category.objects.all()
    })

def category(request, cat):
    categ = Category.objects.get(name = cat)
    return render(request, "auctions/index.html", {
        "listings":categ.listings.filter(active = True)
    })

def comment(request, name):
    if request.method == "POST":
        body = request.POST["comment"]
        username = request.POST["username"]
        newComment = Comment(user = username, body = body, listing = Listing.objects.get(title = name))
        newComment.save()
    return HttpResponseRedirect(reverse("listing", kwargs={'name':name}))