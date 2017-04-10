from textblob import TextBlob
from textblob import Word
from textblob.wordnet import wordnet
import os
import time
from Voice.Alarm import setReminder
from Voice.Wikipedia import wikiSearch
from Voice.SpeechRecognition import listen
from Voice.GoogleTTS import speak
from Voice.BingSearch import bingSearch
from Voice.Youtube import playYouTube
from Voice.GoogleNewsParser import retrieveNews
from Voice.Alarm import setReminder

Category = [{"verbs": ["Search","Find","browse","open"],  "nouns":[]},
            {"verbs":["Scroll","up","down", "move"],    "nouns":["screen","scroll", "bar"]},
            {"verbs":["Type","Enter","write"],  "nouns":[]},
            {"verbs":["Play","hear","sing"],    "nouns":[]},
            {"verbs":["Read","speak","dictate","say", "tell"],  "nouns":["news","document, headlines"]},
            {"verbs":["Remind","set"],  "nouns":["alarm","reminder","time"]},
            {"verbs":["Send","forward","mail"], "nouns":["mail","document"]}]

LowConfidence = 0.1

def GetNoun(blob):
    noun = []
    for word, tag in blob.tags:
        if tag in ("NN", "NNS", "NNPS","NNP"):
            noun.append(word.lemmatize())
    #print(noun)
    return(noun)


def GetVerbs(blob):
    verb = []
    for word, tag in blob.tags:
        if tag in ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ" ):
            verb.append(word.lemmatize())
    #print(verb)
    return verb

#blob = TextBlob("send an email to rashika bhargava")
#GetVerbs(blob=blob)
#GetNoun(blob)

def SimilarityCheck(eachWord1,eachWord2):
    try:
        syns1 = wordnet.synsets(eachWord1)
        syns2 = wordnet.synsets(eachWord2)
        # print("Syns 1: ",eachWord1, syns1, )
        # print("Syns 2: ",eachWord2, syns2)
        w1 = wordnet.synset(syns1[0].name())
        w2 = wordnet.synset(syns2[0].name())
        result = w1.wup_similarity(w2)
        if result is None:
            return 0
        else:
            return result
    except:
        return 0

def TaskSelection(text):
    blob = TextBlob(text)
    verb = GetVerbs(blob)  # getting verbs in a list
    noun = GetNoun(blob)
    print(verb, noun)
    avgVerb_result = [0,0,0,0,0,0,0]
    avgNoun_result = [0,0,0,0,0,0,0]
    sim_result = [0,0,0,0,0,0,0]
    noun_result = [0,0,0,0,0,0,0]

    #print("Verbs: ")
    if len(verb) == 0:
        speak("Iris could not get you. Please speak correctly.")
        return
    else:
        count = 0
        for eachItem in Category:
            sim_result[count], noun_result[count] = SimilarityComparison(count, verb, noun)
            count += 1

        print(sim_result, noun_result)

        # print(sim_result, noun_result)
        indexVerbFirstMax = sim_result.index(max(sim_result))
        valueVerbFirst = sim_result[indexVerbFirstMax]
        sim_result[indexVerbFirstMax] = 0

        indexVerbSecondMax = sim_result.index(max(sim_result))
        valueVerbSecond = sim_result[indexVerbSecondMax]
        sim_result[indexVerbSecondMax] = 0

        # print(avgVerb_result, avgNoun_result)

        indexNounFirstMax = noun_result.index(max(noun_result))
        valueNounFirst = noun_result[indexNounFirstMax]
        noun_result[indexNounFirstMax] = 0

        indexNounSecondMax = noun_result.index(max(noun_result))
        valueNounSecond = noun_result[indexNounSecondMax]
        noun_result[indexNounSecondMax] = 0

        print("First Verb", indexVerbFirstMax, valueVerbFirst)
        print("Second Verb", indexVerbSecondMax, valueVerbSecond)
        print("First Noun", indexNounFirstMax, valueNounFirst)
        print("Second Noun", indexNounSecondMax, valueNounSecond)

        if valueVerbFirst - valueVerbSecond <= LowConfidence:
            learningFunc(verb, noun)
            '''switchTaskAtLowConfidence(indexVerbFirstMax)
            speak(" or ")
            switchTaskAtLowConfidence(indexVerbSecondMax)

            feedbackText, listenFlag = listen()
            if listenFlag != 1:
                sentenceBlob = TextBlob(feedbackText)
                flag = 0

                for eachItem in sentenceBlob.tags:
                    if "yes" == eachItem[0] or "Yes" == eachItem[0] or "yess" == eachItem[0]:
                        flag = 1
                        print("First one selected")
                        switchExecuteTask(indexVerbFirstMax, text)
                        break

#Feed Back Similarity Check

                if flag is 0:
                    feedbackVerb = GetVerbs(sentenceBlob)
                    feedbackNoun = GetNoun(sentenceBlob)

                    if len(feedbackVerb) != 0:
                        feedback_verb1_result, feedback_noun1_result = SimilarityComparison(indexVerbFirstMax, feedbackVerb, feedbackNoun)
                        feedback_verb2_result, feedback_noun2_result = SimilarityComparison(indexVerbSecondMax, feedbackVerb, feedbackNoun)

                        if feedback_verb1_result > feedback_verb2_result:
                            switchExecuteTask(indexVerbFirstMax, text)
                        else:
                            switchExecuteTask(indexVerbSecondMax, text)
                    else:
                        speak("Retry, and be specific!")
                        return'''
        else:
            switchExecuteTask(indexVerbFirstMax, text)

