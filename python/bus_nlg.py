# coding: utf-8
###############################################################################
#
#       LIBRARY asag nlg
#
###############################################################################
# Generic helper functions for the family calendar skill
#
###############################################################################

MAX_CONNECTONS = 3

from myask import myask_slots, myask_log

def Welcome(user_profile, counter):
    if counter == 0:
        speech_prompt = u"Hallo, welche Busauskunft brauchst du."
    else: speech_prompt = u"Sorry, ich habe den Befehl nicht verstanden"
  
    return speech_prompt

def SessionEnd():
    speech_prompt =  u"Dann bis zum nächsten Mal." 
    return speech_prompt
    
def generalHelp(user_profile):
    speech_prompt  = u"Hallo,<break/>"
    speech_prompt += u"Dieser Skill bietet Zugriff auf Live-Verbindungen und Abfahrtszeiten für den Nahverkehr in Aachen.<break/>"
    speech_prompt += u"Du kannst mir Fragen stellen wie zum Beispiel:"
    speech_prompt += u"<p>Wann fährt der nächste Bus ab Richterich Rathaus.</p>"
    speech_prompt += u"<p>Wann fährt die Linie 11 ab Elisenbrunnen.</p>"
    speech_prompt += u" oder "
    speech_prompt += u"<p>Wann fährt der nächste Bus von Ponttor nach Elisenbrunnen.</p>"
    speech_prompt += u"Du kannst diesen Skill personalisieren, um  Anfragen von deiner nächstgelegenen Bushaltestelle noch einfacher zu machen.<break/>"
    speech_prompt += u"Sage zum Beispiel: "
    speech_prompt += u"<p>Ändere die bevorzugte Haltestelle auf Lukasstraße</p>"
    speech_prompt += u"Danach kannst du einfach fragen:"
    speech_prompt += u"<p>Wann fährt der nächste Bus.</p>"
    speech_prompt += u"und erhältst die nächsten Abfahrten ab Lukasstraße."
    speech_prompt += u"<break/>"
    speech_prompt += u"Was kann ich für dich tun?."
    
    return speech_prompt

def GeneralError(errorstring, slots, appdef, user_profile):
    speech_prompt  = u"Es tut mir leid, es ist ein Problem aufgetreten."
    speech_prompt += u"Error in " +str(errorstring)
    return speech_prompt

def InvalidUserProfile(user_profile):
    speech_prompt = u"Sorry, Die Standardhaltestelle ist ungültig.<break/>"
    speech_prompt += u"Bitte versuche es noch einmal.<break/>"
    return speech_prompt
        
def DefaultStationMissing(slots, appdef, user_profile):
    speech_prompt = u"Entschuldigung, ich habe die Standard Haltestelle nicht verstanden.<break/>"
    speech_prompt += u"Bitte versuche es noch einmal.<break/>"
    return speech_prompt

def FavConMissing(slots, appdef, user_profile):
    speech_prompt = u"Entschuldigung, ich habe die gesuchte Verbindung nicht verstanden.<break/>"
    speech_prompt += u"Bitte versuche es noch einmal.<break/>"
    return speech_prompt
    
def OriginMissing(slots, appdef, user_profile):
    speech_prompt = u"Entschuldigung, ich habe die Abfahrtshaltestelle nicht verstanden.<break/>"
    speech_prompt += u"Bitte versuche es noch einmal.<break/>"
    return speech_prompt
    
def DestinationMissing(slots, appdef, user_profile):       
    speech_prompt = ""
    speech_prompt += u"Es tut mir leid, ich habe das Fahrziel leider nicht verstanden.<break/>"
    speech_prompt += u"Bitte versuche es noch einmal.<break/>"
    return speech_prompt
    
def InfoNotInUserProfile(slots, appdef, user_profile):
    speech_prompt = u"Ich habe diese information nicht im Benutzerprofil gefunden.<break/>"
    speech_prompt += u"Bitte versuche es noch einmal.<break/>"
    return speech_prompt

