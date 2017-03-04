# coding: utf-8
"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import locale
from myask import myask_log, myask_slots, myask_appdef, myask_alexaout

import bus_appdef
import aseag_api
import bus_userprofile
import bus_response

def get_user_profile(session):
    #get the user id from the request
    if session['user']['userId'] == "":
        myask_log.error("Missing field 'session.user.userId'. Assuming default user")
        user_profile = bus_userprofile.userProfile("") # create default_profile
    else:
        user_profile = bus_userprofile.userProfile(session['user']['userId'])


    return user_profile


# --------------- output functions ------------------

################################################################################   
def ToInt(stop_id):
    try:
        stop_id = int(stop_id)
    except ValueError:
        pass  # it was a string, not an int.  
        return 0
    else:
        return stop_id

def getOriginStop(slots, appdef, user_profile):
    # parses slots and returns a valid stopID and Name from(in this order)
    #  1) slot 'Origin' (shortlist) --> map name to ID
    #  2) slot 'OriginStation' + slots  'OriginCity' 
    #  3) slot 'OriginStation'
    #  4) slots  'OriginCity' (uses default station for the city)
    #  5) information from previous turn via session attribute qorg_id 
    #  6) user profile DefaultStation
    # RETURNS ID for bus stop, 0 if none found
    
    # check if we got a new station in the request                
    if 'Origin' in slots:
        org_id = slots["Origin"]
    elif  'OriginCity' in slots:
        org_id  = aseag_api.GetDefaultStopIdByCity(slots['OriginCity'] )
    elif 'qorg_id' in slots:   # check if there is a station from the dialog context to re-use
        org_id = slots['qorg_id']
    else: # no information found. Use default location from user profile
        org_id = user_profile.GetDefaultStopId()

    return(ToInt(org_id))
        
def getDestinationStop(slots, appdef, user_profile):
    # parses slots and returns a valid stopID and Name from(in this order)
    #  1) slot 'Destination' (shortlist) --> map name to ID
    #  2) slot 'DestinationStation' + slots  'DestinationCity' 
    #  3) slot 'DestinationStation'
    #  4) slot 'DestinationCity' (uses default station for the city)
    #  5) slot 'Favorites'
    #  6) information from previous session (qdest_id)
    # RETURNS
    # array of valid ID, Name pairs where
    # if no matches were found or information was invalid, array has len 0
    # if a unique id was found array has len 1
    # if multiple options were found len > 1
    
    # remember the information we already have
    
    # check if we got a new station in the request                
    if 'Destination' in slots:
        dest_id = slots["Destination"]
    elif  'DestinationCity' in slots:
        dest_id  = aseag_api.GetDefaultStopIdByCity(slots['DestinationCity'] )
    elif 'qdest_id' in slots:   # check if there is a station from the dialog context to re-use
        dest_id = slots['qdest_id']
    else: # no information found. Use default location from user profile
        dest_id = 0

    return(ToInt(dest_id))
      
