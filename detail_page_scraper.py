'''
Web Scraper to pull the details from a rental property listing on craigslist.
To be used in conjunction with the web crawler in the craigslist_rental_data.py file, 
which data will be returned to. 

To Pull:
- Attributes: apartment / house / condo, guarage, laundery. 
- jpegs
- coordinates
'''

from bs4 import BeautifulSoup
import urllib
import requests
import json
import os

#craigslist_standard_url = 'https://sandiego.craigslist.org/'

#test_property_id = '6112538066'  #'6108245215'

#test_url = 'https://sandiego.craigslist.org/csd/apa/6088195803.html'

def save_jpgs(property_id, image_count, img_link):
	'''
	Save the jpgs to a new file, filename the same as the property id. 
	'''
	# File path for jpegs.
	cwd = os.getcwd()

	# Create a sub folder for each property. 
	jpeg_path = cwd + '/jpegs/' + property_id

	if not os.path.exists(jpeg_path):
		os.makedirs(jpeg_path)

	file_name = property_id + '_' + str(image_count) + '.jpg'
				
	path_file_name = jpeg_path + '/' + file_name

	# Create the new jpg file
	img_file = open(path_file_name, 'wb')

	# Load the picture and write it to the jpeg file. 
	img_file.write(requests.get(img_link).content)
	
	img_file.close()

def scrape_details(property_id, link):
	'''
	Pull information from the detail page, and call the jpg file saving function (above)
	return [latitude, longitude, ]
	@param property_id = the property id that craigslist uses.
	@return = [latitude, longitude, address, title, attributes, text] 
	attributes are a list drawn from the attribute spans and 
	text is the text from the main section
	'''

	html_doc = urllib.urlopen(link)
	
	soup = BeautifulSoup(html_doc, 'html.parser')

	# Save the latitude and longitude of the property. 
	map_div = soup.find(id='map')

	if map_div != None:
		latitude = map_div.get('data-latitude')
		longitue = map_div.get('data-longitude')
	else:
		latitude = None
		longitue = None

	# Scape all of the thumb images. 
	image_links = soup.find_all('a', class_='thumb')
	
	# Test for multiple thumbs. 
	if image_links != []:

		image_count = 0

		for i in image_links:
			image_count += 1

			img_link = i['href']
			if img_link != None:  # why does this not work???
				save_jpgs(property_id, image_count, img_link)
	
	# If there are no thumbnails but only one image scape the one.
	else:
		try:
			img = soup.find('img')
			img_link = img['src']

			save_jpgs(property_id, 1, img_link)	
		except:
			pass

	# Pull the title of the listing.
	try:
		title = soup.find(id='titletextonly').get_text()
	except:
		title = None

	# Pull the address.
	try:
		address = soup.find('div', class_='mapaddress').get_text()
	except:
		address = None
	
	# Pull attributes.
	attributes = []
	try:
		attributes_groups = soup.find_all('p', class_='attrgroup')

		# Add attributes from html to the list. 
		for a in attributes_groups:
			spans = a.find_all('span')
			for s in spans:
				attributes.append(s.get_text())
	except:
		pass

	# Pull text from the page. 
	try:
		text = soup.find(id='postingbody').get_text()
	except:
		text = None

	'''
	Would it be better to do an analysis on what attributes contribute after we have 
	a data set instead of trying to determine if we have a couple now???

	for a in attributes:
		# Parking keywords: carport, off-street parking, attached garage, detached garage, street parking
		if a.find('garage') != -1:
			print 'has garage'
		else:
			print 'no garage'
	'''

	html_doc.close()

	return [latitude, longitue, title, address, attributes, text]

#print scrape_details('6112538066', test_url)

#pic = urllib.urlretrieve('https://images.craigslist.org/01616_46rnDqsiSKE_600x450.jpg', os.path.basename('https://images.craigslist.org/01616_46rnDqsiSKE_600x450.jpg'))



