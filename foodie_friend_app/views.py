"""
Created on Sun May 31 17:45:29 2020

@authors: chetanrupakheti, milson
"""

from django.shortcuts import render
import numpy as np
from matplotlib import pyplot as plt

from zomato import Zomato
import requests
import json


z = Zomato("ef7a18bb9bda931d550f4965d60e5be7")  # zomato obj with key
common = z.common
location = z.location
restaurants = z.restaurant

cusines_map = {}  # maps cusine name to its ID


def getRestaurant(id):  # id = int
    """
    Returns a restaurant's details
    @params id: restautant
    @return: json object of restaurant
    """

    return restaurants.get_restaurant(id)


def getRestaurantLocation(restaurantObj):  # json obj
    """
    @param: restaurant object
    @return: latitude and longitude of a restaurant
    """

    return float(restaurantObj.restaurant.location.latitude), \
           float(restaurantObj.restaurant.location.latitude)


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


def computeDistance(lat1, lon1, lat2, lon2):
    """
    computes distance between two coordinates
    @params
    lat1, lon1: latitude and longitude of start point
    lat2, lon2: latitude and longitude of end point
    @return: distance in miles
    source: https://andrew.hedges.name/experiments/haversine/ ; Haversine Formula
    """

    R = 3961  # radius of earth in mile
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (np.sin(dlat / 2.0)) ** 2 + np.cos(lat1) * np.cos(lat2) * (np.sin(dlon / 2)) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    d = R * c
    return d


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


def getGeoCoords():
    """
    captures latitude and longitude based on current location
    @params: None
    @return: latitude, longitude
    """

    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']
    geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
    geo_request = requests.get(geo_request_url)
    geo_data = geo_request.json()
    return geo_data['latitude'], geo_data['longitude']  # latitude, longitude


def getCusineID(cusineName, latitude, longitude):
    """
    Given a cusine name and current location, returns its zomato cusineID.
    Needed for searching restaurants information
    @params
    cusineName: string, name of the cusing, for example: "indian"
    latitude: current latitude
    longitude: current longitude
    @return
    cusnieID: int number in string format
    """

    if len(cusines_map) == 0:  # checks if cusines_map is already populated
        res = common.get_cuisines(lat=latitude, lon=longitude)
        for r in res:
            cusines_map[r.cuisine_name.lower()] = r.cuisine_id
    cusineID = cusines_map[cusineName.lower()]
    return cusineID


def home(request):
    """
    Main function that gets called
    @param: request object of cusine type
    @return: ranked list of restaurants based on normalized ratings
    example: restaurant.search({"lat":41.8013895,"lon":-87.589538,"cuisines":25,"radius":20000})
    """

    lat, lon = getGeoCoords()  # test example 41.801050, -87.590250
    # print(lat, lon)
    cusine_name = "Italian"  # cusine name for now
    radius = 20000  # test radius in meters for now
    cusineID = getCusineID(cusine_name, lat, lon)
    # print("cusineID {}".format(cusineID))

    """ searching based on current geo location, cusineID, and search radius in meters"""
    restaurantList = restaurants.search({"lat": lat, "lon": lon, "cuisines": cusineID, "radius": radius})

    """sorted final restaurant based on normalized ratings in json format"""
    finalResult = json.dumps(score(restaurantList), indent=4)

    # finalResult = score(restaurantList)  # results as regular dictionary
    # for r in finalResult:
    #    print("name {} \n address {}".format(finalResult[r]['name'], finalResult[r]['address']))

    """Rendering the final results"""
    context = {
        'menus': 'abc',
        'result': restaurantList #finalResult
    }

    return render(request, 'foodie_friend_app/index.html', context)