def FavoriteConnectionNotInProfile(slots, appdef, user_profile):
    speech_prompt = u"Ich habe die gesuchte Verbindung nicht in ihrem profil gefunden.<break/>"
    speech_prompt += u"Bitte versuche es noch einmal.<break/>"
    return speech_prompt

def UnknownOriginBusstop(station_name, slots, appdef, user_profile):
    speech_prompt = ""
    speech_prompt += u"Es tut mir leid, ich kann die Abfahrtshaltestelle "
    speech_prompt += station_name 
    speech_prompt += u" nicht finden.<break/>"
    speech_prompt += u"Bitte versuche es noch einmal.<break/>"
    return speech_prompt

def UnknownDestinationBusstop(station, slots, appdef, user_profile):
    speech_prompt = ""
    speech_prompt += u"Es tut mir leid, ich kann die Zielhaltestelle "+ station + u" nicht finden.<break/>"
    speech_prompt += u"Bitte versuche es noch einmal.<break/>"
    return speech_prompt

def PleaseSetDefaultStation(slots):
    speech_prompt =  u"Ich weiss nicht, von welcher Station du abfahren willst.<break/>"
    speech_prompt += u"Wiederhole das Kommando mit einer Abfahrtsstation " +\
                        u"oder lege eine bevorzugte Haltestelle fest.<break/>"
    speech_prompt += u"Benutze dazu das Kommando 'ändere die bevorzugte haltestelle.<break/>"
    speech_prompt += u"Also zum Beispiel:"
    speech_prompt += u" ändere die bevorzugte haltestelle zu kohlscheid technologiepark"
    return speech_prompt
       
def DefaultStationChanged(stationid, slots, appdef):
    speech_prompt = u"Ich habe die Station "
    speech_prompt +=  appdef.GetSpokenSlotOutputName("Origin", stationid)
    speech_prompt += u" als neue bevorzugte haltestelle eingetragen.<break/>"
    speech_prompt += u"Um das wieder zu ändern, benutze das Kommando: "
    speech_prompt += u" ändere die bevorzugte haltestelle<break/>"
    return speech_prompt
       
def DefaultStationUnchanged(stationid, slots, appdef):
    speech_prompt =  u"Die bevorzugte haltestelle wurde nicht geändert.<break/>"
    speech_prompt += u"Die bevorzugte haltestelle bleibt weiterhin: "
    speech_prompt +=  appdef.GetSpokenSlotOutputName("Origin", stationid)
    return speech_prompt
       
def ConfirmDefaultStationChange(stationid, slots, appdef, user_profile):
    speech_prompt = u"Du willst also deine bevorzugte Haltestelle ändern zu: "
    speech_prompt +=  appdef.GetSpokenSlotOutputName("Origin", stationid)
    return speech_prompt
       
def AeagServerError(slots, appdef, user_profile):
    speech_prompt = u"Es tut mir leid,"
    speech_prompt += u"Es gibt scheinbar ein Problem mit dem Fahrplan-Server."
    return speech_prompt

def SpeakDepartures(departure_list, slots, appdef):
    if 'Busline' in slots: 
        if slots['Busline'] == '?': 
            if 'Busline.literal' in slots:
                out = u'Es tut mir leid, ich kenne die Busnummer '+slots['Busline.literal']+ u' nicht.<break/> '
            else:
                out = u'Es tut mir leid, ich kenne diesen Bus nicht.<break/> '
            return out + SpeakDeparturesList(departure_list, slots, appdef)
        else: 
            return SpeakLineDepartures(departure_list, slots, appdef)
    else:
        return SpeakDeparturesList(departure_list, slots, appdef)


