import urllib
import json
import urllib.parse
import urllib.request

googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'

def get_coordinates2(query, from_sensor=False):
	query = query.encode('utf-8')
	params = {
		'address': query,
		'sensor': "true" if from_sensor else "false"
	}
	url = googleGeocodeUrl + urllib.parse.urlencode(params)
	#print(url)
	json_response = urllib.request.urlopen(url)
	#print(json_response)
	response = json.loads(json_response.read().decode('utf-8'))
	if response['results']:
		location1 = response['results'][0]['geometry']['bounds']['northeast']
		latitude1, longitude1 = location1['lat'], location1['lng']
		location2 = response['results'][0]['geometry']['bounds']['southwest']
		latitude2, longitude2 = location2['lat'], location2['lng']
		
	else:
		latitude, longitude = None, None
		#print (query, "<no results>")
	return latitude1, longitude1,latitude2,longitude2

Nepal_coordinates=get_coordinates2('Nepal')
#print(Nepal_coordinates[0])

def get_coordinates(query, from_sensor=False):
	query = query.encode('utf-8')
	params = {
		'address': query,
		'sensor': "true" if from_sensor else "false"
	}
	url = googleGeocodeUrl + urllib.parse.urlencode(params)
	#print(url)
	json_response = urllib.request.urlopen(url)
	#print(json_response)
	response = json.loads(json_response.read().decode('utf-8'))
	if response['results']:
		location = response['results'][0]['geometry']['location']
		latitude, longitude = location['lat'], location['lng']
		#print (query, latitude, longitude)
	else:
		latitude, longitude = None, None
		#print (query, "<no results>")
	return latitude, longitude



def is_inside_Nepal(query):
	coordinates=get_coordinates(query)
	#print(coordinates)
	if Nepal_coordinates[2]<=coordinates[0] and coordinates[0]<= Nepal_coordinates[0] and Nepal_coordinates[3]<=coordinates[1] and coordinates[1]<= Nepal_coordinates[1]:
		#print("Valid")
		return 1
	else:
		#prin3t("Invalid")	
		return 0

#print(is_inside_Nepal('Sindhupalchok'))