def learningFunc(verb, noun):
    speak("Learning mode enabled. Answer in yes or no.")
    for indexOfeachCategory in range(7):
        switchTaskAtLowConfidence(indexOfeachCategory)
        result_text, flag = listen()
        if flag is 1:
            speak("Learning mode disabled. I could not understand what you say.")
            return
        elif "yes" == result_text or "Yes" == result_text or "yess" == result_text:
            count = 0
            checkVerbFlag = False
            checkNounFlag = False
            for eachQueryVerb in verb:
                for eachItem in Category:
                    checkVerbFlag = checkVerbList(count, eachQueryVerb)
                    if checkVerbFlag is True:
                        break
                    count += 1
                if checkVerbFlag is False:
                    Category[count]["verbs"].append(eachQueryVerb)

            count = 0
            for eachQueryNoun in noun:
                for eachItem in Category:
                    checkNounFlag = checkNounFlag(count, eachQueryNoun)
                    if checkNounFlag is True:
                        break
                    count += 1
                if checkNounFlag is False:
                    Category[count]["nouns"].append(eachQueryNoun)
            break

        else: speak(" or ")

def checkVerbList(indexOfeachCategory, eachVerb):
    verbFlag = False
    if eachVerb in Category[indexOfeachCategory]["verbs"]:
        verbFlag = True
        Category[indexOfeachCategory]["verbs"].remove(eachVerb)

    return verbFlag

def checkNounList(indexOfeachCategory, eachNoun):
    nounFlag = False
    if eachNoun in Category[indexOfeachCategory]["nouns"]:
        nounFlag = True
        Category[indexOfeachCategory]["nouns"].remove(eachNoun)
    return nounFlag

def SimilarityComparison(indexOfCategory, verbs, nouns):
    verb_result = 0.0
    noun_result = 0.0
    Verb_Weightage = 1
    Noun_Weightage = 1
    for eachQueryVerb in verbs:
        for eachVerb in Category[indexOfCategory]["verbs"]:
            sim_word = SimilarityCheck(eachVerb, eachQueryVerb)
            if verb_result < sim_word: verb_result = sim_word * Verb_Weightage
        Verb_Weightage = Verb_Weightage * (60 / 100)

    for eachQueryNoun in nouns:
        for eachNoun in Category[indexOfCategory]["verbs"]:
            sim_word = SimilarityCheck(eachNoun, eachQueryNoun)
            if noun_result < sim_word: noun_result = sim_word * Noun_Weightage
        Noun_Weightage = Noun_Weightage * (60 / 100)

    return verb_result, noun_result


def switchExecuteTask(x, text):
    if x == 0: bingSearch(text)
    elif x == 1: speak("Scroll yet to be coded")
    elif x == 2: speak("Type yet to be coded")
    elif x == 3: playYouTube(text)
    elif x == 4: retrieveNews(text)
    elif x == 5: speak("Alarm yet to be coded")
    elif x == 6: speak("Email yet to be coded")
    else: speak("I am sorry I miscalculated something. Can you please speak again ?")


