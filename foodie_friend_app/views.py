"""
Created on Sun May 31 17:45:29 2020

@authors: chetanrupakheti, milson
"""

from django.shortcuts import render
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

    print(restaurants)

    """Rendering the final results"""
    context = {
        'menus': 'abc',
        'result': restaurants #finalResult
    }

    return render(request, 'foodie_friend_app/index.html', context)
