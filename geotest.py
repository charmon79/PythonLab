import sys, getopt
from pyproj import Proj

print 'Number of args:', len(sys.argv), 'arguments.'
print 'Argument list:', str(sys.argv)



def main(argv):
	# we'll set these vars equal to the input args
	xcoord = [0]
	ycoord = [0]
	
	# define the map projection & boundaries
	pnyc = Proj(
		proj='lcc',
		datum='NAD83',
		lat_1=40.666667,
		lat_2=41.033333,
		lat_0=40.166667,
		lon_0=-74.0,
		x_0=984250.0,
		y_0=0.0,
		preserve_units=True
		)
	
	try:
		opts, args = getopt.getopt(argv,"x:y:")
	except getopt.GetoptError:
		assert False, 'failed to parse args'
	for opt, arg in opts:
		if opt == "-x":
			xcoord = arg
		elif opt == "-y":
			ycoord = arg
		else:
			assert False, "unhandled input option"
	print 'X coordinate is "', xcoord
	print 'Y coodtinate is "', ycoord
	
	lat, lon = pnyc(xcoord, ycoord, inverse=True)
	
	print 'Lat: ', lat
	print 'Lon: ', lon

if __name__ == "__main__":
	main(sys.argv[1:])
