# coding: utf-8
###############################################################################
#
#      module  aseag_api
#
###############################################################################
# contains functions to retrieve data from ASEAG API
#
#  
###############################################################################

import datetime
import requests
import json
import re
import aseag_data

from myask import myask_log

baseurl        = "http://ivu.aseag.de/interfaces/ura/{}"
url_l        = "location"
url_j        = "journey"
url_i        = "instant_V2"
returnlist    = "StopPointName,StopID,StopPointState,StopPointIndicator,Latitude,Longitude,VisitNumber,TripID,VehicleID,LineID,LineName,DirectionID,DestinationName,DestinationText,EstimatedTime,BaseVersion"
usage        = 'Usage: ./main [StopID/StopName] [BusID] ([BusID]…) +[MaxWait]'
infotext    = "Haltestelle:    {}\nHaltestellenID: {}\nLinienfilter:   {}"

totime = 0


def MatchesDirection(station, direction, line, destination):
    #---------------------------------------------------------------------------
    # checks if a given connection matches the list of specified direction 
    #
    # PARAMETERS
    #  'station' station ID for a bus stop
    #  'direction': either 'DIR_INWARD_ or 'DIR_OUTWARD'
    #  'line' : line of the connection under investigation
    #  'destination' destination station of the connection under investigation
    # 
    # RETURNS True if the bus goes in the requested direction
    # If no valid direction is specified or the bus direction cannot be
    # determined, the function returns True
    #---------------------------------------------------------------------------
    if direction == "": return True # if there's no direction, everything matches

    key = str(station)
    if key in aseag_data.HARDCODED_DIRECTIONS:
        inwardlist = aseag_data.HARDCODED_DIRECTIONS[key]["inward"]
        outwardlist = aseag_data.HARDCODED_DIRECTIONS[key]["outward"]
    else:
        inwardlist = aseag_data.HARDCODED_DIRECTIONS["DEFAULT"]["inward"]
        outwardlist = aseag_data.HARDCODED_DIRECTIONS["DEFAULT"]["outward"]
    busline = int(line)
    
    if direction == "DIR_INWARD":
        # positive list: 
        for (itemid, itemdest) in inwardlist:
            if destination == itemdest: # the destination is in the list
                if itemid == 0 or itemid == busline: # the destination matches for all buses or the bus is the right one
                    myask_log.debug(10, "Match: Found inbound match for station '"+key+"' Bus "+str(busline)+ ": "+destination)
                    return True    
        # negative list let's check if the item is in the outbound list
        for (itemid, itemdest) in outwardlist:
            if destination == itemdest: # the destination is in the list
                if itemid == 0 or itemid == busline: # the destination matches for all buses or the bus is the right one
                    myask_log.debug(10, "Mismatch: Found outbound match for station '"+key+"' Bus "+str(busline)+ ": "+destination)
                    return False    
        myask_log.debug(10, "Did not find in/out match for '"+key+"' Bus "+str(busline)+ ": "+destination)
        return True
    elif  direction == "DIR_OUTWARD":
        # positive list: 
        for (itemid, itemdest) in outwardlist:
            if destination == itemdest: # the destination is in the list
                if itemid == 0 or itemid == busline: # the destination matches for all buses or the bus is the right one
                    myask_log.debug(10, "Match: Found outbound match for station '"+key+"' Bus "+str(busline)+ ": "+destination)
                    return True    
        # negative list let's check if the item is in the outbound list
        for (itemid, itemdest) in inwardlist:
            if destination == itemdest: # the destination is in the list
                if itemid == 0 or itemid == busline: # the destination matches for all buses or the bus is the right one
                    myask_log.debug(10, "Mismatch: Found inbound match for station '"+key+"' Bus "+str(busline)+ ": "+destination)
                    return False    
        myask_log.debug(10, "Did not find in/out match for '"+key+"' Bus "+str(busline)+ ": "+destination)
        return True
    else:
        myask_log.error("Invalid direction '"+str(direction) +"' found ignoring filter")
        return True


def unicodify(aseag_str):
    print("Translating String '"+aseag_str+"'")
    textstr = aseag_str.encode('utf-8')
    textstr = unicode(textstr.decode("unicode-escape"))
    return textstr.encode('utf-8')   

