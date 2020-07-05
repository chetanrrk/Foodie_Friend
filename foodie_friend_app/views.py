"""
Created on Sun May 31 17:45:29 2020

@authors: chetanrupakheti,milson
"""

from django.shortcuts import render
import numpy as np
from matplotlib import pyplot as plt

from zomato import Zomato
import requests

z = Zomato("ef7a18bb9bda931d550f4965d60e5be7") ### zomato obj with key
common = z.common
location = z.location
restaurants = z.restaurant

cusines_map={} ### maps cusine name to its ID

def getRestaurant(id): ### id= int
        return restaurants.get_restaurant(id)

def getRestaurantLocation(restaurantObj,field="coords"): ## json obj
        return float(restaurantObj.restaurant.location.latitude),float(restaurantObj.restaurant.location.latitude)

def getRestaurantRating(restaurantObj):
	rating = float(obj.restaurant.user_rating.aggregate_rating) ### rating out of 5
	votes = int(obj.restaurant.user_rating.votes) ### number of votes
	price = obj.restaurant.average_cost_for_two/2.0 ### price for one
	return rating,votes,price

### find resturant with in a coord and cusines and return the ranking
### ranking (votes*rating + price)/sum_over_all_restaurants(votes*rating + price) 
### source: https://andrew.hedges.name/experiments/haversine/ ; Haversine Formula
def computeDistance(lat1,lon1,lat2,lon2):
        R = 3961 ## radius of earth in miles
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (np.sin(dlat/2.0))**2 + np.cos(lat1) * np.cos(lat2) * (np.sin(dlon/2))**2
        c = 2 * np.arctan2( np.sqrt(a), np.sqrt(1-a) )
        d = R * c
        return d ## distance in miles

###TODO: Newer resturants will have lower ratings.Need to normalize over time as well!!
def score(restaurantsList):
	votes=0
	tmp=[]
	tmpRes={}
	sortedResturants={} ### final rank based on normalized rating
	for restura in restaurantsList:
		resturaID,rating,votes,price = getRestaurantRating(restaura)
		tmp.append([resturaID,rating,price])
		totalVote+=votes
	
	for restura in tmp:
		resturaID,rating,price = restura[0],restura[1]/totalVote,restura[2]
		# finalList.append({"id":resturaID,"rating":rating,"price":price})
		tmpRes["id"] = {"rating":rating, "price":price}

		sortedRes = sorted(tmpRes.items(), key=lambda x: x[1][0], reverse=True) ###sorts based on normalized rating
		for r in sortedRes:
			sortedResturants[r[0]] = r[1]
			
		return sortedResturants
	
def getGeoCoords():
	ip_request = requests.get('https://get.geojs.io/v1/ip.json') 
	my_ip = ip_request.json()['ip'] 

	geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json' 
	geo_request = requests.get(geo_request_url) 
	geo_data = geo_request.json() 
	return geo_data['latitude'],geo_data['longitude'] ###lat,lon


def getCusineID(cuineName,latitude,longitude):
	if len(cusines_map)==0:
		res = common.get_cuisines(lat=latitude,lon=longitude)
		for r in res:
			cusines_map[r.cuisine_name.lower()]=r.cuisine_id  
	cusineID = cusines_map[cuineName.lower()]		
	return cusineID
	
### directly applying API's search function and modified ranking to list top choices 
def getCusines(city,state,cusine,radius): 
	"""
	### finds matching city ID first
	cities = common.get_cities(city)
	for i in range(len(cities)):
		c = cities[i].name.split(",")[0]
		s = cities[i].name.split(",")[1]
		if c.lower()==city.lower() and s.lower()==state.lower():
			cityID = cities[i].id ### city id
			break
	### fixing the cusine text just in case 
	cusine_temp = cusine.lower()### converting to the appropriate value in the field
	cusine_new = cusine_temp[0].upper()+cusine_temp[1:] 

	c=common.get_cuisines(cityID) ### 292 for Chicago
        """

	### efficient way to filter using API's search function
	#example: restaurant.search({"lat":41.8013895,"lon":-87.589538,"cuisines":25,"radius":20000}) 
	lat,lon = getGeoCoords() 
	cusineID = getCusineID(cusine, lat, lon) 
	restaurantList = restaurants.search({"lat":lat,"lon":lon,"cuisines":cusineID,"radius":radius}) 

	finalResult = score(restaurantsList)

	return finalResult ### sorted final resturant based on normalized ratings

def home(request):
	### efficient way to filter using API's search function
	#example: restaurant.search({"lat":41.8013895,"lon":-87.589538,"cuisines":25,"radius":20000}) 
	lat,lon = getGeoCoords()
	print(lat, lon)
	cusine = 25
	radius = 20000
	cusineID = getCusineID(cusine, lat, lon)	
	restaurantList = restaurants.search({"lat":lat,"lon":lon,"cuisines":cusineID,"radius":radius}) 

	finalResult = score(restaurantsList) ### sorted final resturant based on normalized ratings
	
	print(finalResult)

	context = {
        'menus' : 'abc',
		'result': finalResult
    }
	return render(request, 'foodie_friend_app/index.html', context)