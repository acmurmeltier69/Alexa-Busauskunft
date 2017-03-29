# Alexa-Busauskunft
Alexa Skill für Busauskunft 

Der Skill wurde ursprünglich geschrieben für Nahverkehr im Raum Aachen, kann aber leicht für andere Städte angepasst werden.

Update (28.März 2017): Unverständlicherweise und ohne nähere Begründung hat die ASEAG die Verwendung ihrer frei zugänglichen URA API (http://ivu.aseag.de/interfaces/ura/instant_V1) untersagt. 
Ich bin jetzt auf der Suche nach alternativen ÖPNV APIs um den Skill zu testen.

## Requires
Der Skill benutzt die folgenden "externen" Pakete:
-  "requests" (zur Vereinfachung der Anfragen an die externe API) Siehe http://docs.python-requests.org/en/master/
-  "myask"    (ein Paar kleine Helferchen, die ich für meine Alexa Skills geschrieben habe) Siehe https://github.com/acmurmeltier69/myask.git
Diese Pakete müssen als Unterverzeichnisse eingebunden werden, wenn der Handler als aws Lambda hochgeladen wird.


# Funktionalität
Dieser Skill bietet Live Abfahrts- und Verbindungsinformationen für den Nahverkehr z.B. für den Raum Aachen.

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

    Die bevorzugte Haltestelle für den Benutzer wird anhand der Amazon UserID in einer DynamoDB Datenbank abgelegt


# Datenmodell für Alexa
Die Informationen die das "Interaktionsmodell" des Alexa Skills benötigt liegen im Verzeichnis "ASK_resources"
- Intent structure --> aseak_intentstruct_generated.js
- definition of custom types --> aseak_customtypes_generated.txt
- Sample utterances --> sample_utterances_generated.txt

Die entsprechenden Dateien wurden mit Hilfe des [myask](https://github.com/acmurmeltier69/myask.git) Tools *myask/myask_appdef.py* automatisch aus einem internen Datenmodell generiert:

 - *'python/bus_appdef.py'* definiert die Intents, Slots und Custom-Slot-Types für den Skill
    - Die Liste der Bushaltestellen wird dabei aus "aseag_data.py" importiert
    - verschiedene Formulierungen ("literal values") für den selben Slot-Wert ("canonical value") werden im Datenmodell zusammengefasst.
      Die von Alexa erkannten slot-Werte werden bereits beim Einlesen (mit myask/myask_slots.py) in die entsprechenden canonicals umgewandelt.
      
 - *'ASK_resources/inputgrammar.txt'* definiert in kompakter form (als vereinfachte Variante einer [BNF-Grammatik](https://de.wikipedia.org/wiki/Backus-Naur-Form)) die möglichen Eingabesätze.
 
    Aus dieser kompakten Grammatik wird mit Hilfe des von *myask/myask_myask_utterancegen.py* eine Datei mit allen möglichen Formulierungen erzeugt, auf denen der Alexa Skill trainiert werden soll.

(Leider hat sich herausgestellt, dass ASK nur eine sehr begrenzte Zahl von "Sample Utterances" akzeptiert. Ich musste die alternativen Formulierungen (z.B. Verben) wieder reduzieren. )
