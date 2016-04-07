import sys, csv, getopt
from osgeo import osr

#print 'Number of args:', len(sys.argv), 'arguments.'
#print 'Argument list:', str(sys.argv)

nyc  = osr.SpatialReference()
nyc.ImportFromEPSG(2263) 
wgs84 = osr.SpatialReference()
wgs84.ImportFromEPSG(4326)

def main(argv):
	
	try:
		opts, args = getopt.getopt(argv,"i:o:")
	except getopt.GetoptError:
		assert False, 'failed to parse args'
	for opt, arg in opts:
		if opt == "-i":
			inputFileName = arg
		elif opt == "-o":
			outputFileName = arg
		else:
			assert False, "unhandled input option"
	#print 'X coordinate is: ', xcoord
	#print 'Y coodtinate is: ', ycoord
	print 'input file name is: ', inputFileName
	print 'output file name is: ', outputFileName
	
	transformation = osr.CoordinateTransformation(nyc,wgs84)
	#geopoint = transformation.TransformPoint(xcoord, ycoord)
	#print geopoint
	
	rownum = 0
	
	inputFile = open(inputFileName,'rb') #opens the CSV file to read
	outputFile = open(outputFileName,'wb') #opens the target CSV file to write
	try:
		reader = csv.reader(inputFile)
		writer = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for row in reader:
			#print row
			if rownum == 0:
				row.append('lat')
				row.append('lon')
			elif row[72].strip() == '' or row[73].strip() == '': #sometimes XCoord & YCoord are blank
				row.append('')
				row.append('')
			else:
				geopoint = transformation.TransformPoint(float(row[72]), float(row[73]))
				lat = geopoint[1]
				lon = geopoint[0]
				row.append(lat)
				row.append(lon)
			writer.writerow(row)
			rownum += 1
			#if rownum > 10:
			#	break
	finally:
		inputFile.close()
		outputFile.close()

if __name__ == "__main__":
	main(sys.argv[1:])
