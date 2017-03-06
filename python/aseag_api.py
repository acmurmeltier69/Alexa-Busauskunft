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

import datetime
import requests
import json
import re
import aseag_data
import aseag_inbound_connection
import argparse

from myask import myask_log

baseurl        = "http://ivu.aseag.de/interfaces/ura/{}"
url_l        = "location"
url_j        = "journey"
url_i        = "instant_V2"
returnlist    = "StopPointName,StopID,StopPointState,StopPointIndicator,Latitude,Longitude,VisitNumber,TripID,VehicleID,LineID,LineName,DirectionID,DestinationName,DestinationText,EstimatedTime,BaseVersion"

totime = 0


def MatchesDirection(station_ID, direction, line, destination):
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

    key = str(station_ID)
    if key in aseag_inbound_connection.INBOUND_LINES:
        inwardlist = aseag_inbound_connection.INBOUND_LINES[key]
    else:
        myask_log.error("Station '"+str(station_ID)+"' not found in inbound list. returning all stations")
        return True
    busline = line
    
    if direction == "DIR_INWARD":
        # positive list: 
        if destination in aseag_data.CENTRAL_DESTINATIONS:
            # if bus goes to one of those, it is by definition inbound. no need to look further
            return True
        elif str(line) in inwardlist: # we have a list of destinations of that line, which pass through the center
            if destination in inwardlist[str(line)]: return True
            else: return False
        else:
            #line unknown
            return False

    elif  direction == "DIR_OUTWARD":
        # exclude all known inbound lines
        if destination in aseag_data.CENTRAL_DESTINATIONS:
            # if bus goes to one of those, it is by definition inbound. no need to look further
            return False
        elif str(line) in inwardlist: # we have a list of destinations of that line, which pass through the center
            if destination in inwardlist[str(line)]: return False
            else: return True
        else:
            #line unknown
            return True
    else:
        myask_log.error(u"Invalid direction '"+str(direction) +u"' found ignoring filter")
        return True


def unicodify(aseag_str):
    outstr = aseag_str
    # nothing to be done here 
    return outstr    

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
    myask_log.debug(5, "got API request \n"+ str(data) + "\n--------------")
    if data['resultCount'] == 0:
        myask_log.debug(3, u"No result for stop name {}".format(name))
    elif data['resultCount'] > 1:        
        myask_log.warning("More than one result for stop name '"+name+"' ("+str(data['resultCount'])+" found)")
        for elem in data['resultList']:
            stopid = elem['stopPointId']
            stopname = unicodify(elem['stopPointName'])        
            resultstops.append([stopid,stopname])
    else: # a single result was shown
        stopid = data['resultList'][0]['stopPointId']
        stopname = unicodify(data['resultList'][0]['stopPointName'])        
        myask_log.debug(3, u"Found a single match for '"+name+"': "+str(stopid) +" : "+stopname)
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
            output.append((linelist[15],linelist[9],linelist[12]))
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


def get_stopdata(stop_point_id, lines, getraw=False):
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
    if getraw: 
        return  request.text
    else: 
        data = deduplication(parsejson(request.text, request.encoding))
        return data


def GetDepartures(StopID, busline, direction, utc_offset):
    #--------------------------------------------------------------------------
    # Returns a list of live bus departures from the specified bus stop
    # PARAMETERS:
    # - 'StopID'  Bus stop ID for the departure station (integer, 1000000-999999)
    # - 'busline' : (integer/string) Filter to show only buses from that line.
    #                If '0', all buses are shown
    # - 'direction: (string) Shows only buses for the specified connection
    #                either 'DIR_INWARD_ or 'DIR_OUTWARD'
    #                if "", all departures are shown
    # 
    # - utc_offset:     Timezone, for which the times should be returned (API uses UTC)
    # RETURNS:
    # List of departures from the station with:
    # [ 
    #    dep_time,    // datetime. Estimated departure time
    #    busnr,       // string    Bus number
    #    destination, // (string) destination of the bus
    # ]
    #--------------------------------------------------------------------------
    myask_log.debug(3, u"aseag_api.GetDepartures: Haltestellenabfrage von "+ str(StopID)+ u". Buslinie: '"+str(busline)+u"'. Direction: "+str(direction))
    if busline == '' or busline == '?': buses = []
    else: buses = [str(busline)] 
    
    output = get_stopdata(StopID, buses)
