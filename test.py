import sys, getopt

print 'Number of args:', len(sys.argv), 'arguments.'
print 'Argument list:', str(sys.argv)

def main(argv):
	xcoord = 0
	ycoord = 0
	try:
		opts, args = getopt.getopt(argv,"hx:y:",["xcoord=","ycoord="])
	except getopt.GetoptError:
		print 'test.py -x <xcoord> -y <ycoord>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'do not use h, asshole'
			sys.exit()
		elif opt in ("-x","--xcoord"):
			xcoord = arg
		elif opt in ("-y","--ycoord"):
			ycoord = arg
	print 'X coordinate is "', xcoord
	print 'Y coodtinate is "', ycoord

if __name__ == "__main__":
	main(sys.argv[1:])