def unix_epoch_to_utcdatetime(epoch_ms):
    ts = epoch_ms * (10**(-3))
#    utc_offset = datetime.datetime.fromtimestamp(ts) - datetime.datetime.utcfromtimestamp(ts)
#    print ("time offset:" + str(utc_offset))
    return datetime.datetime.utcfromtimestamp(ts)

def unix_epoch_to_utcdate(epoch_ms):
    return unix_epoch_to_utcdatetime(epoch_ms).strftime('%Y-%m-%d %H:%M')

def unix_epoch_to_utctime(epoch_ms):
    return unix_epoch_to_utcdatetime(epoch_ms).strftime('%H:%M')

def unix_epoch_from_now_org():
    return int(datetime.datetime.now() * 1000)

def unix_epoch_from_now():
    dt = datetime.datetime.utcnow()
    epoch=datetime.datetime(1970,1,1)
    td = dt - epoch
    # return td.total_seconds()
    delta =  (td.seconds + td.days * 86400) *1000
    return delta

def get_stoppoint(name):
    parameter = {'searchString': name, 'maxResults': 5, 'searchTypes': 'STOPPOINT'}
    request = requests.get(baseurl.format(url_l), params=parameter)
    if request.status_code != 200:
        raise Exception
    if request.headers['content-type'] != 'application/json;charset=UTF-8':
        raise Exception
    data = request.json()
    resultstops = []
    print ("DEBUG: got request \n"+ str(data) + "\n--------------")
    if data['resultCount'] == 0:
        myask_log.debug(3, "No result for stop name {}".format(name))
    elif data['resultCount'] > 1:        
        print("More than one result for stop name {}:".format(name))
        print("ID\tName")
        for elem in data['resultList']:
            stopid = elem['stopPointId']
            stopname = unicodify(elem['stopPointName'])        
            resultstops.append([stopid,stopname])
    else: # a single result was shown
        stopid = data['resultList'][0]['stopPointId']
        stopname = unicodify(data['resultList'][0]['stopPointName'])        
        myask_log.debug(3, "Found a single match for '"+name+"': "+str(stopid) +" : "+stopname)
        resultstops.append([stopid,stopname])
        
    return resultstops
    
def GetStopIdByStationNameCity(stationname, cityname):
    resultstops = []
    return resultstops

def GetDefaultStopIdByCity(cityname, transport):
    return 0
    
def parsejson(data, encoding):
    output = []
    for line in data.splitlines():
        linelist = json.loads(line)
        if (linelist[0] == 1):
            output.append((linelist[15],linelist[8],linelist[12]))
    output.sort(key=lambda tup: tup[0])
    return output

# See: http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
def deduplication(data):
    jsondata = data
    seen = set()
    seen_add = seen.add
    jsondata = [x for x in jsondata if not (x in seen or seen_add(x))]
    return jsondata

def tsfilter(ts, totime): # Todo: schöner machen
    if totime == 0:
        return (unix_epoch_to_utcdatetime(ts) >= datetime.datetime.utcnow() - datetime.timedelta(minutes = 5))
    else:
        return (unix_epoch_to_utcdatetime(ts) >= datetime.datetime.utcnow() - datetime.timedelta(minutes = 5)) and (unix_epoch_to_utcdatetime(ts) <= datetime.datetime.now() + datetime.timedelta(minutes = totime))


def get_stopdata(stop_point_id, lines):
    #--------------------------------------------------------------------------
    # returns the next buses of given lines from a bus stop
    # 
    parameter = {'ReturnList': returnlist, 'StopID': stop_point_id}
    if lines:
        parameter['LineID'] = ",".join(lines)
    request = requests.get(baseurl.format(url_i), params = parameter)
    if request.status_code != 200:
        raise Exception
    if request.headers['content-type'] != 'application/json;charset=UTF-8':
        raise Exception
    data = deduplication(parsejson(request.text, request.encoding))
    return data