def SpeakLineDepartures(departure_list, slots, appdef):
    # list departures of apsecific bus line from a specific busstop
    if  myask_slots.checkslots(slots, ['lang', 'qorg_id', 'Busline'],"SpeakLineDepartures") == False: 
        return myask_slots.error_slots_missing("SpeakConnectionList")
    
    speech_prompt = u""
    numconnections = len(departure_list)
    if numconnections == 0:
        speech_prompt += u"ich habe Keine Abfahrten "
        speech_prompt += u"der Linie " + str(slots['Busline'])
        speech_prompt += u" ab " + appdef.GetSpokenSlotOutputName("Origin", slots['qorg_id']) 
        if "Direction" in slots:
            speech_prompt += u" " +appdef.GetSpokenSlotOutputName("Direction", slots["Direction"])
        speech_prompt += u" gefunden.<break/>"
    else:
        speech_prompt += u"Die Linie " + str(slots['Busline'])
        speech_prompt += u" fährt ab " + appdef.GetSpokenSlotOutputName("Origin", slots['qorg_id'])
        if "Direction" in slots:
            speech_prompt += u" " +appdef.GetSpokenSlotOutputName("Direction", slots["Direction"])
        speech_prompt += u":"
    listcounter = 1
    if numconnections > MAX_CONNECTONS: numconnections = MAX_CONNECTONS
    for departure in departure_list:
        if listcounter > numconnections: break
        listcounter += 1
        (dep_time, busnr, destination) = departure
        speech_prompt += u" um " + dep_time.strftime('%H:%M')
        speech_prompt += u" richtung " + destination +u". <break/>"
        if listcounter == numconnections:
            speech_prompt += u" und "
            
    return speech_prompt
   

def SpeakDeparture(connection, slots, appdef):
    speech_prompt = u""
    (dep_time, busnr, destination) = connection
    speech_prompt += u"Um " + dep_time.strftime('%H:%M')
    speech_prompt += u" fährt die linie " + str(busnr) + u" richtung " + destination +u". <break/>"
    return speech_prompt

 
def SpeakDeparturesList(departure_list, slots, appdef):
    # speak full information for  departures from  station qorg_id
    if  myask_slots.checkslots(slots, ['lang', 'qorg_id'],"SpeakDeparturesList") == False: 
        return myask_slots.error_slots_missing("SpeakDeparturesList")
        
    speech_prompt = u""
    num_departures = len(departure_list)
    if num_departures == 0:
        speech_prompt =  u"ich habe Keine Abfahrten "
        speech_prompt += u" ab " +  appdef.GetSpokenSlotOutputName("Origin", slots['qorg_id'])
        if "Direction" in slots:
            speech_prompt += u" Richtung "+appdef.GetSpokenSlotOutputName("Direction", slots["Direction"])
        speech_prompt += u" gefunden.<break/>"
    elif num_departures == 1:
        speech_prompt = u"Ich habe folgende Abfahrt"
        speech_prompt += u" ab "  +  appdef.GetSpokenSlotOutputName("Origin", slots['qorg_id'])
        if "Direction" in slots:
            speech_prompt += u" Richtung "+appdef.GetSpokenSlotOutputName("Direction", slots["Direction"])
        speech_prompt += u" gefunden.<break/>"
        speech_prompt += SpeakDeparture(departure_list[0], slots, appdef)
    elif num_departures > MAX_CONNECTONS:
        speech_prompt += u"Hier sind die ersten " + str(MAX_CONNECTONS)
        speech_prompt += u" Abfahrten ab " +  appdef.GetSpokenSlotOutputName("Origin", slots['qorg_id'])
        if "Direction" in slots:
            speech_prompt += u" Richtung "+ appdef.GetSpokenSlotOutputName("Direction", slots["Direction"])
        speech_prompt += u".<break/>"
        for i in range (MAX_CONNECTONS):
            speech_prompt += SpeakDeparture(departure_list[i], slots, appdef)
    else:
        speech_prompt = u"Ich habe die folgenden Abfahrten"
        speech_prompt += u" ab " +  appdef.GetSpokenSlotOutputName("Origin", slots['qorg_id'])
        if "Direction" in slots:
            speech_prompt += u" Richtung "+appdef.GetSpokenSlotOutputName("Direction", slots["Direction"])
        speech_prompt += u" gefunden.<break/>"
        for departure in departure_list:
            speech_prompt += SpeakDeparture(departure, slots, appdef)
    return speech_prompt 
    

