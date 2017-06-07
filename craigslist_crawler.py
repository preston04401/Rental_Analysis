#!/usr/bin/python
'''
File to be called with the following options input with the job call:

-s or --start_site (followed by) 'name of the webpage for the crawler to begin'
-j or --json_file 'name of the json file to be created or appended'
-n or --new_file 'true/t if the json file is to be created, false/f otherwise'

Craigslist web crawler to complile data for residentail rental market.
Will need:
- redundancy checker: create a csv file for faster data handling?

POSSIBLE ISSUES:
- Need to figure out how to handle dates in the json/bson file. 
- the craigslist web page has map or list options dropdown.  The crawler may not work
if map is selected (has not been an issue so far though). 
'''

'''
Repost is shown in the list item as data-repost-of='old_item#'
'''

from bs4 import BeautifulSoup
import urllib
import json
import os, sys, getopt
import detail_page_scraper

# Default starting link to be rewriten below with args from file call statement. 
starting_link = 'https://sandiego.craigslist.org/search/apa'

# Default json file name to be rewriten below with args from file call statement. 
json_file_name = r'craigslist_rental_data.json'

# new_file to be rewritten as boolean below.
new_file = False

# getopts to update above variables based on file call statement with cron job. 
try:
	opts, args = getopt.getopt(sys.argv[1:], "-s:-j:-n:", ["start_site=", "json_file=", "new_file="])
except getopt.GetoptError:
	"Error with getopt on job call"
	sys.exit(2)

for opt, arg in opts:
	if opt in ["-s", "--start_site"]:
		starting_link = arg
	elif opt in ["-j", "--json_file"]:
		json_file_name = arg
	elif opt in ["-n", "--new_file"]:
		if "T" in arg or "t" in arg:
			new_file = True
		else:
			new_file = False

def remove_bracket_close():
	'''Removes the closing bracket from an existing json file, 
	in order to append new records.'''
	with open(json_file_name, 'rb+') as edit_file:
		edit_file.seek(-1, os.SEEK_END)
		edit_file.truncate()
		edit_file.write(',' + os.linesep)

def craiglist_id_list():
	'''Compiles and returns the craigslist listing ids that are in the json file.'''
	id_list = []
	with open(json_file_name, 'r') as read_file:
		data = json.load(read_file)
		for i in data:
			id_list.append(i['craigslist_id'])
	return id_list

try:
	craiglist_ids = craiglist_id_list()
except:
	craiglist_ids = []

pages_scraped = 0

def pull_page_data(starting_link, pages_scraped, new_file=True):
	''' Find all of the rental items on the craigslist. Scare data and dump to json file.'''
	global json_file
	# Check to ensure that user actually wants to overwrite data if that is what is happening. 
	cwd = os.getcwd()
	current_files = os.listdir(cwd)

	if new_file and json_file_name in current_files and pages_scraped == 0:
		overwrite_confirm = raw_input('Are you sure you want to overwrite ' + \
			json_file_name + '(y/n)?')

		if overwrite_confirm.find('y') == -1 and overwrite_confirm.find('Y') == -1:
			print 'Operation terminated by user'
			quit()

	if (pages_scraped == 0):
		json_file = open(json_file_name, 'a+')
	
	# check if appending a json file or creating new. 
	if new_file and pages_scraped == 0:
		json_file.write('[')
	elif new_file == False and pages_scraped == 0:
		remove_bracket_close()

	html_doc = urllib.urlopen(starting_link)

	soup = BeautifulSoup(html_doc, 'html.parser')

	for item in soup.find_all('li', class_="result-row"):
		json_row = {}
		
		# Exclude the reposts and items already in json file. 
		if item.get('data-repost-of') == None and \
		item.get('data-pid') not in craiglist_ids:

			json_row['listing_date'] = item.find('time').get('datetime')
			
			craigslist_id = item.get('data-pid')
			json_row['craigslist_id'] = craigslist_id

			meta_data = item.find('span', class_='result-meta')

			price = meta_data.find('span', class_='result-price')

			# Append the json if the data is present. 
			if price != None:
				json_row['Rent_price'] = int(price.text[1:])

			size = meta_data.find('span', class_='housing')

			if size != None:
				size_text = size.text
				# Check for bedroom count and add to json. 
				try:
					br_index = size_text.index('br')
					bedrooms = size_text[br_index - 2: br_index]
					json_row['Num_Bedrooms'] = int(bedrooms)
				except:
					pass
				# Check for square footage and add to json
				try:
					ft_index = size_text.index('ft')
					square_feet = size_text[ft_index - 6 : ft_index]
					json_row['Square_feet'] = int(square_feet)
				except:
					pass
			
			address_1 = item.find('span', class_='result-hood')

			# In some cases there is more location information on the item's spacific page. 
			if address_1 != None:
				open_bracket_indx = address_1.text.index('(')
				close_bracket_indx = address_1.text.index(')')
				json_row['General_Address'] = \
				address_1.text[open_bracket_indx + 1: close_bracket_indx]

			# Find the link to details.
			end_link = item.find('a').get('href')
			craigslist_index = starting_link.index('.org')
			standard_lnk = starting_link[:craigslist_index + 4]
			full_link = standard_lnk + end_link

			json_row['link'] = full_link

			# Pull the details from the linked detail property page. 
			# @return = [latitude, longitue, title, address, attributes, text, map_accuracy]
			details = detail_page_scraper.scrape_details(craigslist_id, full_link)

			json_row['latitude'] = details[0]
			json_row['longitue'] = details[1]
			json_row['title'] = details[2]
			json_row['address_2'] = details[3]
			json_row['attributes'] = details[4]
			json_row['text'] = details[5]
			json_row['map_accuracy'] = details[6]

			# Write the dictionary to file, then a new line. 
			json.dump(json_row, json_file)
			json_file.write(',' + os.linesep)
	
	# Find the next page link.
	pages_scraped += 1

	next_page_button = soup.find('a', class_="button next")

	if next_page_button:
		next_link = 'https://sandiego.craigslist.org' + \
		next_page_button.get('href')

		html_doc.close()
		print "Page completed"+str(pages_scraped)
		pull_page_data(next_link, pages_scraped)
	else:
		# Close the file if there are no more pages. 
		json_file.close()
		html_doc.close()
		print "Last Page completed"+str(pages_scraped)
		# Remove the last comma from the file and add the closing bracket. 
		with open(json_file_name, 'rb+') as json_file_edit:
			json_file_edit.seek(-2, os.SEEK_END)
			json_file_edit.truncate()
			json_file_edit.write(']')

	print 'script complete'

pull_page_data(starting_link, pages_scraped, new_file)