#    print "DEPARTURES:-------------------------"
#    print json.dumps(output, indent=4, sort_keys=False)
#    print "END_CONNECTION-------------------------------------"
    connection_list = []
    for line in output:
        myask_log.debug(5, "LINE: "+ str(line))
        if tsfilter(line[0], totime):
            dep_time = unix_epoch_to_utcdatetime(line[0]) + datetime.timedelta(hours = utc_offset)
            busnr = line[1]
            destination = unicodify(line[2])
            # check if the connection matches the filters for busline and direction
            if MatchesDirection(StopID, direction, busnr, destination):
                connection = (dep_time, busnr, destination)
                connection_list.append(connection)
            else:
                myask_log.debug(5, u"Ignoring connection line "+str(busnr)+u" to "+ destination + u": does not match direction")
    myask_log.debug(4, str(len(connection_list))+ u" connections found")
    
    return connection_list

def get_routedata(origin_ID, destination_ID):
    #---------------------------------------------------------------------------
    # core function for retrieving a connection from the ASEAG server
    # PARAMETERS:
    # - origin_ID:      Bus stop ID for the departure station (integer, 1000000-999999)
    # - destination_ID: Bus stop ID for the departure station (integer, 1000000-999999)
    # RETURNS:
    # raw JSON data structure with the connection results
    #---------------------------------------------------------------------------
    parameter = {'startStopId': origin_ID, 'endStopId': destination_ID, 'departureTime': unix_epoch_from_now(), 'maxNumResults': 4}
    request = requests.get(baseurl.format(url_j), params = parameter)
    if request.status_code != 200:
        myask_log.error(u"ASEAG API call returned unexpected status code '"+str(request.status_code)+u"' \nRequest: "+ str(request))
        return None
    if 'content-type' not in request.headers: 
        myask_log.error(u"ASEAG API call misses header '"+str(request.headers)+u"' \nRequest: "+ str(request))
        return None
    if request.headers['content-type'] != 'application/json;charset=UTF-8':
        myask_log.error(u"ASEAG API call returned unexpected header '"+str(request.headers['content-type'])+u"' \nRequest: "+ str(request))
        return None
    data = request.json()
    return data

def GetConnections(origin_ID, destination_ID, utc_offset):
    #---------------------------------------------------------------------------
    # Retrieves a connection from the ASEAG server (using get_routedata) and
    # returns the connection in a simplified format
    # PARAMETERS:
    # - origin_ID:      Bus stop ID for the departure station (integer, 1000000-999999)
    # - destination_ID: Bus stop ID for the departure station (integer, 1000000-999999)
    # - utc_offset:     Timezone, for which the times should be returned (API uses UTC)
    #
    # RETURNS: datastructure holding multiple connections (joruneys)
    #         Each connection can consist of several parts ('legs')
    #   '[     // list of journeys (matching connections)
    #       'start_datetime' : (datetime) departure time in local time
    #       'end_datetime'   : (datetime) arrival time in local time
    #       'start_loc'      : (string)  name of the overall departure station
    #       'end_loc'        : (string)  name of the overall arrival station
    #       'legs' :  [ // list of legs in this journey
    #           'type' : 'LineChange' | 'bus' | 'walk'
    #            'start_loc': (string)  name of the departure location for this leg
    #            'end_loc' :  (string)  name of the arrival location for this leg
    #            'line'  (string) name of busline (only for type 'bus')
    #            'start_datetime' :  (datetime) start time for this leg (in local time)
    #            'end_datetime'   :  (datetime) end time for this leg (in local time)
    #          ]
    #      ] 
    # If an error occurs, the function returns an empty connection list
    # If an error occurs parsing a specific journey, this journey is returned as empty
    #---------------------------------------------------------------------------
    myask_log.debug(3, u"Fetching connection from  '"+str(origin_ID) + u"' to '"+ str(destination_ID)+u"'...")
    output = get_routedata(origin_ID, destination_ID)
    if output == None: return []

