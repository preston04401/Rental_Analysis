import json

json_file = 'craigslist_rental_data.json'
test_file = '/Users/Preston/programing/data science/udacity nano degree/mongotestdata/twitter.json'

'''
def parse(text):
    try:
        
        return json.loads(text)

    except ValueError as e:
        print('invalid json: %s' % e)
        return None # or: raise

# Pull list of craigslist id #'s.  
with open(json_file, 'r') as read_file:
	print parse(read_file)
	#data = json.load(read_file)
	#print data

'''

with open(json_file, 'r') as filein:
	for line in filein:
		print line