def SpeakConnection(journey, slots, appdef):
    speech_output = ""
    if 'legs' not in journey or len(journey['legs']) == 0:
        speech_output += u"Diese Verbindung kann ich noch nicht vorlesen.<break/>"
        myask_log.error("DisplayJourneySimple: cannot present connection: "+str(journey))
    elif len(journey['legs']) == 1: #direct connection
        leg =journey['legs'][0]
        if leg['type'] == "bus":
            if 'line' in leg:
                speech_output += u"Mit der Linie " + leg['line']
            else:
                speech_output += u"Mit dem Bus"
        speech_output += u" <break/> "        
        speech_output += u" Abfahrt "+ journey['start_loc']
        speech_output += u" um "+ journey['start_datetime'].strftime('%H:%M') +" . "
        speech_output += u" Ankunft " + journey['end_loc']
        speech_output += u" um "+ journey['end_datetime'].strftime('%H:%M') +" . "
    else: # multi-leg trip
        speech_output += u"Mit "
        firstleg = True
        for leg in journey['legs']:
            if firstleg: firstleg = False
            else: speech_output += u" und "
            if leg['type'] == u"bus":
                if 'line' in leg:
                    speech_output += u"Bus " + leg['line']
                else:
                    speech_output += u"Bus"
            elif leg['type'] == "walk":
                    speech_output += u"Fussweg"
        speech_output += u" <break/>"            
        speech_output += u" Abfahrt "+ journey['start_loc']
        speech_output += u" um "+ journey['start_datetime'].strftime('%H:%M') +" . "
        speech_output += u" Ankunft " + journey['end_loc']
        speech_output += u" um "+ journey['end_datetime'].strftime('%H:%M') +" . "
    speech_output += u"<break/>"    
    return speech_output

def SpeakShortConnection(journey, slots, appdef):
    speech_output = ""
    if len(journey['legs']) == 0:
        speech_output += u"Diese Verbindung kann ich noch nicht vorlesen.<break/>"
    elif len(journey['legs']) == 1: #direct connection
        leg =journey['legs'][0]
        if leg['type'] == "bus":
            if 'line' in leg:
                speech_output += u"Mit der Linie " + leg['line']
            else:
                speech_output += u"Mit dem Bus"
        speech_output += u" <break/> "        
        speech_output += u" Abfahrt "
        speech_output +=  journey['start_datetime'].strftime('%H:%M') +" . "
        speech_output += u" Ankunft "
        speech_output += journey['end_datetime'].strftime('%H:%M') +" . "
    else: # multi-leg trip
        speech_output += u"Mit "
        firstleg = True
        for leg in journey['legs']:
            if firstleg: firstleg = False
            else: speech_output += u" und "
            if leg['type'] == u"bus":
                if 'line' in leg:
                    speech_output += u"Bus " + leg['line']
                else:
                    speech_output += u"Bus"
            elif leg['type'] == "walk":
                    speech_output += u"Fussweg"
        speech_output += u" <break/>"            
        speech_output += u" Abfahrt "+ journey['start_loc']
        speech_output += u" um "+ journey['start_datetime'].strftime('%H:%M') +" . "
        speech_output += u" Ankunft " + journey['end_loc']
        speech_output += u" um "+ journey['end_datetime'].strftime('%H:%M') +" . "
    speech_output += u"<break/>"    
    return speech_output

def SpeakConnectionDepArr(journey, slots, appdef):
    speech_output = ""
    if len(journey['legs']) == 0:
        speech_output += u"Diese Verbindung kann ich noch nicht vorlesen.<break/>"
    elif len(journey['legs']) == 1: #direct connection
        leg =journey['legs'][0]
        speech_output += u" Abfahrt "
        speech_output +=  journey['start_datetime'].strftime('%H:%M') +" , "
        speech_output += u" Ankunft "
        speech_output += journey['end_datetime'].strftime('%H:%M') +" . "
    else: # multi-leg trip
        speech_output += u"Mit "
        firstleg = True
        for leg in journey['legs']:
            if firstleg: firstleg = False
            else: speech_output += u" und "
            if leg['type'] == u"bus":
                if 'line' in leg:
                    speech_output += u"Bus " + leg['line']
                else:
                    speech_output += u"Bus"
            elif leg['type'] == "walk":
                    speech_output += u"Fussweg"
        speech_output += u" <break/>"            
        speech_output += u" Abfahrt "+ journey['start_loc']
        speech_output += u" um "+ journey['start_datetime'].strftime('%H:%M') +" . "
        speech_output += u" Ankunft " + journey['end_loc']
        speech_output += u" um "+ journey['end_datetime'].strftime('%H:%M') +" . "
    speech_output += u"<break/>"    
    return speech_output