def get_routedata(start, stop):
    parameter = {'startStopId': start, 'endStopId': stop, 'departureTime': unix_epoch_from_now(), 'maxNumResults': 4}
    request = requests.get(baseurl.format(url_j), params = parameter)
    if request.status_code != 200:
        raise Exception
    if request.headers['content-type'] != 'application/json;charset=UTF-8':
        raise Exception
    data = request.json()
    return data

def GetDepartures(StopID, busline, direction, utc_offset):
    myask_log.debug(3, "aseag_api.GetDepartures: Haltestellenabfrage von "+ str(StopID)+ ". Buslinie: '"+str(busline)+"'. Direction: "+str(direction))
    if busline == 0: buses = []
    else: buses = [str(busline)] 
    
    output = get_stopdata(StopID, buses)
    connection_list = []
    for line in output:
        print "LINE: "+ str(line)
        if tsfilter(line[0], totime):
            dep_time = unix_epoch_to_utcdatetime(line[0]) + datetime.timedelta(hours = utc_offset)
            busnr = line[1]
            destination = unicodify(line[2])
            # check if the connection matches the filters for busline and direction
            if MatchesDirection(StopID, direction, busnr, destination):
                connection = (dep_time, busnr, destination)
                connection_list.append(connection)
                myask_log.debug(5, "Using connection line "+str(busnr)+" to "+str(destination)+ ": matches direction")
            else:
                myask_log.debug(5, "Ignoring connection line "+str(busnr)+" to "+str(destination)+ ": does not match direction")
    myask_log.debug(4, str(len(connection_list))+ " connections found")
    
    return connection_list

def GetConnections(origin_ID, destination_ID, utc_offset):
    myask_log.debug(3, "Routenabfrage von "+str(origin_ID) + " nach "+ str(destination_ID)+"...")
    output = get_routedata(origin_ID, destination_ID)
    result_connections = []
    for journey in output['resultList']:
        res_journey = {}
        try:
            # get jorney_start end end time
            res_journey['start_datetime']   = unix_epoch_to_utcdatetime(journey['startTimeInUnixEpochMillis']) + datetime.timedelta(hours = utc_offset)
            res_journey['end_datetime'] = unix_epoch_to_utcdatetime(journey['endTimeInUnixEpochMillis']) + datetime.timedelta(hours = utc_offset)
            res_journey['start_loc'] = journey['startLocation']['stopPointName']
            res_journey['end_loc'] = journey['endLocation']['stopPointName']
            res_journey['legs'] = []
            #loop over all parts (legs) of this journey
            for connection_leg in journey['elementList']:
                res_connection_leg = {}
                if connection_leg["type"] == "LineChange":
                    res_connection_leg ['type'] = "LineChange"
                elif connection_leg['modalType'] == "bus":
                    res_connection_leg['type'] = "bus"
                    res_connection_leg['start_loc'] = connection_leg['start']['location']['stopPointName']
                    res_connection_leg['end_loc'] =   connection_leg['end']['location']['stopPointName']
                    res_connection_leg['line'] = connection_leg['lineName']
                    tmp_datetime = unix_epoch_to_utcdatetime(
                            connection_leg['start']['aimedArrivalInUnixEpochMillis'] or
                            connection_leg['start']['estimatedArrivalInUnixEpochMillis'] or
                            connection_leg['start']['scheduledArrivalInUnixEpochMillis'])
                    res_connection_leg['start_datetime'] = tmp_datetime + datetime.timedelta(hours = utc_offset)
                    tmp_datetime = unix_epoch_to_utcdatetime(
                            connection_leg['end']['aimedArrivalInUnixEpochMillis']    or 
                            connection_leg['end']['estimatedArrivalInUnixEpochMillis'] or
                            connection_leg['end']['scheduledArrivalInUnixEpochMillis'])                    
                    res_connection_leg['end_datetime'] = tmp_datetime + datetime.timedelta(hours = utc_offset)
                elif connection_leg['modalType'] == "walk":
                    res_connection_leg ['type'] = "walk"
                    tmp_datetime = unix_epoch_to_utcdatetime(
                            connection_leg['start']['aimedArrivalInUnixEpochMillis'] or
                            connection_leg['start']['estimatedArrivalInUnixEpochMillis'] or
                            connection_leg['start']['scheduledArrivalInUnixEpochMillis'])
                    res_connection_leg['start_datetime'] = tmp_datetime + datetime.timedelta(hours = utc_offset)
                    tmp_datetime = unix_epoch_to_utcdatetime(
                            connection_leg['end']['aimedArrivalInUnixEpochMillis'] or 
                            connection_leg['end']['estimatedArrivalInUnixEpochMillis'] or
                            connection_leg['end']['scheduledArrivalInUnixEpochMillis'])
                    res_connection_leg['end_datetime'] = tmp_datetime + datetime.timedelta(hours = utc_offset) 
                    res_connection_leg['start_loc'] = connection_leg['start']['location']['stopPointName']
                    res_connection_leg['end_loc'] =   connection_leg['end']['location']['stopPointName']
                res_journey['legs'].append(res_connection_leg)
        except KeyError as e:
            print("error: cannot parse journey "+ str(journey))
            print e.message, e.args
            res_journey = []

        result_connections.append(res_journey)
   
    myask_log.debug(3, "..."+str(len(result_connections))+" connections found" )
    
    return result_connections

