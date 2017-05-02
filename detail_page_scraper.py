'''
Web Scraper to pull the details from a rental property listing on craigslist.
To be used in conjunction with the web crawler in the craigslist_rental_data.py file, 
which data will be returned to. 

To Pull:
- apartment / house / condo etc. 
- jpegs
- coordinates
- parking / garage. 

'''

from bs4 import BeautifulSoup
import urllib
import requests
import json
import os

craigslist_standard_url = 'https://sandiego.craigslist.org/'

test_property_id = '6112538066'  #'6108245215'

test_url = 'https://sandiego.craigslist.org/ssd/apa/6112538066.html'

def scrape_jpegs():
	pass

def save_jpgs(property_id, image_count):
	file_name = property_id + '_' + str(image_count) + '.jpg'
				
	path_file_name = jpeg_path + '/' + file_name

	# Create the new jpg file
	img_file = open(path_file_name, 'wb')
	# Load the picture and write it to the jpeg file. 
	img_file.write(requests.get(img_link).content)
	
	img_file.close()

def scrape_details(property_id, link):

	html_doc = urllib.urlopen(link)
	
	soup = BeautifulSoup(html_doc, 'html.parser')

	# Save the latitude and longitude of the property. 
	map_div = soup.find(id='map')

	latitude = map_div.get('data-latitude')
	longitue = map_div.get('data-longitude')

	'''
	If there is no thum div, then take the image from the div class='slide first visible'
	'''

	# File path for jpegs.
	cwd = os.getcwd()

	# Create a sub folder for each property. 
	jpeg_path = cwd + '/jpegs/' + property_id

	if not os.path.exists(jpeg_path):
		os.makedirs(jpeg_path)
	
	# Multiple thumbs first:
	image_links = soup.find_all('a', class_='thumb')
	
	# Test for multiple thumbs. 
	if image_links != []:

		image_count = 0

		for i in image_links:
			image_count += 1

			img_link = i['href']
			if img_link != None:  # why does this not work???
				file_name = property_id + '_' + str(image_count) + '.jpg'
				
				path_file_name = jpeg_path + '/' + file_name

				# Create the new jpg file
				img_file = open(path_file_name, 'wb')
				# Load the picture and write it to the jpeg file. 
				img_file.write(requests.get(img_link).content)
				
				img_file.close()
	
	# If there are no thumbnails but only one image.
	else:
		img = soup.find('img')
		print img		
			
			

			#urllib.urlretrieve(img_link, jpeg_path + jpeg_name)
		

	#hrefs = []
	'''
	for i in image_links:
		urllib.urlretrieve(i, )
	'''
		#print image_links['href']
		#hrefs.append(i.get('href'))

	html_doc.close()

	#return hrefs

	

print scrape_details('6112538066', test_url)

#pic = urllib.urlretrieve('https://images.craigslist.org/01616_46rnDqsiSKE_600x450.jpg', os.path.basename('https://images.craigslist.org/01616_46rnDqsiSKE_600x450.jpg'))



