"""
Created on Sun May 31 17:45:29 2020

@authors: chetanrupakheti, milson
"""

from django.shortcuts import redirect, render
import numpy as np
from matplotlib import pyplot as plt

from zomato_distribution_api.zomato_wrapper import Zomato
import requests
import json

key="ef7a18bb9bda931d550f4965d60e5be7"  # zomato's API key

def getRestaurantRating(restaurantObj):
    """
    returns a restaurant's attributes
    @params: restaurantObj
    @return
    results: python dictionary with restaurant's attributes
    """

    results = {}  # return type

    res_id = restaurantObj['R']['res_id']  # restaurant id
    rating = float(restaurantObj['user_rating']['aggregate_rating'])  # rating out of 5
    votes = int(restaurantObj['user_rating']['votes'])  # number of votes
    price = restaurantObj['average_cost_for_two'] / 2.0  # price for one
    name = restaurantObj['name']
    url = restaurantObj['url']
    address = restaurantObj['location']['address']  # add street
    address = address + "\n" + restaurantObj['location']['city']  # add city
    address = address + "\n" + restaurantObj['location']['zipcode']  # add zipcode
    contact = restaurantObj['phone_numbers']

    results["res_id"] = res_id
    results["usr_rating"] = rating
    results["votes"] = votes
    results["price"] = price
    results["name"] = name
    results["url"] = url
    results["address"] = address
    results["contact"] = contact

    return results

def score(restaurantsList):
    """
    computes a normalized ratings based on votes received by a restaurant
    @params
    restaurantsList: list of restaurants
    return: dictionary of restaurants sorted by their normalized rating
    """

    totalVote = 0
    tmp = {}  # contains dictionary of all restaurants that are hit
    tmpRes = {}  # temporary dic to ease sorting
    sortedResturants = {}  # final rank based on normalized rating

    for restaura in restaurantsList['restaurants']:
        results = getRestaurantRating(restaura['restaurant'])

        tmp[results['res_id']] = results  # contains all hits that are unranked yet;
        # restaurant id is the key
        totalVote += results['votes']

    for res in tmp:
        tmp[res]['norm_rating'] = tmp[res]['usr_rating'] / totalVote
        tmpRes[res] = tmp[res]['norm_rating']  # preparing only for sorting purpose

    sortedRes = {k: v for k, v in sorted(tmpRes.items(), key=lambda item: item[1], reverse=True)}  # sorts based on normalized rating
    for r in sortedRes:
        sortedResturants[r] = tmp[r]  # pulling all attributes of a restaurant using its ID

    return sortedResturants


def home(request):
    """
    Main function that gets called
    @param: request object of cusine type
    @return: list of restaurants based on search criteria
    example: restaurant.search({"lat":41.8013895,"lon":-87.589538,"cuisines":25,"radius":20000})
    """

    z = Zomato(key)
    cuisines = "117,148"  # cuisines ID for Nepali and Indian Cuisines
    radius = 200  # radius within the current location in meters
    limit = 10  # number of restaurants to display
    restaurants = z.restaurant_search(radius=radius, cuisines=cuisines, limit=limit)

    # print(restaurants)

    """Rendering the final results"""
    context = {
        'menus': 'abc',
        'result': restaurants #finalResult
    }

    return render(request, 'foodie_friend_app/index.html', context)


def get_cuisine_id(cuisine_name):
    """
    return the zomato's cuisine ID for the given cuisine name
    @params: cuisine_name string
    @return: cuisine ID int
    """

    z = Zomato(key)
    city_id = z.get_city_id()  # get zomato's current city's ID
    cuisines = z.get_cuisines(city_id)  # gets all cuisines
    print(cuisines)
    for c in cuisines:
        print(c.lower())
        if c.lower() == cuisine_name.lower():
            return cuisines[c]  # cuisine id (int)
    raise Exception("your cuisine {} cannot be found!".format(cuisine_name))  # raises exception if no match is found

# @login_required
def search(request):
    if request.POST:
        search_term = request.POST['search_term']        
        # TODO : logic to search the JSON cusines if contains not Restaurant Objects
        # or we can set one variable to all Restaurants here and filter on that JSON object
		# search_results = Resturant.objects.filter(cuisines__icontains=search_term)
		# OR if we need to do more criteria based search do following ways
        # search_results = Resturant.objects.filter(
        #     Q(name__icontains=search_term) | 
        #     Q(cuisines__icontains=search_term) |
        #     Q(highlights__icontains=search_term) |
        #     Q(phone__iexact=search_term)
        # )

        z = Zomato(key)
        # leads to error prone and messy search
        # cuisine_id = get_cuisine_id(search_term)  # gets cuisine id first for searching

        # searching by query directly that Zomato handles well
        cuisines = search_term  # this can be city name/s, comma separated string for multiple cuisines
        radius = 200  # radius within the current location in meters
        limit = 10  # number of restaurants to display
        search_results = z.restaurant_search(radius=radius, query=cuisines, limit=limit)

        print(search_results)

        context = {
            'search_term' : search_term,
            'restaurants': search_results
            # 'contacts': search_results.filter(manager = request.user)
        }
        return render(request, 'foodie_friend_app/search.html', context)
    else:
        return redirect('foodie_friend_app:home')