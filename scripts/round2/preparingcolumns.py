#splits out first numbers of address, street, and last numbers if present (isolating street names)
import os
import csv
from datetime import datetime

file_time = datetime.now()
time_string = file_time.strftime('%Y-%m-%d_%H-%M-%S')
allsfbiz = os.path.join('..','..', '20150605sfbusinesses', 'Registered_Business_Locations_-_San_Francisco.csv')
startdatesfile = os.path.join('..','..','20150605sfbusinesses','round2results','colums_split_round2_{}.csv'.format(time_string))
cities = ['San Francisco', 'SAN FRANCISCO', '', 'SAN FRANCISO',  'SAN  FRANCISCO', 'SAN FRANICSCO', 'SAN FRANCSICO', 'SAN FRANACISCO', 'SAN FRACISCO', 'SAN FRANCISCI', 'SAN  FRACISCO', 'SAN FRANCISCCO', 'SAN FRANCISCQ', 'SAN FRANCISCOQ', 'SAM FRANCISCO', 'SAN FRAANCISCO', 'SAN FRANCISOCO', 'SAN FRANCISC', 'san francisco', 'SANFRANCISCO',  'SAN FRANCISCP', 'SAN FRNCISCO', 'SAN FRANCICO', 'SAN FRANCIASO',  'SAN FARNCISCO','SAN FRANCISCO CA',  'SAN FRANCISCSO', 'SAN FRANCICSO', 'SAN FRANCOSCO', 'SN AFRANCISCO', 'SN FRANCISCO']




def split_address(street_address):
		# split out into 3 columns, leading numbers, street names, ending numbers
		words = street_address.split()
		ldnums = words[0] if words[0] else ""
		words = words[1:] if words[1] else ""
		last = ""

		street_types = ["AVE", "ST", "BLVD", "STREET", "BOULEVARD", "AVENUE", "BL", "WAY", "LN", "ALY", "CTR", "RD", "LANE", "ROAD", "ST.", "BUILDING", "BLDG"]

		num_count = 0
		for char in ldnums:
			if char in "01234567890#":
				num_count += 1
		
		if num_count == 0:
			words = [ldnums] + words
			ldnums = ""

		for word in words:
			if word.upper() in street_types:
				split_index = words.index(word) + 1
				last = words[split_index:]
				words = words[0:split_index]
				break

		words = ' '.join(words)
		last = ' '.join(last)

		return ldnums, words, last



def get_all_addresses_with_end_date(file_name):
	#reads in main file and writes out with extra fields for split street names
	with open(file_name, 'rU') as reader, open(startdatesfile,'wb') as writer:

		reader = csv.DictReader(reader)
		fieldnames = reader.fieldnames + ['leadnums', 'address_words', 'endnums']
		writer = csv.DictWriter(writer, fieldnames) 
		writer.writeheader()

		i = 0

		for row in reader:
			if i < 1000:
				ldnums, words, endnums = split_address(row['Street_Address'])
				row['leadnums'] = ldnums
				row['address_words'] = words
				row['endnums'] = endnums
				writer.writerow(row)
			i+=1


get_all_addresses_with_end_date(allsfbiz)
