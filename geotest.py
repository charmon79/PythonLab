import sys, csv, getopt
from osgeo import osr

print 'Number of args:', len(sys.argv), 'arguments.'
print 'Argument list:', str(sys.argv)

nyc  = osr.SpatialReference()
nyc.ImportFromEPSG(2263) 
wgs84 = osr.SpatialReference()
wgs84.ImportFromEPSG(4326)

def main(argv):
	# we'll set these vars equal to the input args
	xcoord = 987899.0
	ycoord = 212072.0
	
	try:
		opts, args = getopt.getopt(argv,"x:y:i:")
	except getopt.GetoptError:
		assert False, 'failed to parse args'
	for opt, arg in opts:
		if opt == "-x":
			xcoord = arg
		elif opt == "-y":
			ycoord = arg
		elif opt == "-i":
			inputFileName = arg
		else:
			assert False, "unhandled input option"
	print 'X coordinate is: ', xcoord
	print 'Y coodtinate is: ', ycoord
	print 'input file name is: ', inputFileName
	
	#transformation = osr.CoordinateTransformation(nyc,wgs84)
	#result = transformation.TransformPoint(xcoord, ycoord)
	#print result
	
	looper = 0
	
	inputFile = open(inputFileName,'rb') #opens the CSV file
	try:
		reader = csv.reader(inputFile)
		for row in reader:
			print row
			looper += 1
			if looper > 10:
				break
	finally:
		inputFile.close()

if __name__ == "__main__":
	main(sys.argv[1:])
