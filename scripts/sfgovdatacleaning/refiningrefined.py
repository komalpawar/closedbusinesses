#finds last start date of a business and adds last opening entries
import os
import csv
from datetime import datetime



file_time = datetime.now()
time_string = file_time.strftime('%Y-%m-%d_%H-%M-%S')
allsfbiz = os.path.join('..','..','20150407sfbusinesses','lateststartdatesentries','refined_lateststartdates_entries_sfdata_2015-04-29_00-18-03.csv')
startdatesfile = os.path.join('..','..','20150407sfbusinesses','lateststartdatesentries','refiningrefined{}.csv'.format(time_string))

with open(allsfbiz, 'rU') as fullsflist, open(startdatesfile,'wb') as results:
	sfdatareader = csv.DictReader(fullsflist)
	sfdatafieldnames = sfdatareader.fieldnames + ['Oldest_Start_Date_Sfdata', 'Newest_Start_Date_Sfdata', 'Newest_End_Date_Sfdata']
	allnameswriter = csv.DictWriter(results, sfdatafieldnames) 

	allnameswriter.writeheader()
	firststartdates = {}
	laststartdates = {}
	enddates = {}

	# not working properly. maybe need to double-check by address for name changes? currently using location end date rather than bus end date
	for row in sfdatareader:
		nameandaddress = row['DBA Name'] + " " + row['Street_Address'] # accounts for biz's with multiple addresses
		bizid = row['Location_ID']
		startdate = datetime.strptime(row['Business_Start_Date'], "%m/%d/%y") if row['Business_Start_Date'] else None
		locend = datetime.strptime(row['Location_End_Date'], "%m/%d/%y") if row['Location_End_Date'] else None
		bizend = datetime.strptime(row['Business_End_Date'], "%m/%d/%y") if row['Business_End_Date'] else None
		enddate = bizend or locend
		#if nameandaddress in all_names:
		if startdate and (nameandaddress not in firststartdates or startdate < firststartdates[nameandaddress]):
			firststartdates[nameandaddress] = startdate
		if startdate and (nameandaddress not in laststartdates or startdate > laststartdates[nameandaddress]):
			laststartdates[nameandaddress] = startdate
		if enddate and (nameandaddress not in enddates or enddate > enddates[nameandaddress]):
			enddates[nameandaddress] = enddate
	
	#cities = ['San Francisco', 'SAN FRANCISCO', '', 'SAN FRANCISO',  'SAN  FRANCISCO', 'SAN FRANICSCO', 'SAN FRANCSICO', 'SAN FRANACISCO', 'SAN FRACISCO', 'SAN FRANCISCI', 'SAN  FRACISCO', 'SAN FRANCISCCO', 'SAN FRANCISCQ', 'SAN FRANCISCOQ', 'SAM FRANCISCO', 'SAN FRAANCISCO', 'SAN FRANCISOCO', 'SAN FRANCISC', 'san francisco', 'SANFRANCISCO',  'SAN FRANCISCP', 'NORTH HIGHLAND', 'SAN FRNCISCO', 'SAN FRANCICO', 'SAN FRANCIASO',  'SAN FARNCISCO','SAN FRANCISCO CA',  'SAN FRANCISCSO', 'SAN FRANCICSO', 'SAN FRANCOSCO', 'SN AFRANCISCO', 'SN FRANCISCO']

	fullsflist.seek(0)
	sfdatareader = csv.DictReader(fullsflist)
	for row in sfdatareader:
		nameandaddress = row['DBA Name'] + " " + row['Street_Address']
		bizid = row['Location_ID']
		startdate = datetime.strptime(row['Business_Start_Date'], "%m/%d/%y")
		loc_enddate = datetime.strptime(row['Location_End_Date'], "%m/%d/%y") if row['Location_End_Date'] else None
		biz_enddate = datetime.strptime(row['Business_End_Date'], "%m/%d/%y") if row['Business_End_Date'] else None
		strippedcity = (row['City'].strip("")).lower()
		if (biz_enddate or loc_enddate) and startdate == laststartdates[nameandaddress]:
				row['Oldest_Start_Date_Sfdata'] = firststartdates[nameandaddress]
				row['Newest_Start_Date_Sfdata'] = laststartdates[nameandaddress]
				#row['Newest_End_Date_Sfdata'] = enddates[nameandaddress]
				allnameswriter.writerow(row)

