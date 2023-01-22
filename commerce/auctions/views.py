from email import message
from typing_extensions import Required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from .models import User, Category, Listing, Watchlist, Comment, Bid
from django.shortcuts import get_object_or_404
from django.contrib import messages


class NewListingForm(forms.Form):
   brand = forms.CharField(label = "Brand", required=False, widget = forms.TextInput(attrs = {"class":"form-control col-lg-8"}), max_length=30)
   model = forms.CharField(label = "Model", required=False, widget = forms.TextInput(attrs = {"class":"form-control col-lg-8"}), max_length=30)
   description = forms.CharField(label = "Description", required=False, widget = forms.TextInput(attrs = {"class":"form-control col-lg-8"}), max_length=300)
   imageUrl = forms.CharField(label = "ImageUrl", required=False, widget = forms.TextInput(attrs = {"class":"form-control col-lg-8"}), max_length=1000)
   price = forms.FloatField(label = "Price", required=False, widget=forms.NumberInput(attrs={"class":"form-control col-lg-8"}))
   isActive = forms.BooleanField(initial = False, widget = forms.HiddenInput, required = False)
   

def index(request):
    listings = Listing.objects.filter(isActive = True)
    return render(request, "auctions/index.html",{
        "listings": listings
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

@login_required()
def create_Listing(request):
     if request.method == "GET":
        categories = Category.objects.all()
        form = NewListingForm(request.GET)
        return render(request, "auctions/listing.html", {
            "form": form,
            "categories": categories
        })
     else:
        form = NewListingForm(request.POST)
        if form.is_valid():
            brand = form.cleaned_data["brand"]
            model = form.cleaned_data["model"]
            description = form.cleaned_data["description"]
            imageUrl = form.cleaned_data["imageUrl"]
            price = form.cleaned_data["price"]
            category = request.POST.get("category")
            user = request.user
            category2 = Category.objects.get(category0 = category)
            
            createlisting = Listing(
                brand = brand,
                model = model,
                description = description,
                imageUrl = imageUrl,
                price = float(price),
                owner = user,
                category1 = category2
            )
            createlisting.save()

            listings = Listing.objects.filter(isActive = True)
            return render(request, "auctions/index.html",{
                   "listings": listings
                 })



def view(request, model, id):
    
     listing = Listing.objects.get(pk=id)
     user = request.user
     count = Comment.objects.filter(listing=id).count()
     comments = Comment.objects.filter(listing=id)
     bidscount = Bid.objects.filter(listing=id).count()
     bids = Bid.objects.filter(listing=id)
     allowbid = False
     creator = False
     lowbid = False 
     inlist = False
     allowcomment = False
     winner = None
     notactive = False
     if user in listing.watchlist.all():
          inlist = True
       
     first = False
     if count == 0:
           first = True

     firstbid = False
     if bidscount == 0:
           firstbid = True

     if request.user.username == listing.owner.username and listing.isActive == True:
        creator = True
     
     if request.user.username != listing.owner.username and listing.isActive == True:
        allowbid = True
     
     if listing.isActive == True:
          allowcomment = True
     
     else:
        notactive = True
        latest_bid_id = Bid.objects.filter(listing = id).latest("id")
        winner = latest_bid_id.user

     if request.method == "GET":     
          return render(request, "auctions/view.html",{
            "listing": listing,
            "inlist": inlist,
            "comments": comments,
            "count": count,
            "first": first,
            "firstbid": firstbid,
            "bids": bids,
            "bidscount": bidscount,
            "creator": creator,
            "allowbid": allowbid,
            "allowcomment": allowcomment,
            "winner": winner,
            "notactive": notactive
            
          })

     else:  

      bidform = float(request.POST.get("bid"))
      try:
       latestbid_data = Bid.objects.filter(listing = id).latest("id")        
       latestbid = latestbid_data.bid
      except:
        latestbid = listing.price - 1
      if bidform < listing.price or bidform <= latestbid:
         lowbid = True
         return render(request, "auctions/view.html",{
            "listing": listing,
            "inlist": inlist,
            "comments": comments,
            "count": count,
            "first": first,
            "firstbid": firstbid,
            "bids": bids,
            "bidscount": bidscount,
            "listing": listing,
            "lowbid": lowbid,
            "creator": creator,
            "allowbid": allowbid,
            "allowcomment": allowcomment,
            "winner": winner,
            "notactive": notactive
          })
      else:    
         newbid = Bid(
           bid = bidform,
           user = user,
           listing = listing

         )
         newbid.save()
         return render(request, "auctions/view.html",{
            "listing": listing,
            "inlist": inlist,
            "comments": comments,
            "count": count,
            "first": first,
            "firstbid": firstbid,
            "bids": bids,
            "bidscount": bidscount,
            "listing": listing,
            "lowbid": lowbid,
            "creator": creator,
            "allowbid": allowbid,
            "allowcomment": allowcomment,
            "winner": winner,
            "notactive": notactive,
            "bidadded": True
          })     
         


def close(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        user = request.user
        listing.isActive = False
        listing.save()
        latest_bid_id = Bid.objects.filter(listing = id).latest("id")
        winner = latest_bid_id.user
        listing.watchlist.add(winner)
        listing.watchlist.add(user)
        model = listing.model
        return HttpResponseRedirect(reverse("view",args=(model, id, )))



def add(request, model, id):

    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        user = request.user
        listing.watchlist.add(user)
        return HttpResponseRedirect(reverse("view",args=(model, id, )))

def remove(request, model, id):

    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        user = request.user
        listing.watchlist.remove(user)
        return HttpResponseRedirect(reverse("view",args=(model, id, )))

    





def comment(request, id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=id)
        comment = request.POST.get("comment")
        addcomment = Comment(
           user = user,
           listing = listing,
           comment = comment
        )
        addcomment.save()
        model = listing.model
        return HttpResponseRedirect(reverse("view",args=(model, id, )))

def watchlist(request):
    if request.method == "GET":
        user = request.user
        p = False
        listings = Listing.objects.filter(watchlist = user)
        if Listing.objects.filter(watchlist = user).count() < 1:
         p = True
        return render(request, "auctions/watchlist.html",{
            "listings": listings,
            "p":p

        })


def category(request):
     search = False   
     categories = Category.objects.all()
     if request.method == "GET":  
        return render(request, "auctions/category.html", {
            "categories": categories,
            "search": search
        })

     else:
        search = True
        categoryform = request.POST.get("category")
        category = Category.objects.get(category0 = categoryform)
        listings = Listing.objects.filter(isActive = True, category1 = category)
        return render(request, "auctions/category.html",{
        "listings": listings,
        "categories": categories,
        "search": search,
        "res": categoryform

        })
