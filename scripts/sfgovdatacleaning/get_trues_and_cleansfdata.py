import csv
import pprint
import os
from datetime import datetime

with open('by_name_full-2015-04-24.csv', 'rU') as readfile, open('trues_only.csv', 'wb') as outputfile:
	reader = csv.DictReader(readfile)
	bynamefieldnames = reader.fieldnames
	truesonlywriter = csv.DictWriter(outputfile, bynamefieldnames)

	truesonlywriter.writeheader()
	all_names = []
	names_with_true_found = []
	names_none_found = []

	n = 0
	for row in reader:
		#pprint.pprint(row)
		n += 1
		dba_name = row['DBA Name sfdata']
		if dba_name not in all_names:
			all_names.append(dba_name)
		closedstatus = row['is_closed']
		if closedstatus != "False":
			print row['address'], type(row['address'])
			truesonlywriter.writerow(row)
			if dba_name not in names_with_true_found:
				names_with_true_found.append(dba_name)

	for name in all_names:
		if name not in names_with_true_found:
			names_none_found.append(name)

	allsfbiz = os.path.join('20150422_Registered_Business_Locations_-_San_Francisco.csv')

	with open(allsfbiz, 'rU') as fullsflist, open('sfdata_yelpfound.csv', 'wb') as sfdata_yelpfound:
		sfdatareader = csv.DictReader(fullsflist)
		sfdatafieldnames = sfdatareader.fieldnames + ['Oldest_Start_Date_Sfdata', 'Newest_Start_Date_Sfdata', 'Newest_End_Date_Sfdata']
		allnameswriter = csv.DictWriter(sfdata_yelpfound, sfdatafieldnames) 

		allnameswriter.writeheader()

		firststartdates = {}
		laststartdates = {}
		enddates = {}


		# not working properly. maybe need to double-check by address for name changes? currently using location end date rather than bus end date
		for row in sfdatareader:
			bizname = row['DBA Name']
			bizid = row['Location_ID']
			startdate = datetime.strptime(row['Business_Start_Date'], "%m/%d/%y") if row['Business_Start_Date'] else None
			enddate = datetime.strptime(row['Location_End_Date'], "%m/%d/%y") if row['Location_End_Date'] else None
			#if bizname in all_names:
			if startdate and (bizname not in firststartdates or startdate < firststartdates[bizname]):
				firststartdates[bizname] = startdate
			if startdate and (bizname not in laststartdates or startdate > laststartdates[bizname]):
				laststartdates[bizname] = startdate
			if enddate and (bizname not in enddates or enddate > enddates[bizname]):
				enddates[bizname] = enddate

		fullsflist.seek(0)
		sfdatareader = csv.DictReader(fullsflist)
		for row in sfdatareader:
			bizname = row['DBA Name']
			bizid = row['Location_ID']
			startdate = datetime.strptime(row['Business_Start_Date'], "%m/%d/%y")
			enddate = datetime.strptime(row['Location_End_Date'], "%m/%d/%y") if row['Location_End_Date'] else None
			if bizname in enddates:
				if enddate and (enddates[bizname] > laststartdates[bizname]):
					row['Oldest_Start_Date_Sfdata'] = firststartdates[bizname]
					row['Newest_Start_Date_Sfdata'] = laststartdates[bizname]
					row['Newest_End_Date_Sfdata'] = enddates[bizname]
					allnameswriter.writerow(row)



	# find all start times for a business, and if any are later than all of the end times, take it out of the list
