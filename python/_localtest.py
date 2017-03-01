# coding: utf-8

from myask import myask_log, myask_appdef, myask_localtest, myask_utterancegen
import bus_appdef
import bus_handler

CONST_TEST_BATCH      = 1
CONST_TEST_UTTERANCE  = 2
CONST_TEST_RANDOM     = 3
CONST_CREATE_ASK_SPEC = 4
CONST_CREATE_SAMPLES  = 5

NUM_RANDOM = 1
TESTINTENTS = ['*']
BASEDIR = "C:/Users/Andreas_Kellner/_MY_DATA/AlexaSkill/git/Alexa-Busauskunft/"
TEST_DIR = BASEDIR + "test_events/"
TESTFILE_BATCH = "TestList2.csv"
TESTFILE_SINGLE = "T2_zeige_abfahrten_ab_elisenbrunnen.js"

ASK_RESOURCEDIR = BASEDIR + "ask_resouces/"
ASK_GENERATION_GRAMMAR = "inputgrammar.txt"
ASK_SAMPLE_OUTPUT = "sample_utterances_generated.txt"

#TEST_TYPE = CONST_TEST_UTTERANCE
TEST_TYPE = CONST_TEST_BATCH
#TEST_TYPE = CONST_TEST_RANDOM
#TEST_TYPE = CONST_CREATE_ASK_SPEC
#TEST_TYPE = CONST_CREATE_SAMPLES



def main():     

    
    appdef = myask_appdef.applicationdef(bus_appdef.APPNAME, bus_appdef.APPID,
                                         bus_appdef.INTENTS, bus_appdef.SLOTS, 
                                         bus_appdef.SLOTTYPES)
    
    handlerfunction = bus_handler.lambda_handler

    myask_log.SetDebugLevel(99)
    if TEST_TYPE == CONST_TEST_UTTERANCE:
        filename = TEST_DIR + TESTFILE_SINGLE
        event = myask_localtest.ReadInputJSON(filename)
        myask_localtest.TestEvent(event, handlerfunction)

    elif TEST_TYPE == CONST_TEST_BATCH:
        filename = TEST_DIR + TESTFILE_BATCH
        myask_localtest.batchtest(filename, TEST_DIR, TESTINTENTS, handlerfunction)

    elif TEST_TYPE == CONST_TEST_RANDOM:
        myask_localtest.randomtest(NUM_RANDOM, TESTINTENTS, appdef, handlerfunction)

    elif TEST_TYPE == CONST_CREATE_ASK_SPEC:
        intent_json = appdef.CreateIntentDef()
        print("=======BEGIN INTENT DEF=====================================\n\n")
        print intent_json
        print("\n=======END INTENT DEF=====================================\n\n")
        typeinfo = appdef.GetAllSlotLiterals()
        for (slottype, slotliterals) in typeinfo:
            print("\n--- "+slottype+" ---")
            for literal in slotliterals:
                print literal
    elif TEST_TYPE == CONST_CREATE_SAMPLES:
        inputfile = ASK_RESOURCEDIR + ASK_GENERATION_GRAMMAR
        training_sentences = myask_utterancegen.createSampleUtterancesFromGrammar(inputfile)
        
        # print utterances to file
        outputfile = ASK_RESOURCEDIR + ASK_SAMPLE_OUTPUT
        fout = open(outputfile, 'w+')
        for i in range(len(training_sentences)):
            line = training_sentences[i]
            #        print "writing line "+str(i)+". --> '"+line+"'"
            fout.write(line+"\n")
        fout.close()


#-------------------------------------------------------------------------------
#  end of main() function 
#-------------------------------------------------------------------------------

if __name__ == "__main__": main()