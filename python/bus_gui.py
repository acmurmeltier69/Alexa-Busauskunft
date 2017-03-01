# coding: utf-8
###############################################################################
#
#       LIBRARY asag_gui
#
###############################################################################
# Functions to create information for the card output
#
###############################################################################


from myask import myask_log, myask_slots
import re
MAX_DISPLAY_CONNECTONS = 10

def ShowAlexaSlots(slots, appdef):
    #--------------------------------------------------------------------------
    # displays the alexa slots in the gui
    # parameters:
    # - slots: list of slots
    # - appdef: application definition (to (de-) canonicalize
    # Return (string): Multi-line card output
    #---------------------------------------------------------------------------
    
    cardtext = "ALEXA_SLOTS: "
    for thisslot in slots:
        m = re.search(r'literal$', thisslot)
        if m is None:
            cardtext += " '"+thisslot+"'='"+str(slots[thisslot])+"'"
#            if thisslot+".literal" in slots:
#                cardtext += "('"+ slots[thisslot+".literal"] + "')"
            cardtext += ",  "
    return cardtext

def DisplayGeneralHelp(user_profile):
    text_out  = u""
    text_out += u"Dieser Skill bietet Zugriff auf Live-Verbindungen und Abfahrtszeiten für den Nahverkehr in Aachen.\n"
    text_out += u"Beispiele für Fragen:\n"
    text_out += u"  'Wann fährt der nächste Bus ab Richterich Rathaus'.\n"
    text_out += u"  'Wann fährt die Linie 11 ab Elisenbrunnen.'\n"
    text_out += u"  'Wann fährt der nächste Bus von Ponttor nach Elisenbrunnen.'\n"
    text_out += u"Personalisierung:\n"
    text_out += u"Lege die bevorzugte Haltestelelle fest, um die Bedienung zu vereinfachen:\n"
    text_out += u"  'Ändere die bevorzugte Haltestelle auf Lukasstraße'\n"
    text_out += u"Danach kannst du einfach fragen:\n"
    text_out += u"  'Wann fährt der nächste Bus.'\n"
    text_out += u"und erhältst die nächsten Abfahrten ab Lukasstraße.\n"

    return text_out
def DisplayBusstopList(matches, slots, appdef):
    display_text = ""
    display_text += "Ich habe mehrere passende Haltestellen gefunden."
    display_text += "Das kann ich noch nicht."
    return display_text

def DisplayDeparture(connection, slots, appdef):
    display_text = ""
    (dep_time, busnr, destination) = connection
    display_text += u"Ab "+ dep_time.strftime('%H:%M')
    display_text += u" Linie " + str(busnr) 
    display_text += u" --> " + destination +u"\n"
    return display_text

def ShowDepartureList(departure_list, slots, appdef):
    #--------------------------------------------------------------------------
    # displays information on bus departures
    # parameters:
    # - departure list
    # - slots: list of slots
    # - appdef: application definition (to (de-) canonicalize
    # Return (string): Multi-line card output
    #---------------------------------------------------------------------------
    if  myask_slots.checkslots(slots, ['lang', 'qorg_id'],"ShowDepartureList") == False: 
        return myask_slots.error_slots_missing("ShowDepartureList")

    display_text = ""
    num_departures = len(departure_list)
    if num_departures == 0:
        display_text =  u"Keine Abfahrten "
        display_text += u" ab " + appdef.GetSlotOutputName("Origin", slots['qorg_id'])+u" ("+str(slots['qorg_id'])+u")"
        if 'Buslinie' in slots:
            display_text += u" für  Linie"+str(slots['Buslinie'])    
        display_text += u" gefunden."
    else:
        display_text =  str(num_departures) +u" Abfahrt(en)"
        display_text += u" ab " + appdef.GetSlotOutputName("Origin", slots['qorg_id'])+u" ("+str(slots['qorg_id'])+u")"
        display_text += u" gefunden.\n"
        if num_departures > MAX_DISPLAY_CONNECTONS: 
            num_departures = MAX_DISPLAY_CONNECTONS
            display_text += u"Hier sind die ersten "+str(num_departures)+u"\n"
        for i in range(num_departures):
            display_text += DisplayDeparture(departure_list[i], slots, appdef)
 
    return display_text

def DisplayJourneySimple(journey, slots, appdef):
    if 'legs' not in journey or len(journey['legs']) == 0:
        display_text = "ERROR_IN_CONNECION"
        myask_log.error("DisplayJourneySimple: cannot present connection: "+str(journey))
    else:
        display_text = u'{:5s} ab {:15s} --> {:15s} an {:5s} {:d} Umstiege '.format(
            journey['start_datetime'].strftime('%H:%M'),
            unicode(journey['start_loc']),
            unicode(journey['end_loc']),
            journey['end_datetime'].strftime('%H:%M'),
            len(journey['legs'])-1)
        display_text += "("
        firstleg=True
        for leg in journey['legs']:
            if firstleg: firstleg=False
            else: display_text +=", "
            if leg['type'] == "bus":
                if 'line' in leg:
                    display_text += "Bus " + leg['line']
                else:
                    display_text += "Bus ??"
            elif leg['type'] == "walk":
                    display_text += "laufen"
        display_text += ")\n"
    return display_text

def DisplayConnectionList(connection_list, slots, appdef):
    if  myask_slots.checkslots(slots, ['lang', 'qorg_id', 'qdest_id'],"DisplayConnectionList") == False: 
        return myask_slots.error_slots_missing("DisplayConnectionList")

    display_text = ""
    num_connections = len(connection_list)
    if  num_connections == 0:
        display_text = "Keine Verbindung"
        display_text += " von " + appdef.GetSlotOutputName("Origin", slots['qorg_id'])
        display_text += " nach " + appdef.GetSlotOutputName("Destination", slots['qdest_id'])
        display_text += " gefunden."
    else:
        display_text = str(num_connections) + " Verbindungen"
        display_text += " von " + appdef.GetSlotOutputName("Origin", slots['qorg_id'])
        display_text += " nach " + appdef.GetSlotOutputName("Destination", slots['qdest_id'])
        display_text += " gefunden.\n"
        counter = 0
        for journey in connection_list:
            counter +=1
            display_text += str(counter) +". : "
            display_text += DisplayJourneySimple(journey, slots, appdef)
            
    return display_text