import sys, getopt, time, thread
from elasticsearch import Elasticsearch
from elasticsearch.helpers import reindex
from elasticsearch.exceptions import ConnectionError, NotFoundError

finished = False # we'll use this to check if reindex is done from a parallel thread
start_time = time.time()

# get input args into variables. die if not all expected args exist.
try:
	url, source, target = str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3])
except IndexError:
	# usageError()
	print >> sys.stderr, ("Usage: "+str(sys.argv[0])+" url source target")
	sys.exit(1)

# instantiate ES object
es = Elasticsearch([url])

# test that we can connect to the ES cluster at the given URL, 
# and that the requested source index exists. if not, die.
try:
	es.cat.indices(source)
except ConnectionError:
	print("ERROR: Failed to connect to ES at URL: "+url)
	exit()
except NotFoundError:
	print("ERROR: Index \""+source+"\" does not exist")
	exit()
finally:
	# make sure the requested target index doesn't already contain data.
	try:
		test = es.count(index=target)
	except NotFoundError:
		print "WARNING: Target index \""+target+"\" doesn't exist. It will be created with auto mapping."
	finally:
		if 'test' in locals() and test > 0:
			print("ERROR: Index \""+target+"\" already contains data. Aborting.")
			exit(1)

# passed validation checks, so let's do the reindex thing now
def DoReindex():
	try:
		print url + ": reindexing data from \""+source+"\" to \""+target+"\"..."
		reindex(es, source, target)
	except:
		raise

def CheckStatus():
	global start_time
	global finished
	es = Elasticsearch([url])
	source_count = es.count(index=source)
	target_count = es.count(index=target)
	print "copied "+str(target_count['count'])+" of "+str(source_count['count'])+" ( elapsed: "+str(int(time.time() - start_time))+" sec. )"
	if source_count == target_count:
		finished = True

if __name__ == '__main__':
	thread.start_new_thread(DoReindex,())
	while finished == False:
		time.sleep(5)
		CheckStatus()
	print "Reindex finished."
