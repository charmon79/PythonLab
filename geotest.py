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
		opts, args = getopt.getopt(argv,"x:y:i:o:")
	except getopt.GetoptError:
		assert False, 'failed to parse args'
	for opt, arg in opts:
		if opt == "-x":
			xcoord = arg
		elif opt == "-y":
			ycoord = arg
		elif opt == "-i":
			inputFileName = arg
		elif opt == "-o":
			outputFileName = arg
		else:
			assert False, "unhandled input option"
	print 'X coordinate is: ', xcoord
	print 'Y coodtinate is: ', ycoord
	print 'input file name is: ', inputFileName
	print 'output file name is: ', outputFileName
	
	#transformation = osr.CoordinateTransformation(nyc,wgs84)
	#result = transformation.TransformPoint(xcoord, ycoord)
	#print result
	
	rownum = 0
	
	inputFile = open(inputFileName,'rb') #opens the CSV file to read
	outputFile = open(outputFileName,'wb') #opens the target CSV file to write
	try:
		reader = csv.reader(inputFile)
		writer = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		for row in reader:
			print row
			writer.writerow(row)
			if rownum == 0:
				header = row
			else:
				
			rownum += 1
			if rownum > 10:
				break
	finally:
		inputFile.close()
		outputFile.close()

if __name__ == "__main__":
	main(sys.argv[1:])
