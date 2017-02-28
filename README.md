# Alexa-Busauskunft
Alexa Skill für Buauskunfts  
Geschriebe nfür Nahverkehr im Raum Aachen (ASEAG), kann aber leicht für andere Städte angepasst werden.

Der Skill benutzt die ASEAG Unified realtime api (URA) (Base URL:  http://ivu.aseag.de/interfaces/ura/instant_V1)
Siehe z.B http://content.tfl.gov.uk/tfl-live-bus-river-bus-arrivals-api-documentation.pdf 

## Requires
Der Skill benutztz die folgenden "externen" Pakete:
-  "requests" (zur Vereinfachung der Anfragen an die ASEAG API) Siehe http://docs.python-requests.org/en/master/
-  "myask"    (ein Paar kleine Helferchen, die ich für meine Alexa Skills geschrieben habe) Siehe https://github.com/acmurmeltier69/myask.git
Diese Pakete müssen als Unterverzeichnisse eingebunden werden, wenn der Handler als aws Lambda hochgeladen wird.


# Funktionalität
Dieser Skill bietet Live Abfahrts- und Verbindungsinformationen für den Nahverkehr der ASEAG im Raum Aachen.

Sofern der Benutzer einmalig eine Haltestelle als bevorzugeten Abfahrtspunkt festgelegt hat, 
können Abfahrten und Verbindungen von dieser Haltestelle vereinfacht abgefragt werden. 

Unterstützte Kommandos (Intents):
 - **GetDeparturesFromFavorite** : Zeige Live-Abfahrtszeiten der Busse von der bevorzugten Haltestelle
 
Beispiele:
   
>  "Wann fährt der nächste Bus"

>  "Wann geht der nächste Bus der Line 47"

>  "Wann kommt der nächste Bus stadteinwärts"

 - **GetDeparturesFromOther** :  Zeige Live-Abfahrtszeiten ab einer anderen Haltestelle

Beispiele:
   
>  "Wann fährt der nächste Bus ab Richterich Rathaus"

>  "Zeige die Abfahrten die Linie 11 ab Elisenbrunnen"

 - **GetFavConnecionDepartures** : Suche Verbindungen von der bevorzugten Haltestelle zu anderen Zielen

Beispiele:
   
>  "Wann kommt der nächste Bus zum Hauptbahnhof"

>  "Wann geht ein Bus in die Liebigstraße"
     
- **FindConnectionFromOther** : Suche Verbindungen zwischen zwei beliebigen Haltestellen

Beispiele:

>  "Wann geht der nächste Bus vom Ponttor zum Hauptbahnhof"

>  "Wann geht ein Bus von Richterich rathaus in die Liebigstraße"
 
- **ChangeDefaultStation** : Ändere die bevorzugte Haltestelle für den Benutzer

Beispiel:
   
>  "Ändere die_bevorzugte_haltestelle zu Kohlscheid Markt"

    Die bevorzugte Haltestelle für den benutzer wird anhand der Amazon UserID in einer DynamoDB Datenbank abgelegt


# Datenmodell für Alexa
Die Informationen die das "Interaktionsmodell" des Alexa Skills benötigt liegen im Verzeichnis "ASK_resources"
- Intent structure --> aseak_intentstruct_generated.js
- definition of custom types --> aseak_customtypes_generated.txt
- Sample utterances --> sample_utterances_generated.txt

Die entsprechenden Dateien wurden mit Hilfe des [myask](https://github.com/acmurmeltier69/myask.git) Tools *myask/myask_appdef.py* automatisch aus einem internen Datenmodell generiert:

 - *'python/bus_appdef.py'* definiert die Intents, Slots und Custom-Slot-Types für den Skill
    - Die Liste der ASEAG Bushaltestellen wird dabei aus "aseag_data.py" importiert
    - verschiedene Formulierungen ("literal values") für den selben Slot-Wert ("canonical value") werden im Datenmodell zusammengefasst.
      Die von Alexa erkannten slot-Werte werden bereits beim Einlesen (mit myask/myask_slots.py) in die entsprechenden canonicals umgewandelt.
      
 - *'ASK_resources/inputgrammar.txt'* definiert in kompakter form (als vereinfachte Variante einer [BNF-Grammatik](https://de.wikipedia.org/wiki/Backus-Naur-Form)) die möglichen Eingabesätze.
 
    Aus dieser kompakten Grammatik wird mit Hilfe des von *myask/myask_myask_utterancegen.py* eine Datei mit allen möglichen Formulierungen erzeugt, auf denen der Alexa Skill trainiert werden soll.

(Leider hat sich herausgestellt, dass ASK nur eine sehr begrenzte Zahl von "Sample Utterances" akzeptiert. Ich musste die Alternativen Formuliereungen (z.B. Verben) wieder reduzieren. ) 
     
    