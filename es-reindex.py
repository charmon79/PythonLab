import sys, getopt, thread
from elasticsearch import Elasticsearch
from elasticsearch.helpers import reindex
from elasticsearch.exceptions import ConnectionError, NotFoundError

finished = 0 # we'll use this to check if reindex is done from a parallel thread

# def usageError():
# 	print >> sys.stderr, ("Usage: "+str(sys.argv[0])+" url source target")
# 	sys.exit(1)

# get input args into variables. die if not all expected args exist.
try:
	url, source, target = str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3])
except IndexError:
	# usageError()
	print >> sys.stderr, ("Usage: "+str(sys.argv[0])+" url source target")
	sys.exit(1)

# print "args check done"

# try:
# 	source = 
# except IndexError:
# 	usageError()

# try:
# 	target = 
# except IndexError:
# 	usageError()

def esReindex():
	# print "should see me"

	# instantiate the ES object.
	es = Elasticsearch([url])

	# test that we can connect to the ES cluster at the given URL, 
	# and that the requested source index exists. if not, die.
	try:
		es.cat.indices(source)
	except ConnectionError:
		print("ERROR: Failed to connect to ES at URL: "+url)
		exit()
	except NotFoundError:
		print("ERROR: Index '"+source+"' does not exist")
		exit()
	finally:
		# make sure the requested target index DOESN'T exist already, and die if it does.
		try:
			test = es.cat.indices(target)
		except NotFoundError:
			pass
		finally:
			if 'test' in globals():
				#print(test)
				print("ERROR: Index '"+target+"' already exists")
				exit()
	# passed validation checks, so let's do the reindex thing now
	try:
		reindex(es, source, target)
	finally:
		finished = 1

if __name__ == '__main__':
	# print "should be starting a thread"
	# thread.start_new_thread(esReindex,())
	esReindex()