def _FetchConnections(slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Finds connections from one bus stop to another
    #
    # Requires the following slots to be set:
    # 'qorg_id' bus stop ID for the origin stop
    # 'qdest_is' bus stop ID for the destination stop
    # Optional slots (used to filter the results=
    #    "Busline"  : list only this buses for a specific line
    #    "Next"      : (future) List only next or next N connections
    #    "Transport" : (future) Filter by Mode of Transport: Bus, Train, Direct
    # RETURNS: Alexa output structure
    #--------------------------------------------------------------------------
       
    if  myask_slots.checkslots(slots, ['lang', 'qorg_id', 'qdest_id'],"_FetchConnections") == False: 
        return myask_alexaout.createAlexaErrorOutput(myask_slots.error_slots_missing("_FetchConnections"), slots)
        
    myask_log.debug(3, "In Function _FindConnection " + str(slots['qorg_id'])+ "-->"+str(slots['qdest_id']))

    # prepare slots for call to aseag API
 
    # convert all times to localtime, independent of the AWS server location
    if 'utc_offset' in slots: utc_offset = slots['utc_offset']
    else: utc_offset = 0            

    if 'Busline' in slots and slots['Busline'] != "?" : linefilter = slots['Busline']
    else: linefilter = ''
     
    if 'Transport' in slots: transport = slots['Transport']
    else: transport = ""

    match, result_connections = aseag_api.GetFilteredConnections(slots['qorg_id'], slots['qdest_id'], linefilter, transport, utc_offset)
                     
    myask_log.debug(2, "connection results from "+ str(slots['qorg_id'])+ " to " + str(slots['qdest_id'])+ \
                    "match:" +str(match)+":\n" + str(result_connections))
  
    return bus_response.out_Connections(result_connections, slots, appdef, user_profile)  



################################################################################
#
# handler functions for individual speech intents
#
################################################################################
def process_GetDeparturesFromFavorite(slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Shows live departures from the user's default connection
    # 
    # Intent: 'DeparturesFromFavorite'
    # Slots:  (used to filter departures)
    #    "Direction" : lists only inbound / outbound buses
    #    "Busline"  : list only buses for a specific line
    #    "Next"      : (future) List only next or next N connections
    #    "Transport" : FIlter by Mode of Transport: Bus, Train, Direct
    #--------------------------------------------------------------------------
    myask_log.debug(3, "Got intent 'GetDeparturesFromFavorite'")

    # convert all times to localtime, independent of the AWS server location
    if 'utc_offset' in slots: utc_offset = slots['utc_offset']
    else: utc_offset = 0            

    if 'Busline' in slots and slots['Busline'] != "?" : linefilter = slots['Busline']
    else:   linefilter = ''
 
    if "Direction" in slots: direction = slots["Direction"]
    else: direction = ""

    #-----------------------------------------------------------------------
    # get ID for origin stop from user profile
    #-----------------------------------------------------------------------    
    if user_profile.isKnownUser():
        slots['qorg_id'] = ToInt(user_profile.GetDefaultStopId())
    else:
        return bus_response.out_PromptUserProfileNeeded(slots)
    
    if(slots['qorg_id']) < 10000: return bus_response.out_InvalidFavorite(user_profile)
    
    results = aseag_api.GetDepartures(slots['qorg_id'], linefilter, direction, utc_offset)
    return bus_response.out_Departures(results, slots, appdef, user_profile)

def process_GetDeparturesFromOther(slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Shows live departures from a specific station 'origin'
    # 
    # Intent: 'Departures'
    # Slots:  
    #    "Origin"    : station from which the departures are requested
    #    "Direction" : lists only inbound / outbound buses
    #    "Busline"  : list only buses for a specific line
    #    "Next"      : (future) List only next or next N connections
    #    "Transport" : FIlter by Mode of Transport: Bus, Train, Direct
    #--------------------------------------------------------------------------
    myask_log.debug(3, "Got intent 'GetDeparturesFromOther'")

    # convert all times to localtime, independent of the AWS server location
    if 'utc_offset' in slots: utc_offset = slots['utc_offset']
    else: utc_offset = 0            

    if 'Busline' in slots and slots['Busline'] != "?" : linefilter = slots['Busline']
    else:   linefilter = ''
 
    if "Direction" in slots: direction = slots["Direction"]
    else: direction = ""

    #-----------------------------------------------------------------------
    # get ID for origin stop
    #-----------------------------------------------------------------------    
    if 'Origin' not in slots:
        myask_log.debug(5, "Slot 'Origin' missing in GetDeparturesFromOther...")
        if user_profile.HasDefaultStop():
            # user favorite as fall-back
            slots['qorg_id'] = ToInt(user_profile.GetDefaultStopId())
            myask_log.debug(5, "...Using user profile default instead")
        else:
            myask_log.debug(5, "...and no default stop found in user profile")
            return bus_response.out_OriginMissing(slots, appdef, user_profile)

    else:
        slots['qorg_id'] = ToInt(slots['Origin'])

    if slots['qorg_id'] < 10000:
        if 'Origin.literal' in slots['Origin.literal']:
            return bus_response.out_InvalidOrigin(slots['Origin.literal'], slots, appdef, user_profile)
        else:
            return bus_response.out_InvalidOrigin('', slots, appdef, user_profile)
    else: 
        results = aseag_api.GetDepartures(slots['qorg_id'], linefilter, direction, utc_offset)
        return bus_response.out_Departures(results, slots, appdef, user_profile)

    # if we are here, something went wrong
    return bus_response.out_ImplementationError("GetDeparturesFromOther", slots, appdef, user_profile)

def process_GetFavConnecionDepartures(slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # shows departures a favorite connection from the uer's user profile
    # 
    # Intent: 'GetFavConnecionDepartures'
    # Slot: 'FavConnection' identifier for a favorite connection from the user profile
    # A favorite connection (slot '') from the user profile provides
    #  - departure station
    #  - destination station
    #  - preferred busline (optional)
    #  - preferred time-window (optional)         
    #--------------------------------------------------------------------------
    myask_log.debug(3, "Got intent 'GetFavConnecionDepartures'")
    
    if 'FavConnection' not in slots:
        return bus_response.out_FavoriteConnectionMissing(slots, appdef, user_profile)
    
    else:
        fav_connection = user_profile.GetFavoriteConnection(slots["FavConnection"])
        if len(fav_connection) == 0: 
            return bus_response.out_FavoriteConnectionNotInUserProfile(slots["FavConnection"], 
                                                                       slots, appdef, user_profile)
        else: # favorite connection found    
            if "OrgID" not in fav_connection or "DestID" not in fav_connection:
                myask_log.warning("No StartID or StopID found in FavoriteConnection '"+slots["FavConnection"]+"' for user ")
                return bus_response.out_InvalidFavoriteConnection(slots, appdef, user_profile)
            else:
                if "PreferredLines"  in fav_connection: linefilter = fav_connection["PreferredLine"] 
                else: linefilter = ''

                if "DepTimeWindowStart" in fav_connection: start_time = fav_connection["DepTimeWindowStart"]
                else: start_time = ""

                if "DepTimeWindowEnd" in fav_connection: end_time = fav_connection["DepTimeWindowEnd"]
                else: end_time = ""

                if 'utc_offset' in slots: utc_offset = slots['utc_offset']
                else: utc_offset = 0            

                (match, result_connections) = aseag_api.FindFavoriteConnetions(fav_connection["OrgID"],
                                                                               fav_connection["DestID"],
                                                                               start_time, end_time,
                                                                               linefilter, utc_offset)
                # put it in the normal fields for smooth output
                slots['qorg_id'] = ToInt(fav_connection["OrgID"])
                slots['qdest_id'] = ToInt(fav_connection["DestID"])
                if linefilter != '' : slots['Busline'] = str(linefilter)
                return bus_response.out_FavoriteConnection(match, result_connections, slots, appdef, user_profile)

    # if we are here, something went wrong
    return bus_response.out_ImplementationError("process_GetFavConnecionDepartures", slots, appdef, user_profile)

def process_FindConnectionFromFavorite(slots, appdef, user_profile):
    #---------------------------------------------------------------------------
    # Lists connections to a specific station from the user's default station
    #
    # Intent: 'FindConnectionFromFavorite'
    # Slots: 
    #  - "Destination"  station to which connections  should be found
    #  - "DestinationCity"
    #    "Busline"  : list only buses for a specific line
    #    "Next"      : (future) List only next or next N connections
    #    "Transport" : Filter by Mode of Transport: Bus, Train, Direct
    # Origin is set to the user's default sstation
    #---------------------------------------------------------------------------
    myask_log.debug(3, "Got intent FindConnectionFromFavorite")
 

    #-----------------------------------------------------------------------
    # fill origin  ID from user profile
    #-----------------------------------------------------------------------    
    if user_profile.isKnownUser():
        slots['qorg_id'] = ToInt(user_profile.GetDefaultStopId())
    else:
        return bus_response.out_PromptUserProfileNeeded(slots)

    #-------------------------------------------------------------------------
    # fill destination ID
    #-------------------------------------------------------------------------
    if 'Destination' in slots:
        destination_id = ToInt(slots["Destination"])
        destination_str = slots["Destination"]
    elif 'qdest_id' in slots:   # check if there is a station from the dialog context to re-use
        destination_id = ToInt(slots['qdest_id'])
        destination_str = "" 
    else: # no information found. Use default location from user profile
        return bus_response.out_DestinationMissing(slots, appdef, user_profile)
   
    
    myask_log.debug(5, "Got destination ID "+str(destination_id))
    if int(destination_id) < 10000:
        myask_log.warning("Invalid stop id for destination station:"+ str(destination_id))
        if 'Destination.literal' in slots:
            return bus_response.out_InvalidDestination(slots["Destination.literal"], slots, appdef, user_profile)
        else:
            return bus_response.out_InvalidDestination(destination_str, slots, appdef, user_profile)

    # we got a single result
    slots['qdest_id'] = destination_id

    return _FetchConnections(slots, appdef, user_profile)


def process_FindConnectionFromOther(slots, appdef, user_profile):
    #---------------------------------------------------------------------------
    # Lists connections from a specific station to a specific station
    #
    # Intent: 'FindConnection'
    # Slots: 
    #  - "Origin"  station to which connections  should be found
    #  - "OriginCity"
    #  - "Destination"  station to which connections  should be found
    #  - "DestinationCity"
    #    "Busline"  : list only buses for a specific line
    #    "Next"      : (future) List only next or next N connections
    #    "Transport" : Filter by Mode of Transport: Bus, Train, Direct
    # Origin is set to the user's default sstation
    #---------------------------------------------------------------------------
    myask_log.debug(3, "Got intent FindConnectionFromOther")
 
    # convert all times to localtime, independent of the AWS server location
    
    #-----------------------------------------------------------------------
    # get ID for origin stop
    #-----------------------------------------------------------------------    
    if 'Origin' not in slots:
        if user_profile.isKnownUser():
            # user favorite as fall-back
            slots['qorg_id'] = ToInt(user_profile.GetDefaultStopId())
        else:
            return bus_response.out_OriginMissing(slots, appdef, user_profile)
    else:
        slots['qorg_id'] = ToInt(slots['Origin'])

    if slots['qorg_id'] < 10000:
        if 'Origin.literal' in slots:
            return bus_response.out_InvalidOrigin(slots['Origin.literal'], slots, appdef, user_profile)
        else:
            return bus_response.out_InvalidOrigin(slots['Origin'], slots, appdef, user_profile)
    
        
    #-------------------------------------------------------------------------
    # fill destination ID
    #-------------------------------------------------------------------------
    if 'Destination' in slots:
        destination_id = ToInt(slots["Destination"])
        destination_str = slots["Destination"]
    elif 'qdest_id' in slots:   # check if there is a station from the dialog context to re-use
        destination_id = ToInt(slots['qdest_id'])
        destination_str = "" 
    else: # no information found. Use default location from user profile
        return bus_response.out_DestinationMissing(slots, appdef, user_profile)

    if int(destination_id) < 10000:
        myask_log.warning("Invalid stop id for destination station:"+ str(destination_id))
        if 'Destination.literal' in slots:
            return bus_response.out_InvalidDestination(slots['Destination.literal'], slots, appdef, user_profile)
        else:
            return bus_response.out_InvalidDestination(destination_str, slots, appdef, user_profile)

    # we got a single result
    slots['qdest_id'] = destination_id

    return _FetchConnections(slots, appdef, user_profile)
    
def process_ChangeDefaultStation(slots, appdef, user_profile):
    #---------------------------------------------------------------------------
    # Handles a user request to change the default stop
    # 
    # The system triggers a confirmation question back to the user
    # if the user answers with "yes" or "no", the function ConfirmChangeDefaultStation is called
    #---------------------------------------------------------------------------
    myask_log.debug(3, "Got intent 'GetFavConnecionDepartures'")

    if "Origin" not in slots:
        return bus_response.out_DefaultStationMissing(slots, appdef, user_profile)
    elif ToInt(slots["Origin"]) < 10000:
        return bus_response.out_DefaultStationMissing(slots, appdef, user_profile)
       
    slotlist = ["Origin"]
    session_attributes = myask_slots.store_session_slots("ChangeDefaultStation", slotlist, slots)

    return bus_response.out_ConfirmChangeFavorite(slots["Origin"], session_attributes, 
                                                  slots, appdef, user_profile)

 
def ConfirmChangeDefaultStation(slots, appdef, user_profile):
    #---------------------------------------------------------------------------
    # Handles confirmation of change of default slot
    # slot "Confirmed" contains the user answer
    #---------------------------------------------------------------------------
    if  myask_slots.checkslots(slots, ['lang', 'Confirmed'],"ConfirmChangeDefaultStation") == False: 
        return myask_alexaout.createAlexaErrorOutput(myask_slots.error_slots_missing("ConfirmChangeDefaultStation"), slots)

    myask_log.debug(3, "Got command 'ConfirmChangeDefaultStation'")
    
    if "Origin" in slots:
        new_default_id = slots["Origin"]
    else:
        myask_log.error("ConfirmChangeDefaultStation called without slot 'Origin'. How could this happen?")
        new_default_id = user_profile.GetDefaultStopId()

    if slots["Confirmed"] == True: # user confirmed
        myask_log.debug(5, "User has confirmed selection of new default station")
        myask_log.debug(2, "New default station is " + str(new_default_id))
        result = user_profile.SetDefaultStopId(new_default_id)
        if result:
            myask_log.debug(1, "New favorite set successfully")
        else:
            myask_log.error("New favorite could not be set")
        return bus_response.out_DefaultChanged(slots, appdef, user_profile)
    else: # user did not confirm
        return bus_response.out_DefaultChangeCancelled(slots, appdef, user_profile)
         
    # if we are here, something went wrong
    return bus_response.out_ImplementationError("process_GetFavConnecionDepartures", slots, appdef, user_profile)
    

def process_DeleteProfile(slots, appdef, user_profile):
    user_profile.DeleteUserProfile()
    return bus_response.out_ProfileDeleted(slots, appdef, user_profile)
     
################################################################################
################################################################################
#
#
#   event handlers   
#
#
################################################################################
################################################################################


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+
#+ main handler for alexa intents              on_intent
#+
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
def on_intent(intent_request, session,appdef, user_profile):
    #--------------------------------------------------------------------------
    # Main intent handler function.
    # Called when Alexa receives a speech intent
    
    """ Called when the user specifies an intent for this skill """

    myask_log.debug(5, "on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    current_intent = intent_request['intent']['name']
    input_locale = intent_request['locale'] 

    myask_log.debug(2,  "Got user profile: "+ str(user_profile.GetProfile()))
    
    if current_intent in ["AMAZON.YesIntent", "AMAZON.NoIntent"]:
        slots = myask_slots.parse_slots(intent, session, True, input_locale, appdef)
        if   current_intent == "AMAZON.YesIntent": slots["Confirmed"] = True
        elif current_intent == "AMAZON.NoIntent": slots["Confirmed"] = False
        if 'prev_intent' in slots:
            if slots["prev_intent"] == "ChangeDefaultStation":
                return ConfirmChangeDefaultStation(slots, appdef, user_profile)
            else:
                myask_alexaout.createAlexaErrorOutput("Oops, da ist was schiefgelaufen")
        else:
            myask_alexaout.createAlexaErrorOutput("Sorry, das habe ich nicht verstanden")
            
                
    slots = myask_slots.parse_slots(intent, session, False, input_locale, appdef)
    slots['current_intent'] = current_intent    
        
    #Now process the intent via the appropriate function
    myask_log.debug(3, "Handling current_intent='"+str(current_intent)+"'")    
    if   current_intent == "GetDeparturesFromFavorite": return process_GetDeparturesFromFavorite(slots, appdef, user_profile)
    elif current_intent == "GetDeparturesFromOther": return process_GetDeparturesFromOther(slots, appdef, user_profile)
    elif current_intent == "GetFavConnecionDepartures": return process_GetFavConnecionDepartures(slots, appdef, user_profile)
    elif current_intent == "FindConnectionFromFavorite": return process_FindConnectionFromFavorite(slots, appdef, user_profile)
    elif current_intent == "FindConnectionFromOther": return process_FindConnectionFromOther(slots, appdef, user_profile)
    elif current_intent == "ChangeDefaultStation": return process_ChangeDefaultStation(slots, appdef, user_profile)
    elif current_intent == "DeleteProfile": return process_DeleteProfile(slots, appdef, user_profile)
    elif current_intent == "AMAZON.HelpIntent":
        return bus_response.out_Help(user_profile)
    elif current_intent == "AMAZON.CancelIntent" or current_intent == "AMAZON.StopIntent":
        return bus_response.out_SessionEnd()
    else:
        raise ValueError("Invalid intent")

def on_session_started(session_started_request, session):
    # Called when the session starts 
    # gets the user_profile that belongs to this session
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session, user_profile):
    """ Called when the user launches the skill without specifying what they
    want
    """
    user_profile = get_user_profile(session)

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId']+", userName="+user_profile.getUserName())

    # Dispatch to your skill's launch
    return bus_response.out_Welcome(user_profile)


def on_session_ended(session_ended_request, session, user_profile):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=True
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context, iswin=False):
    DEVELOPMET_IDs=['LOCAL_TEST', 
                    'amzn1.ask.skill.a5cea9e0-a824-45e6-830f-5e048085f85d']  # andi debug
    
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    appdef = myask_appdef.applicationdef(bus_appdef.APPNAME, bus_appdef.APPID,
                                         bus_appdef.INTENTS, bus_appdef.SLOTS, 
                                         bus_appdef.SLOTTYPES)

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] != appdef.GetAppID())\
        and (event['session']['application']['applicationId'] not in  DEVELOPMET_IDs):
        raise ValueError("Invalid Application ID")


    # set locale according to input
    if event['request']['locale'] == "de-DE":
        if(iswin):
            locale.setlocale(locale.LC_ALL, "deu_deu")
        else:
            locale.setlocale(locale.LC_ALL, 'de_DE')
    elif event['request']['locale'] == "en-UK":
        locale.setlocale(locale.LC_ALL, 'en_GB')
    elif event['request']['locale'] == "en-US":
        locale.setlocale(locale.LC_ALL, 'en_US')
    else:
        locale.setlocale(locale.LC_ALL, 'en_US')
    user_profile = get_user_profile(event['session'])

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'], user_profile)
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'],appdef, user_profile)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'], user_profile)
