#finds last start date of a business [ID'd by name and address] and adds last opening entries for that business.
#new strategy -- find every address with an end date, and include everything with that address
import os
import csv
from datetime import datetime

file_time = datetime.now()
time_string = file_time.strftime('%Y-%m-%d_%H-%M-%S')
allsfbiz = os.path.join('..','..', '20150605sfbusinesses', 'Registered_Business_Locations_-_San_Francisco.csv')
startdatesfile = os.path.join('..','..','20150605sfbusinesses','round2results','cleaned_data_round2_{}.csv'.format(time_string))
cities = ['San Francisco', 'SAN FRANCISCO', '', 'SAN FRANCISO',  'SAN  FRANCISCO', 'SAN FRANICSCO', 'SAN FRANCSICO', 'SAN FRANACISCO', 'SAN FRACISCO', 'SAN FRANCISCI', 'SAN  FRACISCO', 'SAN FRANCISCCO', 'SAN FRANCISCQ', 'SAN FRANCISCOQ', 'SAM FRANCISCO', 'SAN FRAANCISCO', 'SAN FRANCISOCO', 'SAN FRANCISC', 'san francisco', 'SANFRANCISCO',  'SAN FRANCISCP', 'SAN FRNCISCO', 'SAN FRANCICO', 'SAN FRANCIASO',  'SAN FARNCISCO','SAN FRANCISCO CA',  'SAN FRANCISCSO', 'SAN FRANCICSO', 'SAN FRANCOSCO', 'SN AFRANCISCO', 'SN FRANCISCO']


def get_all_addresses_with_end_date(file_name):
	with open(file_name, 'rU') as fullsflist, open(startdatesfile,'wb') as results:
		total_with_end_dates = 0
		total_entries_added = 0
		sfdatareader = csv.DictReader(fullsflist)
		sfdatafieldnames = sfdatareader.fieldnames 
		writer = csv.DictWriter(results, sfdatafieldnames) 
		writer.writeheader()
		addresses_with_end_dates = []
		#find all addresses with an end date.
		for row in sfdatareader:
			address = row['Street_Address']
			enddate = True if (row['Location_End_Date'] or row["Business_End_Date"]) else False
			if enddate and (address not in addresses_with_end_dates):
				addresses_with_end_dates.append(address)
				total_with_end_dates += 1
		print "total end dates found: " + str(total_with_end_dates)
		#write all entries with those addresses (including those with no end date)
		fullsflist.seek(0)
		sfdatareader = csv.DictReader(fullsflist)
		for row in sfdatareader:
			if row['Street_Address'] in addresses_with_end_dates:
				writer.writerow(row)
				total_entries_added += 1
		print "total entries added: " + str(total_entries_added)

get_all_addresses_with_end_date(allsfbiz)



"""
with open(allsfbiz, 'rU') as fullsflist, open(startdatesfile,'wb') as results:
	sfdatareader = csv.DictReader(fullsflist)
	sfdatafieldnames = sfdatareader.fieldnames #+ ['Oldest_Start_Date_Sfdata', 'Newest_Start_Date_Sfdata', 'Newest_End_Date_Sfdata']
	allnameswriter = csv.DictWriter(results, sfdatafieldnames) 

	allnameswriter.writeheader()
	firststartdates = {}
	laststartdates = {}
	enddates = {}
	names = []
	addresses = []

	# gets and stores last start dates, first start dates, and last end dates for each entry in reader
	for row in sfdatareader:
		nameandaddress = row['DBA Name'] + " " + row['Street_Address'] # accounts for biz's with multiple addresses
		startdate = datetime.strptime(row['Business_Start_Date'], "%m/%d/%Y") if row['Business_Start_Date'] else None
		enddate = datetime.strptime(row['Location_End_Date'], "%m/%d/%Y") if row['Location_End_Date'] else None
		#if nameandaddress in all_names:
		if startdate and (nameandaddress not in firststartdates or startdate < firststartdates[nameandaddress]):
			firststartdates[nameandaddress] = startdate
		if startdate and (nameandaddress not in laststartdates or startdate > laststartdates[nameandaddress]):
			laststartdates[nameandaddress] = startdate
		if enddate and (nameandaddress not in enddates or enddate > enddates[nameandaddress]):
			enddates[nameandaddress] = enddate
	

	#stores names and addresses for all last start dates entries that also have a location end date or business end date. 
	fullsflist.seek(0)
	sfdatareader = csv.DictReader(fullsflist)
	for row in sfdatareader:
		nameandaddress = row['DBA Name'] + " " + row['Street_Address']
		bizid = row['Location_ID']
		startdate = datetime.strptime(row['Business_Start_Date'], "%m/%d/%Y")
		loc_enddate = datetime.strptime(row['Location_End_Date'], "%m/%d/%Y") if row['Location_End_Date'] else None
		biz_enddate = datetime.strptime(row['Business_End_Date'], "%m/%d/%Y") if row['Business_End_Date'] else None
		name = row['DBA Name']
		address = row['Street_Address']
		if (loc_enddate or biz_enddate) and startdate == laststartdates[nameandaddress] and row['City'] in cities:
			if name not in names:
				names.append(name)
			if address not in addresses:
				addresses.append(address)

	#goes through reader file and pulls all entries with matching name in names or matching address in addresses, writes to new file
	fullsflist.seek(0)
	sfdatareader = csv.DictReader(fullsflist)
	for row in sfdatareader:
		name = row['DBA Name']
		address = row['Street_Address']
		if name in names or address in addresses:
			#row['Oldest_Start_Date_Sfdata'] = firststartdates[nameandaddress]
			#row['Newest_Start_Date_Sfdata'] = laststartdates[nameandaddress]
			#row['Newest_End_Date_Sfdata'] = enddates[nameandaddress]
			allnameswriter.writerow(row)
			"""


