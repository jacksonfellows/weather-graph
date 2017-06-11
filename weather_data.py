import requests, json, datetime
import matplotlib.pyplot as plt
import numpy as np

dates = []

def get_temps(start, end): # returns two numpy arrays of the min and max temperatures for the given date range
	make_dates = False
	if dates == []:
		make_dates = True

	# some constants for using the NOAA API
	DATASET = 'GHCND'
	DATATYPES = ['TMIN', 'TMAX']
	STATION_ID = 'GHCND:USW00094290'
	LIMIT = '1000'
	UNITS = 'standard'
	TOKEN = 'dFsdbxejVbzhOrTcHJQBXktpmkGkdqQT'

	params = {'datasetid': DATASET, 'datatypeid': DATATYPES, 'stationid': STATION_ID, 'limit': LIMIT, 'units': UNITS, 'startdate': start, 'enddate': end}
	HEADER = {'token': TOKEN}

	response = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data', params = params, headers = HEADER) # the arguments params and headers are automatically added to the url
	
	data = json.loads(response.text) # parse the json of the response

	mins, maxs = [], []

	# looping through JSON is intuitive
	for i in data['results']: # for every item of data
		temp = i['value']
		if i['datatype'] == 'TMIN': # if it's a min
			mins.append(temp) # add it to the min list
			if make_dates:
				dates.append(i['date'][5:10])
		else: # otherwise
			maxs.append(temp) # add it to the max list

	return np.array(mins), np.array(maxs) # convert these standard lists to numpy objects


date = datetime.date(2017, 5, 15) # first date of the week of the most current year
last_year = 2000 # display data back to this year

num_years = date.year - last_year + 1
week_inc = datetime.timedelta(6) # when added to a date object, they will cover one week

width = .8/num_years

x = np.arange(7) # here, numpy creates a data structure with [0, 1, 2 ... 6]

bars, years = [], []

while date.year >= last_year:
	mins, maxs = get_temps(date, date + week_inc) # note clear Python syntax for a function that returns multiple arguments

	offset = .8 - (width * len(years)) - width
	color = len(years) / num_years

	bar = plt.bar(x + offset, maxs - mins, bottom = mins, color = plt.cm.Set1(color), width = width) # create all of the bars for one year
	# x + offset -> this is numpy's syntax for adding a value to every item in an array
	# maxs - mins -> numpy's syntax for subtracting every value in maxs by its corresponding value in mins

	bars.append(bar)
	years.append(date.year)

	date = date.replace(year = date.year - 1)

# format the plot
plt.title('Daily Temperature Ranges For The Same Week Over Multiple Years (Data From The Sand Point Weather Station in Magnuson Park, Seattle)')
plt.ylabel('Temperature (Degrees Fahrenheit)')
plt.xlabel('Day')
plt.legend(bars, years)
plt.xticks(x, dates)

# and display it
plt.show()