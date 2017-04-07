from textblob import TextBlob
from textblob import Word
from Voice.Wikipedia import wikiSearch
from textblob.wordnet import wordnet
import os
from Voice.SpeechRecognition import listen
import time
from Voice.Alarm import setReminder
import math
from scipy import spatial


Category = [{"verbs": ["Search","Find","browse"],  "nouns":[]},
            {"verbs":["Scroll","up","down", "move"],    "nouns":["screen","scroll", "bar"]},
            {"verbs":["Type","Enter","write"],  "nouns":[]},
            {"verbs":["Play","hear","sing"],    "nouns":[]},
            {"verbs":["Read","speak","dictate","say"],  "nouns":["news","document"]},
            {"verbs":["Remind","set"],  "nouns":["alarm","reminder","time"]},
            {"verbs":["Send","forward","write","mail"], "nouns":["mail","document"]}]

def GetNoun(blob):
    noun = []
    for word, tag in blob.tags:
        if tag in ("NN", "NNS", "NNPS","NNP"):
            noun.append(word.lemmatize())
    return(noun)

def GetVerbs(blob):
    verb = []
    for word, tag in blob.tags:
        if tag in ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ" ):
            verb.append(word.lemmatize())
    return verb

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
    sim_result = [0,0,0,0,0,0,0]
    noun_result = [0,0,0,0,0,0,0]
    count = 0

    #print("Verbs: ")
    for eachQueryVerb in verb:
        count = 0
        for eachItem in Category:
            for eachVerb in eachItem["verbs"]:
                #print(count, eachQueryVerb, eachVerb)
                simWord = SimilarityCheck(eachQueryVerb, eachVerb)
                if sim_result[count] < simWord: sim_result[count] = simWord
                #sim_result[count] +=  SimilarityCheck(eachQueryVerb, eachVerb)
                #if len(eachItem["verbs"]) != 0: sim_result[count] /= len(eachItem["verbs"])
            count += 1

    #print("Nouns: ")
    for eachQueryNoun in noun:
        count = 0
        for eachItem in Category:
            for eachNoun in eachItem["nouns"]:
                #print(count, eachQueryNoun, eachNoun)
                simWord = SimilarityCheck(eachQueryNoun, eachNoun)
                if sim_result[count] < simWord: sim_result[count] = simWord
                #noun_result[count] +=  SimilarityCheck(eachQueryNoun, eachNoun)
            if len(eachItem["nouns"]) != 0: noun_result[count] /= len(eachItem["nouns"])
            count += 1

    print(sim_result, noun_result)

TaskSelection("Can you Search how to write quick sort algorithm")

'''
def TaskSelection(text):
    blob = TextBlob(text)
    verb = GetVerbs(blob) # getting verbs in a list
    noun = GetNoun(blob)

    result_similarity = [0,0,0,0,0,0,0] # a list to store the similarity check values
    noun_similarity = [0,0,0,0,0,0,0]
    count = 0

    for eachQueryVerb in verb:
        for itemCategory in Category:
            for eachVerb in itemCategory["verbs"]:
                result_similarity[count] += SimilarityCheck(eachVerb, eachQueryVerb)
                print(result_similarity[count], eachVerb, eachQueryVerb)
                #result_similarity[count] /= len(itemCategory["verbs"])
            count += 1

    count = 0

    for eachQueryNoun in noun:
        for itemCategory in Category:
            for eachNoun in itemCategory["nouns"]:
                noun_similarity[count] += SimilarityCheck(eachNoun, eachQueryNoun)
                print(result_similarity[count], eachNoun, eachQueryNoun)
                #noun_similarity[count] /= len(itemCategory["nouns"])
            count += 1

    for eachResultSim, eachNounSim in result_similarity, noun_similarity:
        eachResultSim += eachNounSim / 2

    #print(result_similarity)

TaskSelection("Set an alarm at 8")'''
    #print(similar_param)
    #print(similar_param.index(max(similar_param)))

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
