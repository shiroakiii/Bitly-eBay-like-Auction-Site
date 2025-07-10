from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Category, AuctionListing, Bid, User, Comment
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "auctions/index.html")

def browse(request):
    category_name = request.GET.get("category")

    if category_name:
        listings = AuctionListing.objects.filter(category__name__iexact=category_name)
    else:
        listings = AuctionListing.objects.all()

    for listing in listings:
        highest_bid = listing.bids.order_by("-amount").first()
        if highest_bid:
            listing.current_price = highest_bid.amount
        else:
            listing.current_price = listing.starting_bid

    return render(request, "auctions/browse.html", {
        "listings": listings,
        "selected_category": category_name
    })

def listing_view(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    num_bids = listing.bids.count()  
    comments = Comment.objects.filter(listing=listing).order_by("-timestamp")
    highest_bid = listing.bids.order_by("-amount").first()
    if highest_bid:
        current_price = highest_bid.amount
    else:
        current_price = listing.starting_bid
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_price": current_price,
        "num_bids": num_bids,
        "comments": comments
    })

@login_required
def place_bid(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(AuctionListing, id=listing_id)
        bid_amount = request.POST.get("bid")

        try:
            bid_amount = float(bid_amount)
        except ValueError:
            messages.error(request, "Invalid bid amount.")
            return redirect("listing", listing_id)
        
        current_highest = listing.bids.order_by("-amount").first()

        if current_highest:
            if bid_amount <= current_highest.amount:
                messages.error(request, "Bid must be higher than the current bid.")
                return redirect("listing", listing_id)
        else:
            if bid_amount < listing.starting_bid:
                messages.error(request, "Bid must be at least the starting bid.")
                return redirect("listing", listing_id)

        bid = Bid(
            user = request.user,
            listing = listing,
            amount = bid_amount
        )
        bid.save()
        messages.success(request, "Bid placed")
        return redirect("listing", listing_id)


@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    content = request.POST.get("comment")
    if content:
        Comment.objects.create(user=request.user, listing=listing, content=content)

    return redirect("listing", listing_id=listing.id)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return HttpResponseRedirect(reverse("browse"))
        else:
            messages.error(request, "Invalid username and/or password.")
            return render(request, "auctions/login.html")
    else:
        return render(request, "auctions/login.html")

def watchlist(request):
    user = request.user
    watchlist_items = user.watchlist.all()

    for item in watchlist_items:
        highest_bid = item.bids.order_by("-amount").first()
        if highest_bid:
            item.current_price = highest_bid.amount
        else:
            item.current_price = item.starting_bid

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist_items
    })

@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    if listing in request.user.watchlist.all():
        request.user.watchlist.remove(listing)
    else:
        request.user.watchlist.add(listing)
    return redirect("listing", listing_id=listing_id)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("browse"))


def close_listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)

    if listing.is_active:
        highest_bid = listing.bids.order_by("-amount").first()
        if highest_bid:
            listing.winner = highest_bid.user
        listing.is_active = False
        listing.save()

    return redirect("listing", listing_id=listing.id)

@login_required
def create_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        starting_bid = request.POST.get("starting_bid")
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)
        imageURL = request.POST.get("image_url")

        if not title or not description or not starting_bid:
            messages.warning(request, "Title, Description, and Starting Bid are required.")
            return render(request, "auctions/register.html")

        listing = AuctionListing(
            title = title,
            description = description,
            starting_bid = starting_bid,
            image_url = imageURL,
            category = category,
            owner = request.user
        )
        listing.save()
        messages.success(request, "Listing Created!")
        return HttpResponseRedirect(reverse("create"))

    return render(request, "auctions/create.html", {
        "categories": Category.objects.all()
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"].strip()
        email = request.POST["email"].strip()
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Added check for empty fields
        if not username or not email or not password or not confirmation:
            messages.warning(request, "All fields are required.")
            return render(request, "auctions/register.html")

        # Ensure password matches confirmation
        if password != confirmation:
            messages.warning(request, "Passwords must match.")
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.warning(request, "Username already exists.")
            return render(request, "auctions/register.html")

        login(request, user)
        messages.success(request, "Account created and logged in!")
        return HttpResponseRedirect(reverse("browse"))

    else:
        return render(request, "auctions/register.html")
    

def categories(request):
    return render(request, "auctions/categories.html")