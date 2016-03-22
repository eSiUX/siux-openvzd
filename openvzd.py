#!/usr/bin/python

import os, commands, time, ConfigParser, sys, random, xmlrpclib



def userBeancounters( filename='/proc/user_beancounters' ):

	if not os.path.isfile( filename ):
		print 'Filename="%s" not found' % (filename,)
		return ''

        f = open( filename, 'r' )
        data = f.read().split('\n')
	print 'Filename="%s", len=%s' % (filename, len(data) )
        f.close()

        return data



def vzParam( data=[] ):

        vz      = {}
        vzId    = -1

        names   = ['resource', 'held', 'maxheld', 'barrier', 'limit', 'failcnt']

        for lines in data:
 
                if not lines:
                        continue

                line = lines.split()
                if len(line) not in (6,7):
                        continue

                # get vzId
                if len(line) == 7:

                        if line[0][-1:] != ':':
                                continue

                        vzId = int(line[0][:-1])
                        line.remove( line[0] )

                if vzId not in vz:
                        vz[ vzId ] = {}

		resourceName = line[0]
                for no in range(1,len(line)):
			vz[ vzId ][ '%s_%s' % (resourceName, names[no]) ] = line[no]

        return vz



def vzList():

        ret = {}

        for lines in commands.getoutput('vzlist -a').split('\n'):

                if not lines:
                        continue

                line = lines.split()
                if len( line ) != 5:
                        continue                

                try:
                        vzId = int(line[0])
                except:
                        continue

                ret[ vzId ] = line[4]

        return ret



if __name__ == '__main__':

	timeSleep = 60
	apiKey = '06d197ba7a6e13dd41c57e939ce75463'

        # read /proc/user_beadncounters
        data    = userBeancounters()

        # virtuals
        vzIds   = vzList()

        # param for virtuals
        vzParams = vzParam( data=data )

	# hostname
	serverHostname = open( '/etc/hostname' ).read().split('\n')[0]
	
	# data add
	server = xmlrpclib.ServerProxy( 'http://preinstall:3025/RPC2' )
	for vzId in vzParams:
		params = vzParams[vzId]

		print 'openvz.add(', apiKey, vzId, vzIds.get(vzId,'unknown'), serverHostname, params,')'
		retAdd = server.openvz.add( apiKey, vzId, vzIds.get(vzId,'unknown'), serverHostname, params )
		print "openvz.add(%s, %s), ... ) - > %s: %s" % (vzId, vzIds.get(vzId,'unknown'), retAdd['status'], retAdd['statusMessage' ])
		print

        # sleep Xs
        print 'sleep %s s' % (timeSleep,)
        time.sleep( timeSleep )

	print 'done.'