def SpeakConnectionList(connection_list, slots, appdef):
    if  myask_slots.checkslots(slots, ['lang', 'qorg_id', 'qdest_id'],"SpeakConnectionList") == False: 
        return myask_slots.error_slots_missing("SpeakConnectionList")

    speech_output = ""
    num_connections = len(connection_list)
    if  num_connections == 0:
        speech_output = u"Ich habe keine Verbindung"
        speech_output += u" von " +  appdef.GetSpokenSlotOutputName("Origin", slots['qorg_id'])
        speech_output += u" nach " + appdef.GetSpokenSlotOutputName("Destination",slots['qdest_id'])
        speech_output += u" gefunden."
    elif num_connections ==1:
        speech_output = u"Ich habe die folgende Verbindung"
        speech_output += u" von " +  appdef.GetSpokenSlotOutputName("Origin", slots['qorg_id'])
        speech_output += u" nach " + appdef.GetSpokenSlotOutputName("Destination",slots['qdest_id'])
        speech_output += u" gefunden.<break/>"
        speech_output += SpeakConnection(connection_list[0], slots, appdef)
    else:
        speech_output = u"Ich habe " + str(num_connections) + u" Verbindungen"
        speech_output += u" von " +  appdef.GetSpokenSlotOutputName("Origin", slots['qorg_id'])
        speech_output += u" nach " + appdef.GetSpokenSlotOutputName("Destination",slots['qdest_id'])
        speech_output += u" gefunden.<break/>"
        counter = 0
        for connection in connection_list:
            counter +=1
            speech_output += str(counter) + u". Verbindung<break/> "
            speech_output += SpeakConnection(connection, slots, appdef)

    return speech_output

def SpeakFavoriteConnections(match,connection_list, slots, appdef, user_profile):
    if  myask_slots.checkslots(slots, ['lang', 'qorg_id', 'qdest_id'],"SpeakFavoriteConnections") == False: 
        return myask_slots.error_slots_missing("SpeakFavoriteConnections")
    
    speech_output = ""
    num_connections = len(connection_list)
    if  num_connections == 0:
        speech_output = u"Ich habe keine Verbindung"
        speech_output += u" von " +  appdef.GetSpokenSlotOutputName("Origin", slots['qorg_id'])
        speech_output += u" nach " + appdef.GetSpokenSlotOutputName("Destination",slots['qdest_id'])
        speech_output += u" gefunden."
    elif match == False:
        speech_output = u"Ich habe die Lieblingsverbindung nicht gefunden. "
        speech_output += u"Hier sind Alternativen: <break/>"
        counter = 0
        for connection in connection_list:
            counter +=1
            speech_output += SpeakConnection(connection_list[0], slots, appdef)
    elif 'Buslines' in slots and len(slots['Buslines']) == 1:
        speech_output = u"Hier sind die gewünschen Lieblingsverbindungen "
        speech_output += u" mit der Linie " + str(slots['Buslines'][0])
        speech_output += u" von " +  appdef.GetSpokenSlotOutputName("Origin", slots['qorg_id'])
        speech_output += u" nach " + appdef.GetSpokenSlotOutputName("Destination",slots['qdest_id'])
        speech_output += u":"     
        counter = 0
        for connection in connection_list:
            counter +=1
            speech_output += SpeakConnectionDepArr(connection, slots, appdef)
            if counter == len(connection_list)-1:
                speech_output += u" und " 
    else:
        speech_output = u"Hier sind die gewünschen Lieblingsverbindungen: "
        counter = 0
        for connection in connection_list:
            counter +=1
            speech_output += SpeakShortConnection(connection, slots, appdef)

    return speech_output