def GetConnectionsWithBus(origin_ID, destination_ID, busline, utc_offset):
    connection_list =  GetConnections(origin_ID, destination_ID, utc_offset)
    
    if busline == 0: return (True, connection_list)
    
    print("checking for buses"+ str(busline))
    matching_connections = []
    # check if the buses are indeed used
    for connection in connection_list:
        # check if this connection uses the specified buy
        if 'legs' in connection:
            usesbus = False
            for leg in connection['legs']:
                if 'line' in leg and int(leg['line']) == busline:
                    myask_log.debug(5, u"match found for bus "+str(busline) +\
                                    u" in connection "+str(connection) )
                    usesbus = True
                    break
            if usesbus: matching_connections.append(connection)
            else: myask_log.debug(5, u"NO match found for bus "+str(busline) +\
                                    u" in connection "+str(connection) )

    if len(matching_connections) == 0:
        return (False, connection_list)
    else:
        return (True, matching_connections)
       
def GetFilteredConnections(start_id, stop_id, preferred_bus, prefered_transport, utc_offset):
    if prefered_transport != "":
        myask_log.warning("GetFilteredConnections: Filtering by transport not yet impleneted")
        
    return GetConnectionsWithBus(start_id, stop_id, preferred_bus, utc_offset)
    
def FindFavoriteConnetions(start_id, stop_id, start_time, end_time, preferred_bus, utc_offset):
    match, lineconnections = GetConnectionsWithBus(start_id, stop_id, preferred_bus, utc_offset)
    
    if match and start_time != "" : # filter for time window only if there is a bus match
        matching_connections = []
        if re.match("\d\d:\d\d$", start_time): 
            tmp = datetime.datetime.strptime(start_time, "%H:%M")
            window_start = tmp.time()
        else:
            myask_log.error("Invalid start time format in 'FindFavoriteConnetions': "+start_time)
            start_time = datetime.datetime.utcnow()+ datetime.timedelta(hours = utc_offset)
  
        if(end_time == "" ):
            window_end = window_start + datetime.timedelta(hours=1)
        elif re.match("\d\d:\d\d$", end_time): 
            tmp = datetime.datetime.strptime(end_time, "%H:%M")
            window_end= tmp.time()
        else:
            myask_log.error("Invalid end time format in 'FindFavoriteConnetions': "+ end_time)
            window_end = window_start + datetime.timedelta(hours=1)
       
       
        # now loop over all connections and check if they depart in the right time window
        for connection in lineconnections:
            # check if this connection departs in the specified time
            deptime = connection['start_datetime'].time()
            if (deptime >= window_start and deptime <= window_end):
                myask_log.debug(5, u"time match in connection "+str(connection) )
                matching_connections.append(connection)
            else: myask_log.debug(5, u"NO time match in connection "+str(connection) )

        if len(matching_connections) == 0:
            myask_log.debug(5, u"No matchin connections in timewondow found. Returning all")
            return (False, lineconnections)
        else:
            return (True, matching_connections)
       
    else:
        return match, lineconnections
    