#    print "CONNECTION:-------------------------"
#    print json.dumps(output, indent=4, sort_keys=False)
#    print "END_CONNECTION-------------------------------------"
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
            myask_log.error(u"error: cannot parse journey "+ str(journey))
            print e.message, e.args
#            print json.dumps(output, indent=4, sort_keys=False)
            res_journey = []

        result_connections.append(res_journey)
   
    myask_log.debug(3, u"..."+str(len(result_connections))+u" connections found" )    
    return result_connections

def GetConnectionsWithBus(origin_ID, destination_ID, busline, utc_offset):
    #---------------------------------------------------------------------------
    # Retrieves connection thet contain a specific busline only.
    # The system fetches connections from 'origin_ID' to 'destination_ID' using
    # GetConnections().
    # The results are then filtered to only contain connections where
    # at least one leg uses the specified busline.
    # If no matches are found at all, the system returns the full list (constraint is relaxed)
    # PARAMETERS:
    # - origin_ID:      Bus stop ID for the departure station (integer, 1000000-999999)
    # - destination_ID: Bus stop ID for the departure station (integer, 1000000-999999)
    # - busline:        (int/string) denoting the busline to be filtered for
    # - utc_offset:     Timezone, for which the times should be returned (API uses UTC)
    # RETURNS:  match,connection_list
    # 'match' (booloean): True if the busline constraint was met, False if it was relaxed
    # 'connection_list' list of bus connections. See GetConnections() for details
    #---------------------------------------------------------------------------   
    connection_list =  GetConnections(origin_ID, destination_ID, utc_offset)
    
    if busline == '' or busline == '?': return (True, connection_list)
    
    print(u"checking for buses"+ str(busline))
    matching_connections = []
    # check if the buses are indeed used
    for connection in connection_list:
        # check if this connection uses the specified buy
        if 'legs' in connection:
            usesbus = False
            for leg in connection['legs']:
                if 'line' in leg and leg['line'] == busline:
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
        myask_log.warning(u"GetFilteredConnections: Filtering by transport not yet implemented")
        
    return GetConnectionsWithBus(start_id, stop_id, preferred_bus, utc_offset)
    
def FindFavoriteConnetions(start_id, stop_id, start_time, end_time, preferred_bus, utc_offset):
    match, lineconnections = GetConnectionsWithBus(start_id, stop_id, preferred_bus, utc_offset)
    
    if match and start_time != "" : # filter for time window only if there is a bus match
        matching_connections = []
        if re.match("\d\d:\d\d$", start_time): 
            tmp = datetime.datetime.strptime(start_time, "%H:%M")
            window_start = tmp.time()
        else:
            myask_log.error(u"Invalid start time format in 'FindFavoriteConnetions': "+start_time)
            start_time = datetime.datetime.utcnow()+ datetime.timedelta(hours = utc_offset)
  
        if(end_time == "" ):
            window_end = window_start + datetime.timedelta(hours=1)
        elif re.match("\d\d:\d\d$", end_time): 
            tmp = datetime.datetime.strptime(end_time, "%H:%M")
            window_end= tmp.time()
        else:
            myask_log.error(u"Invalid end time format in 'FindFavoriteConnetions': "+ end_time)
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


def getDirectConnection(origin_id, destination_id):
    #---------------------------------------------------------------------------
    # checks for direct connections from tart_id to stop_id and returns
    # a list of entries [line, destination]
    #---------------------------------------------------------------------------
    direct_connections = []
    connections = get_routedata(origin_id, destination_id)
    if 'resultList' not in connections:
        return direct_connections
    for journey in connections['resultList']:
        if 'elementList' not in journey: continue
        if len(journey['elementList']) != 1:
            myask_log.debug(7,"connection found with '"+str(len(journey['elementList']))+"' legs. ignoring")
        else:
            con = {}
            leg = journey['elementList'][0]
            try:
                con['lineName'] = leg['lineName']
                con['tripId'] = leg['tripId']
                con['destinationName'] = leg['destinationName']
                direct_connections.append(con)
            except:
                myask_log.debug(3, "fields missing")
    return direct_connections
      


