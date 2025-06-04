# Uncomment the required imports before adding the code
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
from django.conf import settings

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from .restapis import get_request, analyze_review_sentiments, post_review
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Define backend URL using settings
BACKEND_URL = getattr(settings, "BACKEND_URL",
                     "https://lukaslondono-3030.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai"
                    ).rstrip("/")

# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request) # Terminate user session
    data = {"userName":""} # Return empty username
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}
    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))
    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)

#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(f"{BACKEND_URL}{endpoint}")
    return JsonResponse({"status":200,"dealers":dealerships})

def get_dealer_reviews(request, dealer_id):
    if(dealer_id):
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(f"{BACKEND_URL}{endpoint}")
        if reviews:
            for review_detail in reviews:
                try:
                    response = analyze_review_sentiments(review_detail['review'])
                    if response and 'sentiment' in response:
                        review_detail['sentiment'] = response['sentiment']
                    else:
                        review_detail['sentiment'] = 'neutral'  # Default sentiment if analysis fails
                except Exception as e:
                    print(f"Error analyzing sentiment: {e}")
                    review_detail['sentiment'] = 'neutral'  # Default sentiment on error
            return JsonResponse({"status":200,"reviews":reviews})
        else:
            return JsonResponse({"status":404,"message":"No reviews found"})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = f"/fetchDealer/{dealer_id}"
        print(f"Fetching dealer details from: {BACKEND_URL}{endpoint}")
        dealership = get_request(f"{BACKEND_URL}{endpoint}")
        print(f"Dealership response: {dealership}")
        
        if dealership:
            if isinstance(dealership, list) and len(dealership) > 0:
                return JsonResponse({"status":200,"dealer":dealership})
            elif isinstance(dealership, dict):
                return JsonResponse({"status":200,"dealer":[dealership]})
            else:
                print(f"Unexpected dealership data format: {dealership}")
                return JsonResponse({"status":404,"message":"Dealer not found"})
        else:
            return JsonResponse({"status":404,"message":"Dealer not found"})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})

def contact(request):
    return JsonResponse({"status": 200, "message": "Contact endpoint is working"})