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
    existingcounter = 0
    observedcounter = 0
    stationcounter = 0
    nodirect_con= 0
    for station in aseag_data.STATIONLIST:
        stationcounter +=1
        origin_id = int(station[0])
        orig_str = str(origin_id)
        myask_log.debug(9, "--- Station: "+orig_str)
        if orig_str in existing_connections:
            debugstr = "--- Station: "+orig_str
            inbound_line_departures = existing_connections[orig_str]
            # do some statistics
            stationlinecounter = 0
            for lines in  inbound_line_departures:
                stationlinecounter += len(lines)
            existingcounter += stationlinecounter
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
            observedcounter +=1
            dest = con['destinationName']
    #            if dest == "Aachen Bushof" : continue
            line = con['lineName']
            if line not in inbound_line_departures: 
                debugstr += "+"
                myask_log.debug(3, "new: "+ str(line) + " --> " + dest)
                newcounter += 1
                stationlinecounter += 1
                inbound_line_departures[line] = [dest]
            else:
                if dest not in inbound_line_departures[line]: 
                    debugstr += "+"
                    myask_log.debug(3, "new: "+ str(line) + " --> " + dest)
                    newcounter += 1
                    stationlinecounter += 1
                    inbound_line_departures[line].append(dest)
                else:
                    debugstr += "." 
                    myask_log.debug(9, "old "+ str(line) + " --> " + dest)
        myask_log.debug(3, str(stationcounter)+" : "+debugstr)
        data_str = json.dumps(inbound_line_departures, sort_keys=True, ensure_ascii=False, separators=(',',':')).encode('utf8')
        #enforce proper unicode tracking to avoid issues when re-reading
        data_str = data_str.replace('["','[u"')
        data_str = data_str.replace('","','", u"')
        fout.write(" '"+ str(origin_id)+ "' : " +data_str  + ",\n")
        # do some statistics
        if stationlinecounter == 0: nodirect_con +=1
    fout.write("}")
    fout.close()
    myask_log.debug(1, "-----------------------------------")
    myask_log.debug(1, "Stations: "+ str(stationcounter)+ " ("+str(nodirect_con)+" without direction info)")
    myask_log.debug(1, "Existing: Dest.   " + str(existingcounter) +" ")
    myask_log.debug(1, "Observed  Dest.   " + str(observedcounter) +"  destinations found this time")
    myask_log.debug(1, "New  Destinations " + str(newcounter) +"  destinations added")



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