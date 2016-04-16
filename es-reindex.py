import sys, getopt, time, thread
from elasticsearch import Elasticsearch
from elasticsearch.helpers import reindex
from elasticsearch.exceptions import ConnectionError, NotFoundError

finished = False # we'll use this to check if reindex is done from a parallel thread
success = False # and we'll use this to check if the reindex completed successfully or not
startTime = time.time()

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

def DoReindex():
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
		print url + ': copying data from \"'+source+'\" to \"'+target+'\"...' 
		# startTime = time.time()		
		reindex(es, source, target)

		# print url + ': copy complete ('+str(elapsedTime)+' seconds)'
		finished = True
		success = True
	except:
		finished = True
		raise

def StatusWatcher():
	while finished == False:
		elapsedTime = time.time() - startTime
		if elapsedTime % 2 == 0:
			print str(elapsedTime)
	elapsedTime = time.time() - startTime
	print url + ': copy complete ('+str(elapsedTime)+' seconds)'


if __name__ == '__main__':
	# DoReindex()
	thread.start_new_thread(DoReindex,())
	thread.start_new_thread(StatusWatcher,())
	while 1:
		pass