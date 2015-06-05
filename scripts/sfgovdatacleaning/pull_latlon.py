
import os
import csv
from datetime import datetime


file_time = datetime.now()
time_string = file_time.strftime('%Y-%m-%d_%H-%M-%S')
refined_data = os.path.join('..','..','20150407sfbusinesses','lateststartdatesentries','refiningrefined2015-04-29_13-41-24.csv')
splitoutlat = os.path.join('..','..','20150407sfbusinesses','lateststartdatesentries','splitoutlat{}.csv'.format(time_string))

with open(refined_data, 'rU') as refined, open(splitoutlat,'wb') as splitlat:
	refinedreader = csv.DictReader(refined)
	refinedreaderfieldnames = refinedreader.fieldnames + ['latitude'] + ['longitude']
	allnameswriter = csv.DictWriter(splitlat, refinedreaderfieldnames)

	allnameswriter.writeheader()

	for row in refinedreader:
		if "(" in row['Business_Location']:
			latlon = row['Business_Location'].split('(')[1][0:-1]
		else:
			latlon = None
		if latlon:
			latitude, longitude = latlon.split(", ")
		row['latitude'] = latitude
		row['longitude'] = longitude
		allnameswriter.writerow(row)


