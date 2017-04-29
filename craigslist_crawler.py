'''
Craigslist web crawler to complile data for residentail rental market.
Will need:
- Web crawler to pull links for each listing from main page (and next page)
- redundancy checker
- data to pull:
	- date of listing
	- rent $ per month
	- address / location
	- property size (sf) if available
	- bed / bath count

POSSIBLE ISSUES:
- Need to figure out how to handle dates in the json/bson file. 
- the craigslist web page has map or list options dropdown.  The crawler may not work
if map is selected (has not been an issue so far though). 
'''

'''Craigslists shows links for each listing inside of list of items (li) in the html. 
Each has an item number.  
With the item numbers the links can be recreated in the url.
example https://sandiego.craigslist.org/csd/apa/6108616530.html  6108616530 is the item number. 

Repost is shown in the list item as data-repost-of='old_item#'
'''

from bs4 import BeautifulSoup
import urllib
import json
import os

starting_link = 'https://sandiego.craigslist.org/search/apa'

json_file_name = r'craigslist_rental_data.json'

'''
# Pull list of craigslist id #'s.  
with open(json_file_name, 'r') as read_file:
	data = json.load(read_file)
	print data
'''


json_file = open(json_file_name, 'a+')

def remove_bracket_close():
	'''Removes the closing bracket from an existing json file, 
	in order to append new records.'''
	with open(json_file_name, 'rb+') as edit_file:
		edit_file.seek(-1, os.SEEK_END)
		edit_file.truncate()
		edit_file.write(',' + os.linesep)


def craiglist_id_list():
	with open(json_file_name, 'r') as read_file:
		data = json.load(read_file)
		print data

pages_scraped = 0

def pull_page_data(starting_link, pages_to_pull, pages_scraped, new_file=True):
	''' Find all of the rental items on the craigslist. Scare data and dump to json file.'''
	
	if new_file and pages_scraped == 0:
		json_file.write('[')
	elif new_file == False and pages_scraped == 0:
		remove_bracket_close()

	html_doc = urllib.urlopen(starting_link)

	soup = BeautifulSoup(html_doc, 'html.parser')

	for item in soup.find_all('li', class_="result-row"):
		json_row = {}
		
		# Exclude the reposts. 
		if item.get('data-repost-of') == None:
				
			json_row['listing_date'] = item.find('time').get('datetime')
			json_row['craigslist_id'] = item.get('data-pid')

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
			
			address = item.find('span', class_='result-hood')

			# In some cases there is more location information on the item's spacific page. 
			if address != None:
				open_bracket_indx = address.text.index('(')
				close_bracket_indx = address.text.index(')')
				json_row['General_Address'] = address.text[open_bracket_indx + 1: close_bracket_indx]

			# Write the dictionary to file, then a new line. 
			json.dump(json_row, json_file)
			json_file.write(',' + os.linesep)
			#json_file.write(os.linesep)
			
			#json_file.write('\n')
			

			#save_to_file(json_row)
	# Find the next page link.
	pages_scraped += 1

	next_link = 'https://sandiego.craigslist.org' + soup.find('a', class_="button next").get('href')

	html_doc.close()

	
	if pages_scraped < pages_to_pull:
		pull_page_data(next_link, pages_to_pull, pages_scraped)
	else:
		json_file.close()
		# Remove the last comma from the file and add the closing bracket. 
		with open(json_file_name, 'rb+') as json_file_edit:
			json_file_edit.seek(-2, os.SEEK_END)
			json_file_edit.truncate()
			json_file_edit.write(']')
			json_file_edit.close()	


pull_page_data(starting_link, 4, pages_scraped, new_file=False)
#craiglist_id_list()	



