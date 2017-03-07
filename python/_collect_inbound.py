# coding: utf-8
###############################################################################
#
#      module  aseag_api
#
###############################################################################
# contains functions to retrieve data from ASEAG API
# Initial version was based on based  https://github.com/feuerrot/aseag-python
#  
###############################################################################

import json
import aseag_data
import aseag_inbound_connection
import aseag_api
from datetime import datetime
from myask import myask_log
from shutil import copyfile


def CollectInbound(outputfile):
    existing_connections = aseag_inbound_connection.INBOUND_LINES
    fout = open(outputfile, 'w+')
    fout.write("# coding: utf-8\n\n")
    fout.write("#List of inbound connections per station.\n")
    fout.write("#Auto-generated on " +datetime.now().strftime("%Y-%m-%d %H:%M")+"\n\n")
    fout.write("INBOUND_LINES= {\n")
    newcounter = 0
    for station in aseag_data.STATIONLIST:
        origin_id = int(station[0])
        orig_str = str(origin_id)
        myask_log.debug(9, "--- Station: "+orig_str)
        if orig_str in existing_connections:
            debugstr = "--- Station: "+orig_str
            inbound_line_departures = existing_connections[orig_str]
        else:
            debugstr = "+++ Station: "+orig_str
            inbound_line_departures = {}
        dircon = aseag_api.getDirectConnection(origin_id, 100000)
        if len(dircon) == 0: # no direct connection to bushof, let's try kaiserplatz
            dircon = aseag_api.getDirectConnection(origin_id, 100003)
            if len(dircon) > 0: debugstr += "(KP):"
            else:  debugstr += " NONE"
        else: debugstr += "    :"
#        dircon = []
        for con in dircon:
            dest = con['destinationName']
    #            if dest == "Aachen Bushof" : continue
            line = con['lineName']
            if line not in inbound_line_departures: 
                debugstr += "+"
                myask_log.debug(3, "new: "+ str(line) + " --> " + dest)
                inbound_line_departures[line] = [dest]
            else:
                if dest not in inbound_line_departures[line]: 
                    debugstr += "+"
                    myask_log.debug(3, "new: "+ str(line) + " --> " + dest)
                    newcounter += 1
                    inbound_line_departures[line].append(dest)
                else:
                    debugstr += "." 
                    myask_log.debug(9, "old "+ str(line) + " --> " + dest)
        myask_log.debug(3, debugstr)
        data_str = json.dumps(inbound_line_departures, sort_keys=True, ensure_ascii=False, separators=(',',':')).encode('utf8')
        #enforce proper unicode tracking to avoid issues when re-reading
        data_str = data_str.replace('["','[u"')
        data_str = data_str.replace('","','", u"')
        fout.write(" '"+ str(origin_id)+ "' : " +data_str  + ",\n")
    fout.write("}")
    fout.close()
    myask_log.debug(1, "Done. Added "+ str(newcounter) +" new destinations")

################################################################################

tmpfile = "c:/tmp/aseag_inbound_connection.py"
target = "./aseag_inbound_connection.py"
myask_log.SetDebugLevel(3)
CollectInbound(tmpfile)

userinput = raw_input("Copy : '"+tmpfile+"' to '"+target+"' ? (yes/no): ")
if userinput == "yes":
    print "OK"
    copyfile(tmpfile, target)
    print "File copied"
else:
    print "File not copied"