def switchTaskAtLowConfidence(x):
    if x == 0: speak("Do you want to search ?")
    elif x == 1: speak("Do you want to scroll ?")
    elif x == 2: speak("Do you want to type ?")
    elif x == 3: speak("Do you want to play song ?")
    elif x == 4: speak("Do you want me to read headlines ?")
    elif x == 5: speak("Do you want to set reminder ?")
    elif x == 6: speak("Do you want to send email ?")
    else: speak("I am sorry I miscalculated something. Can you please speak again ?")

#TaskSelection("I want to hear peacful music")


def Askwords(blob):
   # print(blob.words)
    for eachWord in blob.words:
        if eachWord == "Who" or eachWord == 'who' or blob.tags == 'NNP':
            wikiSearch(str(blob))
            break
    else:
        pass
        #Bing search


'''def Alarm(blob):
    for eachTag in blob.tags:
        if "CD" == eachTag[1]:
            dt = list(time.localtime())
            currenthour = dt[3]
            currentminute = dt[4]
            tobeSet = eachTag[0]
            value = int(tobeSet)
            if len(tobeSet) == 1 or len(tobeSet) == 2:
                if "am" == eachTag[0]:
                    setReminder(value , 0)
                elif "pm" == eachTag[0]:
                    value = value + 12
                    if value == 24:
                        setReminder(0, 0)
                    else:
                        setReminder(value + 12, 0)
                else:
                    if currenthour > value :
                        setReminder(value,0)
                    elif currenthour < value :
                        value = value + 12
                        if value == 24:
                            setReminder(0,0)
                        else:
                            setReminder(value ,0)
                    else:
                        print("Please specify the minutes too")
            elif len(tobeSet) == 3:

                hour = tobeSet[0]
                minutes = tobeSet[1] + tobeSet[2]

                if "am" == eachTag[0]:
                    setReminder(int(hour),int(minutes))

                elif "pm" == eachTag[0]:
                    setReminder(int(hour) + 12 , int(minutes))
                else:
                    if currenthour > int(hour):
                        setReminder(int(hour), int(minutes))
                    elif currenthour < int(hour):
                        newHour = int(hour) + 12
                        if newHour == 24:
                            setReminder(0, 0)
                        else:
                            setReminder(newHour,int(minutes))
                            print("alarm set")
                    else:
                        if currentminute > int(minutes):
                            setReminder(int(hour) +12,int(minutes))
                        elif currentminute < int(minutes):
                            setReminder(int(hour),int(minutes))
                        else:
                            print("Please specify am or pm")

            elif len(tobeSet) == 4:
                hour = tobeSet[0] + tobeSet[1]
                minutes = tobeSet[2] + tobeSet[3]
                if "am" == eachTag[0]:
                    if hour == '12':
                        setReminder(0,int(minutes))
                    elif int(hour) < 12:
                        setReminder(int(hour),int(minutes))
                    else:
                        print("Please give correct time")
                elif "pm" == eachTag[0]:
                    convertedhour = int(hour) + 12
                    if convertedhour == 24:
                        setReminder(0,int(minutes))
                    else:
                        setReminder(convertedhour , int(minutes))
                else:
                    if currenthour > int(hour):
                        setReminder(int(hour), int(minutes))
                    elif currenthour < int(hour):
                        newHour = int(hour) + 12
                        if newHour == 24:
                            setReminder(0, 0)
                        else:
                            setReminder(newHour,int(minutes))
                            print("alarm set")
                    else:
                        if currentminute > int(minutes):
                            setReminder(int(hour) +12,int(minutes))
                        elif currentminute < int(minutes):
                            setReminder(int(hour),int(minutes))
                        else:
                            print("Please specify am or pm")

            else:
                print("Only hours and minutes required")





#Alarm(blob)
#listen()'''





#syns = wordnet.synsets("program")
#print(syns[0].lemmas()[0].name())#just the word
#print(syns[0].name()) #synset
#print(syns[0].definition())# meaning