def main():
#        - aseag_api.py [-oid DEP_STOP_ID] [-did DESTINATION_STOP_ID] [-line LINENUMBER] [-dir IN_OUT] [-t TRANSPORT] [-raw]
#       - if no origin is given, system uses default-stop 
#       - if no destination is given, system shows departures from origin
#       output: if '-raw' is given, present raw output from ASEAG API, else give simplified output   
    print("in main")
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", type=int,
                        help="define output verbosity")
    org_group = parser.add_mutually_exclusive_group(required=True)
    org_group.add_argument("-oid", "--origin_id", type=int,
                        help="6-digit station ID of origin (departure) station")
    org_group.add_argument("-oname", "--origin_name", type=str,
                        help="name of origin (departure) station")
    dep_group = parser.add_mutually_exclusive_group()
    dep_group.add_argument("-did", "--destination_id", type=int,
                        help="6-digit station ID of destination station")
    dep_group.add_argument("-dname", "--destination_name", type=str,
                        help="name of destination station")

    parser.add_argument("-l", "--busline", type=str, 
                        help="Line (NR or string")
    parser.add_argument("-dir", "--direction", type=int, 
                        help="direction: 1=inward 2=outward")
    parser.add_argument("-raw", "--raw_mode", action="store_true",
                        help="If set, output raw API results")
    args = parser.parse_args()    

    if args.verbosity:
        myask_log.SetDebugLevel(args.verbosity)

    if args.origin_id: 
        origin_id = args.origin_id
    elif args.origin_name: 
        origin_id_list =  get_stoppoint(args.origin_name)
        if len(origin_id_list) != 1: 
            myask_log.error("no unique stop found")
            for alt in origin_id_list:
                print alt
            return
        else:
            origin_id = origin_id_list[0][0]
    else:
        myask_log.error("origin destination not specified")
    origin_id = int(origin_id)    # just to be sure
    
    if origin_id <100000 or origin_id > 999999:
        myask_log.error("invalid origin id '"+str(origin_id)+"#")

    if args.destination_id: 
        destination_id = args.destination_id
    elif args.destination_name: 
        destination_id_list =  get_stoppoint(args.destination_name)
        if len(destination_id_list) != 1: 
            myask_log.error("no unique stop found")
            for alt in destination_id_list:
                print alt
            return
        else:
            destination_id = destination_id_list[0][0]
    else:
        destination_id = 0 # code for not set
    destination_id = int(destination_id)    # just to be sure

    if destination_id != 0 and (destination_id <100000 or destination_id > 999999):
        myask_log.error("invalid destination_id  '"+str(destination_id)+"#")
        return
    if args.busline: busline = args.busline
    else: busline = "" 
        
    if args.direction:
        if args.direction == 1: direction = "DIR_INWARD"
        elif args.direction == 2: direction = "DIR_OUTWARD"
        else:
            myask_log.error("invalid direction  '"+str(args.direction)+" (must be 1 (inbound) or 2 (outbound)")
            return
    else: 
        direction = ""
    # now process the commands
    if destination_id == 0: # (departures only)
        if args.raw_mode:
            if direction != "":
                print "Departure Post-Filter for direction not supported in raw mode"
            if busline =="" : buslines = []
            else: buslines = [busline]
            results = get_stopdata(origin_id,buslines, getraw=True)
            print  results
        else:
            results =  GetDepartures(origin_id, busline, direction, utc_offset=1)
            for result in results:
                print result
    
    else: # origin and destination
        if args.raw_mode:
            if busline != "":
                print "Connection Post-Filter for busline not supported in raw mode"
            print "Raw results-----------------"
            output = get_routedata(origin_id, destination_id)
            print json.dumps(output, indent=4, sort_keys=False)         
        else:
            match, results = GetConnectionsWithBus(origin_id, destination_id, busline, utc_offset=1)
            print "Match: " +str(match)
            for result in results:
                print result
            
            
if __name__ == "__main__":
    main()