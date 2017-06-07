import sys, getopt

def main(argv):
	start_site = ""
	json_file = ""
	new_file = ""

	try:
		#opts, args = getopt.getopt(argv, "-s:-j:-n:", ["start_site=", "json_file", "new_file"])
		opts, args = getopt.getopt(argv, "-s:-j:-n:", ["start_site=", "json_file=", "new_file="])
	except getopt.GetoptError:
		print "error message here"
		sys.exit(2)

	#print opts
	for opt, arg in opts:
		if opt in ["-s", "--start_site"]:
			start_site = arg
		elif opt in ["-j", "--json_file"]:
			json_file = arg
		elif opt in ["-n", "--new_file"]:
			if "T" in arg or "t" in arg:
				new_file = True
			else:
				new_file = False

	print "\n", start_site, json_file, new_file

if __name__ == "__main__":
	main(sys.argv[1:])