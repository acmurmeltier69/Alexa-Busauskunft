# coding: utf-8

import bus_nlg
import bus_gui

from myask import myask_log, myask_alexaout

def out_Welcome(user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for Welcome message
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("R0")
    out = myask_alexaout.alexaout()
    out.card_title = "Welcome"
    out.should_end_session = False
    out.speech_output = bus_nlg.Welcome(user_profile, 0)
    out.reprompt_text = bus_nlg.Welcome(user_profile, 1)
    out.card_text = bus_gui.DisplayGeneralHelp(user_profile) 
    return out.createOutput([])

def out_Welcome2(user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for Welcome message
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("R99")
    slots = {}
    slots['PrevIntent'] = 'Help'
    out = myask_alexaout.alexaout()
    out.card_title = "Help"
    out.speech_output = bus_nlg.generalHelp(user_profile) 
    out.card_text = bus_gui.DisplayGeneralHelp(user_profile) 
    return out.createOutput(slots)

def out_Help(user_profile): 
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for Help Request
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("R99")
    slots = {}
    slots['PrevIntent'] = 'Help'
    out = myask_alexaout.alexaout()
    out.card_title = "HELP"
    out.should_end_session = False
    out.speech_output = bus_nlg.generalHelp(user_profile) 
    out.card_text = bus_gui.DisplayGeneralHelp(user_profile) 
    return out.createOutput(slots)
  
def out_SessionEnd():
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for SessionEnd message
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("R98")
    slots = {}
    slots['PrevIntent'] = 'End'
    out = myask_alexaout.alexaout()
    out.card_title = bus_nlg.SessionEnd()
    out.DisplaySpeechOutputOnCard()        
    return out.createOutput(slots)

def out_Departures(results, slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for a list of bus connections
    # Parameters:
    #  'results' : list of departures
    #  'slots' : current slots (for debug output)
    #  'appdef': application data (for translating literals and canonicals)
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("R1")
    out = myask_alexaout.alexaout()
    out.speech_output = bus_nlg.SpeakDepartures(results, slots, appdef)
    out.card_text     = bus_gui.ShowDepartureList(results, slots, appdef)
    out.card_title = "GetDeparturesFromFavorite"   
    return out.createOutput(slots)

def out_Connections(results, slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for a list of bus connections
    # Parameters:
    #  'results' : list of departures
    #  'slots' : current slots (for debug output)
    #  'appdef': application data (for translating literals and canonicals)
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("R2")
    out = myask_alexaout.alexaout()
    out.speech_output = bus_nlg.SpeakConnectionList(results, slots, appdef)
    out.card_text = bus_gui.DisplayConnectionList(results, slots, appdef)
    return out.createOutput(slots)

def out_FavoriteConnection(match, results, slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for a list of bus connections
    # Parameters:
    #  'results' : list of departures
    #  'slots' : current slots (for debug output)
    #  'appdef': application data (for translating literals and canonicals)
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("R4")
    out = myask_alexaout.alexaout()
    out.speech_output = bus_nlg.SpeakFavoriteConnections(match, results, slots, appdef, user_profile)
    out.card_text = bus_gui.DisplayConnectionList(results, slots, appdef)
    return out.createOutput(slots)

def out_ConfirmChangeFavorite(station_id, session_attributes, slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure to ask user to confirm he wants to change default stop
    # Parameter
    #  'station_id' : ID for the new default station
    #  'slots' : current slots (for debug output)
    #  'appdef': application data (for translating literals and canonicals)
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("R3")
    out = myask_alexaout.alexaout()
    out.card_title = "ConfirmChangeFavorite"
    out.speech_output = bus_nlg.ConfirmDefaultStationChange(station_id, slots, appdef, user_profile)
    out.DisplaySpeechOutputOnCard()
    out.should_end_session = False
    return out.createOutput(slots, session_attributes)

def out_ProfileDeleted(slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for Warning message "FavoriteMissing"
    # Parameters:
    #  'slots' : current slots (for debug output)
    #  'appdef': application data (for translating literals and canonicals)
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("R10")
    out = myask_alexaout.alexaout()
    out.card_title = "ProfileDeleted"
    out.speech_output = ""
    out.DisplaySpeechOutputOnCard()        
    return out.createOutput(slots)   

def out_DefaultChanged(slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure to indicate that the default has been changed
    # Parameters:
    #  'slots' : current slots (for debug output)
    #  'appdef': application data (for translating literals and canonicals)
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("R11")
    out = myask_alexaout.alexaout()
    out.card_title = "DefaultStationChanged"
    out.speech_output = bus_nlg.DefaultStationChanged(user_profile.GetDefaultStopId(),  slots, appdef)
    out.DisplaySpeechOutputOnCard()
    return out.createOutput(slots)

def out_DefaultChangeCancelled(slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure to indicate that the default change has been cancelled
    # Parameters:
    #  'slots' : current slots (for debug output)
    #  'appdef': application data (for translating literals and canonicals)
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("R12")
    out = myask_alexaout.alexaout()
    out.card_title = "DefaultStationChanged"
    out.speech_output = bus_nlg.DefaultStationUnchanged(user_profile.GetDefaultStopId(),  slots, appdef)
    out.DisplaySpeechOutputOnCard()
    return out.createOutput(slots)

def out_DefaultStationMissing(slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for Warning message "FavoriteMissing"
    # Parameters:
    #  'slots' : current slots (for debug output)
    #  'appdef': application data (for translating literals and canonicals)
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("W1")
    out = myask_alexaout.alexaout()
    out.card_title = "DefaultStationMissing"
    out.speech_output = bus_nlg.DefaultStationMissing(slots, appdef, user_profile)
    out.DisplaySpeechOutputOnCard()        
    return out.createOutput(slots)
 
def out_PromptUserProfileNeeded(slots):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for Warning message "UserProfileNeeded"
    # Parameters:
    #  'slots' : current slots (for debug output)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("W2")
    out = myask_alexaout.alexaout()
    out.card_title = "User Profile needed"
    out.should_end_session = True
    out.speech_output = bus_nlg.PleaseSetDefaultStation(slots) 
    out.DisplaySpeechOutputOnCard()    
    return out.createOutput(slots)

def out_OriginMissing(slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for Warning message "OriginMissing"
    # Parameters:
    #  'slots' : current slots (for debug output)
    #  'appdef': application data (for translating literals and canonicals)
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("W3")
    out = myask_alexaout.alexaout()
    out.card_title = "OriginMissing"
    out.speech_output = bus_nlg.OriginMissing(slots, appdef, user_profile) 
    out.DisplaySpeechOutputOnCard()        
    return out.createOutput(slots)
 
def out_DestinationMissing(slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for Warning message "DestinationMissing"
    # Parameters:
    #  'slots' : current slots (for debug output)
    #  'appdef': application data (for translating literals and canonicals)
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("W4")
    out = myask_alexaout.alexaout()
    out.card_title = "DestinationMissing"
    out.speech_output = bus_nlg.DestinationMissing(slots, appdef, user_profile)
    out.DisplaySpeechOutputOnCard()        
    return out.createOutput(slots)
 
def out_FavoriteConnectionMissing(slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for Warning message "FavoriteConnectionMissing"
    # Parameters:
    #  'slots' : current slots (for debug output)
    #  'appdef': application data (for translating literals and canonicals)
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("W5")
    out = myask_alexaout.alexaout()
    out.card_title = "FavoriteConnectionMissing"
    out.speech_output = bus_nlg.FavConMissing(slots, appdef, user_profile)
    out.DisplaySpeechOutputOnCard()        
    return out.createOutput(slots)
 
def out_FavoriteConnectionNotInUserProfile(favcon, slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for Warning message "FavoriteConnection not found in profile"
    # Parameters:
    # 'favcon': Favorite connection identifier
    #  'slots' : current slots (for debug output)
    #  'appdef': application data (for translating literals and canonicals)
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("W10")
    out = myask_alexaout.alexaout()
    out.card_title = "FavoriteConnectionMissing"
    out.speech_output = bus_nlg.FavoriteConnectionNotInProfile(slots, appdef, user_profile)
    out.DisplaySpeechOutputOnCard()        
    return out.createOutput(slots)
    
def out_InvalidOrigin(station_name, slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for Warning message "InvalidOrigin"
    # Parameters:
    #  'slots' : current slots (for debug output)
    #  'appdef': application data (for translating literals and canonicals)
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("W6")
    out = myask_alexaout.alexaout()
    out.card_title = "InvalidOrigin"
    out.speech_output = bus_nlg.UnknownOriginBusstop(station_name, slots, appdef, user_profile)
    out.DisplaySpeechOutputOnCard()        
    return out.createOutput(slots)

def out_InvalidDestination(station, slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for Warning message "FavoriteMissing"
    # Parameters:
    #  'slots' : current slots (for debug output)
    #  'appdef': application data (for translating literals and canonicals)
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("W7")
    out = myask_alexaout.alexaout()
    out.card_title = "InvalidDestination"
    out.speech_output = bus_nlg.UnknownDestinationBusstop(station, slots, appdef, user_profile)
    out.DisplaySpeechOutputOnCard()        
    return out.createOutput(slots)

def out_InvalidFavorite(user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for Warning message "FavoriteMissing"
    # Parameters:
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("W8")
    out = myask_alexaout.alexaout()
    out.card_title = "InvalidFavorite"
    out.speech_output = bus_nlg.InvalidUserProfile(user_profile) 
    out.DisplaySpeechOutputOnCard()        
    return out.createOutput({})

def out_InvalidFavoriteConnection(slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for Warning message "FavoriteMissing"
    # Parameters:
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("W11")
    out = myask_alexaout.alexaout()
    out.card_title = "InvalidFavorite"
    out.speech_output = bus_nlg.InvalidUserProfile(user_profile) 
    out.DisplaySpeechOutputOnCard()        
    return out.createOutput(slots)

def out_AeagServerError(slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for Warning message "FavoriteMissing"
    # Parameters:
    #  'slots' : current slots (for debug output)
    #  'appdef': application data (for translating literals and canonicals)
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("W9")
    out = myask_alexaout.alexaout()
    out.card_title = "InvalidDestination"
    out.speech_output = bus_nlg.AeagServerError(slots, appdef, user_profile)
    out.DisplaySpeechOutputOnCard()        
    return out.createOutput(slots)   
    
def out_ImplementationError(errorstring, slots, appdef, user_profile):
    #--------------------------------------------------------------------------
    # Generate Alexa Output structure for a general error message
    # Parameters:
    #  'slots' : current slots (for debug output)
    #  'appdef': application data (for translating literals and canonicals)
    #  'user_profile' : user information  (for personalizing message)
    #--------------------------------------------------------------------------    
    myask_log.ReportDialogState("ERROR")
    out = myask_alexaout.alexaout()
    out.card_title = "General Error"
    out.speech_output = bus_nlg.GeneralError(errorstring, slots, appdef, user_profile)
    out.DisplaySpeechOutputOnCard()        
    return out.createOutput(slots)   
    
