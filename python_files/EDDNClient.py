#!/usr/bin/env python

import zlib
import zmq
import simplejson
import sys, os, datetime, time, getopt

# Configuration
__relayEDDN             = 'tcp://eddn.edcd.io:9500'
__timeoutEDDN           = 600000
__debugEDDN             = False # Set False to listen to production stream
__logVerboseFile        = os.path.dirname(__file__) + '/Logs_Verbose_EDDN_%DATE%.htm' # Set to False if you do not want verbose logging
__logJSONFile           = os.path.dirname(__file__) + '/Logs_JSON_EDDN_%DATE%.log' # Set to False if you do not want JSON logging

# Used this to excludes yourself for example has you don't want to handle your own messages ^^
__excludedSoftwares     = [
    'My Awesome Market Uploader'
]

# Start
def date(__format):
    d = datetime.datetime.utcnow()
    return d.strftime(__format)

__oldTime = False

def echoLog(__str):
    global __oldTime, __logVerboseFile
    
    if __logVerboseFile != False:
        __logVerboseFileParsed = __logVerboseFile.replace('%DATE%', str(date('%Y-%m-%d')))
    
    if __logVerboseFile != False and not os.path.exists(__logVerboseFileParsed):
        f = open(__logVerboseFileParsed, 'w')
        f.write('<style type="text/css">html { white-space: pre; font-family: Courier New,Courier,Lucida Sans Typewriter,Lucida Typewriter,monospace; }</style>')
        f.close()

    if (__oldTime == False) or (__oldTime != date('%H:%M:%S')):
        __oldTime = date('%H:%M:%S')
        __str = str(__oldTime)  + ' | ' + str(__str)
    else:
        __str = '        '  + ' | ' + str(__str)
        
    print (__str)
    sys.stdout.flush()

    if __logVerboseFile != False:
        f = open(__logVerboseFileParsed, 'a')
        f.write(__str + '\n')
        f.close()
    

def echoLogJSON(__json):
    global __logJSONFile
    
    if __logJSONFile != False:
        __logJSONFileParsed = __logJSONFile.replace('%DATE%', str(date('%Y-%m-%d')))
        
        f = open(__logJSONFileParsed, 'a')
        #f.write(str(__json['message']) + '\n')
        f.write(str(__json.decode('utf-8')) + '\n')
        f.close()
        

def main(argv):
    number_of_datasets = 0
    try:
        opts, args = getopt.getopt(argv,":n:",["number_of_datasets="])
    except getopt.GetoptError:
        print('EDDNClient.py -n <number_of_datasets> or use EDDNClient.py --number_of_datasets=')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-n", "--number_of_datasets"):
            number_of_datasets = int(arg)
            print('Downloaded', number_of_datasets, 'datasets from EDDN')
    
    echoLog('Starting EDDN Subscriber')
    echoLog('')
    
    context     = zmq.Context()
    subscriber  = context.socket(zmq.SUB)
    
    subscriber.setsockopt(zmq.SUBSCRIBE, b"") #ein B - vielleicht das hier weg machen ?!
    subscriber.setsockopt(zmq.RCVTIMEO, __timeoutEDDN)

    iteration_count = 0
    while True:
        try:
            subscriber.connect(__relayEDDN)
            echoLog('Connect to ' + __relayEDDN)
            echoLog('')
            echoLog('')
            
            while True:
                if iteration_count == number_of_datasets:
                    if number_of_datasets == 0:
                        print('Use arguments for define the number of data sets that will downloaded.\n Try: -n <number_of_datasets> or --number_of_datasets=')
                        sys.exit(2)
                    else:
                        print('Downloaded', number_of_datasets, 'datasets from EDDN')
                    break
                __message   = subscriber.recv()
                
                if __message == False:
                    subscriber.disconnect(__relayEDDN)
                    echoLog('Disconnect from ' + __relayEDDN)
                    echoLog('')
                    echoLog('')
                    break
               
                __message   = zlib.decompress(__message)
                if __message == False:
                    echoLog('Failed to decompress message')

                __json      = simplejson.loads(__message)
                if __json == False:
                    echoLog('Failed to parse message as json')

                __converted = False
                
                # print schema info
                if __debugEDDN == True:
                    __json['$schemaRef'].replace('/test', '')

                __schemaType = __json['$schemaRef'].replace('https://eddn.edcd.io/schemas/', '').rsplit('/', 1)[-2]
                __schemaVersion = __json['$schemaRef'].rsplit('/', 1)[1]

                echoLog('Receiving '+__schemaType+' v'+__schemaVersion+' message:' )

                __excluded   = False

                if __json['header']['softwareName'] in __excludedSoftwares:
                    __excluded = True

                # Handle message
                if __excluded == True:
                    echoLog('EXCLUDED' + __json['header']['softwareName'])
                else:
                    echoLog('   - Timestamp: ' + __json['message']['timestamp'])
                    echoLog('   - Uploader ID: ' + __json['header']['uploaderID'])
                    echoLog('   - Software: ' + __json['header']['softwareName'] + ' / ' + __json['header']['softwareVersion'])
                    echoLog('')
                    # do the logging into file
                    echoLogJSON(__message)
                
                iteration_count +=1

            if iteration_count == number_of_datasets:
                break

        except zmq.ZMQError as e:
            echoLog('')
            echoLog('ZMQSocketException: ' + str(e))
            subscriber.disconnect(__relayEDDN)
            echoLog('Disconnect from ' + __relayEDDN)
            echoLog('')
            time.sleep(5)

if __name__ == '__main__':
    main(sys.argv[1:])
