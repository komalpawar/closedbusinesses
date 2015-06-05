
import argparse
import json
import pprint
import sys
import urllib
import urllib2
import csv
from datetime import datetime
import os.path

import oauth2


API_HOST = 'api.yelp.com'
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
with open('keys.json', 'rb') as key_file:
	KEYS = json.load(key_file)

CONSUMER_KEY = str(KEYS['CONSUMER_KEY'])
CONSUMER_SECRET = str(KEYS['CONSUMER_SECRET'])
TOKEN = str(KEYS['TOKEN'])
TOKEN_SECRET = str(KEYS['TOKEN_SECRET'])



def request(host, path, url_params=None):

    url_params = url_params or {}
    url = 'http://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()
    print signed_url
    
    print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    response_data = conn.read()

    try:
        response = json.loads(response_data)
    finally:
        conn.close()

    return response

def search(offset): #

    location = "San Francisco CA"
    term = "galaxy granite inc"


    url_params = {
    	'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': 20,
        'offset': offset,
        #'bounds':'37.767794,-122.431304|37.765734,-122.427735',
        ##'radius_filter':'100',
        ##'sort':'2'
    } 
    results = request(API_HOST, SEARCH_PATH, url_params=url_params)
    return results['businesses']

def prep_dict(p):

	new_list = []

	for item in p:
		item_dict = {}
		for entry in item:
			if isinstance(item[entry], dict):
				for key, value in item[entry].iteritems():
					item_dict[key] = value.encode('utf-8') if isinstance(value, unicode) else value
			else:
				item_dict[entry] = item[entry].encode('utf-8') if isinstance(item[entry], unicode) else item[entry]
		new_list.append(item_dict)

	return new_list

def get_field_names(bizlist):

	fieldnames = []
		
	for bus in bizlist[0:20]:
		for v in bus:
			if v not in fieldnames:
				fieldnames.append(v)

	return fieldnames


def main():
	file_time = datetime.now()
	time_string = file_time.strftime('%Y-%m-%d_%H-%M-%S')
	csvfilename = os.path.join('business_csvs','businesses-{}.csv'.format(time_string))

	with open(csvfilename, 'wb') as csvfile:
		offset = 0
		offset_increment = 20
		number_to_fetch = 20
		first_batch = True
		writer = None

		while offset < number_to_fetch:
			bizlist = prep_dict(search(offset))
			if first_batch:
				fieldnames = get_field_names(bizlist)
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
				writer.writeheader()
				first_batch=False
			for row in bizlist:
				writer.writerow(row)
			offset += offset_increment


if __name__ == "__main__":
	main()

