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
import asyncio
import threading
import pyautogui as pa

Category = [{"verbs": ["Search","Find","browse","open"],  "nouns":[]},
            {"verbs":["Scroll","up","down", "move"],    "nouns":["screen","scroll", "bar"]},
            {"verbs":["Type","Enter","write"],  "nouns":[]},
            {"verbs":["Play","hear","sing"],    "nouns":[]},
            {"verbs":["Read","speak","dictate","say", "tell"],  "nouns":["news","document, headlines"]},
            {"verbs":["Remind","set"],  "nouns":["alarm","reminder","time"]},
            {"verbs":["Send","forward","mail"], "nouns":["mail","document"]}]

Number = {'one' : 1,'two' : 2,'three': 3,'four' : 4,'five' : 5,'six' : 6, 'seven' : 7,'eight' : 8,'nine' : 9,'ten' : 10,
          'eleven': 11,'twelve': 12,'thirteen': 13,'fourteen': 14,'fifteen' : 15,'sixteen': 16, 'seventeen': 17,'eighteen': 18,'nineteen': 19,'twenty': 20,
          'twenty-one' : 21,'twenty-two' : 22,'twenty-three': 23,'twenty-four' : 24,'twenty-five' : 25,'twenty-six' : 26, 'twenty-seven' : 27,'twenty-eight' : 28,'twenty-nine' : 29,'thirty' : 30,
          'thirty-one' : 31,'thirty-two' : 32,'thirty-three': 33,'thirty-four' : 34,'thirty-five' : 35,'thirty-six' : 36, 'thirty-seven' : 37,'thirty-eight' : 38,'thirty-nine' : 39,'forty' : 40,
          'forty-one' : 41,'forty-two' : 42,'forty-three': 43,'forty-four' : 44,'forty-five' : 45,'forty-six' : 46, 'forty-seven' : 47,'forty-eight' : 48,'forty-nine' : 49,'fifty' : 50,
          'fifty-one' : 51,'fifty-two' : 52,'fifty-three': 53,'fifty-four' : 54,'fifty-five' : 55,'fifty-six' : 56, 'fifty-seven' : 57,'fifty-eight' : 58,'fifty-nine' : 59,'sixty' : 60}


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
    if x == 0: Search(TextBlob(text))
    elif x == 1: pa.screenshot("VA_Screenshot.png")
    elif x == 2: TypeInformation(TextBlob(text))
    elif x == 3: playYouTube(text)
    elif x == 4: News(TextBlob(text))
    elif x == 5: alarm(TextBlob(text))
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
#line_recognized = "type some data for me"
#blob = TextBlob(line_recognized)


    #under construction------------------------------->
def Alarm(blob):
    print(blob.tags)
    for eachWord in blob.words:
        if eachWord in Number:
            blob.words = [w.replace(eachWord,str(Number[eachWord])) for w in blob.words] #listcomprehensions
            #print(blob.words)
        else:
            continue
    new_sentence = ' '.join(blob.words)
    blob = TextBlob(new_sentence)
    print(blob.tags)
    count = 0
    time_nums = []
    for eachTag in blob.tags:
        if "am" == eachTag[0] or "A.M" == eachTag[0]:
            for eachTag in blob.tags:
                if "CD" == eachTag[1]:
                    time_nums.append(eachTag[0])
                    count+=1
            print(time_nums)
            print(count)
            if count == 1:
                if ':' in time_nums[0]:
                    hours, minutes = map(int, time_nums[0].split(':'))
                    if hours<13 and minutes<60:
                        if hours == 12:
                            setReminder(00,minutes,"Alarm set")
                            break
                        else:
                            setReminder(hours,minutes,"Alarm set")
                            break
                    break
                else:
                    hours = int(time_nums[0])
                    if hours == 12:
                        setReminder(00,00,"Alarm set")
                        break
                    else:
                        print("alarm set for", hours)
                        setReminder(hours,00,"Alarm set")
                        break

            elif count == 2:
                hours = int(time_nums[0])
                minutes = int(time_nums[1])
                if (hours == 12):
                    setReminder(00,minutes, "Alarm set")
                    break
                else:
                    setReminder(hours,minutes,"Alarm set")
                    break
            else:#when count comes out to be more than two
                print("Time was not specified correctly. Specfiy the time again")
                #listen()
        elif "pm" == eachTag[0] or "P.M" == eachTag[0]:
            for eachTag in blob.tags:
                if "CD" == eachTag[1]:
                    time_nums.append(eachTag[0])
                    count+=1
            print(time_nums)
            print(count)
            if count == 1:
                if ':' in time_nums[0]:
                    hours, minutes = map(int, time_nums[0].split(':'))
                    if hours >= 12 and hours < 24 and minutes <= 60:
                        setReminder(hours,minutes,"Alarm set")
                        break
                    elif hours<12 and minutes <= 60:
                        setReminder(hours + 12,minutes,"Alarm set")
                        break
                    else:
                        print("Please specify a correct time")
            elif count == 2:
                hours = int(time_nums[0])
                minutes = int(time_nums[1])
                if hours >= 12 and hours < 24 and minutes <= 60:
                    setReminder(hours, minutes, "Alarm set")
                    break
                elif hours < 12 and minutes <= 60:
                    setReminder(hours + 12, minutes, "Alarm set")
                    break
                else:
                    print("Please specify a correct time")
        else:
            for eachTag in blob.tags:
                if "CD" == eachTag[1]:
                    time_nums.append(eachTag[0])
                    count += 1
                print(time_nums)
                print(count)
                dt = list(time.localtime())
                current_hour = dt[3]
                current_minute = dt[4]
                if count == 1:
                    hour = int(time_nums[0])
                    if hour < 23 and hour >=1 and isinstance( hour, int ):
                       if current_hour>12 and current_hour <= 23:
                           newHour = hour + 12
                           if newHour > hour:
                               print("in block one")
                               setReminder(newHour,00,"set alarm")
                               break
                           else:
                               setReminder(hour,00,"set Alarm")
                               break
                       elif current_hour<=12:
                           if(hour <= 12):
                               if(hour<=current_hour):
                                   hour = hour + 12
                                   if(hour == 24):
                                        setReminder(00,00,"set Alarm")
                                        break
                                   else:
                                       setReminder(hour,00,"set Alarm")
                                       break

                               else:
                                   setReminder(hour,00,"setAlarm")
                                   break
                           else:
                                setReminder(hour,00,"setAlarm")
                                break
                    else:
                       print("Please enter the correct time")
                elif count == 2:
                    hour = int(time_nums[0])
                    minutes = int(time_nums[1])
                    if hour < 23 and hour >= 1 and isinstance(hour, int) and minutes < 60:
                        if current_hour > 12 and current_hour <= 23:
                            newHour = hour + 12
                            if newHour > hour:
                                setReminder(newHour, minutes, "set alarm")
                                break
                            elif newHour == current_hour:
                                if current_minute < minutes:
                                    setReminder(newHour,minutes,"set alarm")
                                    break
                                elif current_minute > minutes:
                                    setReminder(hour,minutes,"set alarm")
                                    break
                                else:
                                    print("Time elapsed already . please change the time")

                        elif current_hour <= 12:
                            if (hour <= 12):
                                if hour < current_hour:
                                    hour = hour + 12
                                    if (hour == 24):
                                        setReminder(00, minutes, "set Alarm")
                                        break
                                    else:
                                        setReminder(hour,minutes, "set Alarm")
                                        break

                                elif hour > current_hour:
                                    setReminder(hour,minutes, "setAlarm")
                                    break
                                else:
                                    if(current_minute < minutes):
                                        setReminder(hour,minutes,"set alarm")
                                        break
                                    elif(current_minute > minutes):
                                        setReminder(hour+12,minutes,"set alarm")
                                        break
                            else:
                                setReminder(hour,minutes, "setAlarm")
                                break
                    else:
                        print("Please enter the correct time")
                else:
                    print("hours and minutes not recognized")


def Search(blob):
    index_list = []
    count = 0
    for item in blob.words:
        if item == "find" or item == "search" or item == "open" or item == "browse":
            index_list.append(blob.words.index(item))
            count += 1
    print(index_list)
    if count == 0:
        for eachWord in blob.words:
            if eachWord == "Who" or eachWord == 'who' or blob.tags == 'NNP' or eachWord == "what" or eachWord == "how":
                bingSearch(blob.sentences)
    else:
        if index_list[0] == 0:
            index_list[0] = index_list[0] + 1
            bingSearch(' '.join(blob.words[index_list[0]:]))

        else:
            index_list[0]= index_list[0] + 1
            bingSearch(' '.join(blob.words[index_list[0]:]))

def alarm(blob):
    time_list = []
    locale_str = ""
    for eachTag in blob.tags:
        if eachTag[1] == "CD":
            time_list.append(eachTag[0])
        elif eachTag[0] == "am" or eachTag[0] == "A.M" or eachTag[0] == "pm" or eachTag[0] == "P.M":
            locale_str = eachTag[0]

    minutes_str = ""
    hours_str = ""
    count = 0
    hour = 0
    minute = 0
    colanFlag = False
    for eachTime in time_list:
        for eachChar in eachTime:
            if eachChar != ":" and colanFlag is False:
                hours_str += eachChar
            elif eachChar == ":":
                colanFlag = True
                continue
            if colanFlag is True and count == 0:
                minutes_str += eachChar

        if colanFlag is False and count == 0:
            hour = int(eachTime)
        elif colanFlag is True and count == 0:
            hour = int(hours_str)
            minute = int(minutes_str)

        elif count > 0:
            minute += int(eachTime)
        count += 1

    print(hour, minute, locale_str)

    if locale_str == "":
        dt = list(time.localtime())
        curr_hour = dt[3]
        curr_min = dt[4]

        if hour < 24 and hour >= 1 and curr_hour > 12 and curr_hour <= 23 and minute < 60:
                newHour = hour + 12
                if newHour > hour:
                    setReminder(newHour, minute, "set alarm")
                else:
                    setReminder(hour, minute, "set Alarm")

        elif hour < 24 and hour >= 1 and curr_hour < 13 and curr_hour >= 0 and minute < 60:
            if hour <= 12 and hour < curr_hour:
                hour = hour + 12
                if hour == 24:
                    setReminder(00 ,minute,"set alarm")
                else:
                    setReminder(hour,minute,"set alarm")
            elif hour <= 12 and hour > curr_hour:
                setReminder(hour,minute,"set alarm")
            elif hour <= 12 and hour == curr_hour:
                if curr_min < minute:
                    setReminder(hour,minute,"set alarm")
                else:
                    hour = hour + 12
                    if hour == 24:
                        setReminder(00,minute,"set alarm")
                    else:
                        setReminder(hour,minute,"set alarm")
            elif hour > 12 :
                setReminder(hour,minute,"set alarm")
            else:
                speak("please speak the correct time")

    elif locale_str == "pm" or "P.M" and minute < 60:
        if hour < 12 and hour > 0:
            setReminder(hour+12,minute,"set alarm")
        elif hour < 24 and hour > 11:
            setReminder(hour,minute,"set alarm")

    elif locale_str == "am" or "A.M" and minute < 60:
        if hour <= 12 and hour > 0:
            if hour == 12 :
                setReminder(00, minute,"set alarm")
            else:
                setReminder(hour,minute,"set alarm")
        else:
            speak("Time spoken in a wrong format")

#Search(blob)


#syns = wordnet.synsets("program")
#print(syns[0].lemmas()[0].name())#just the word
#print(syns[0].name()) #synset
#print(syns[0].definition())# meaning'''
#Alarm(blob)

     # error here code ok i will text blob wala problem solved

def News(blob):
    str = ' '.join(GetNoun(blob))
    retrieveNews(str)

def TypeInformation(loop, future):
            speak("Type mode on.")
            speak("Iris is now ready to enter the text.")
            asyncio.ensure_future(listen(future))
            future.add_done_callback(speech_recognition_complete_Type)
            thread = threading.Thread(target=speech_recognition_start_Type, args=(future, loop))
            thread.start()

def speech_recognition_start_Type(future, loop):
        try:
            loop.run_until_complete(future=future)
        except:
            print("Speech recognition failed to start")
            speak("Speech recognition failed to start")
            return

def speech_recognition_complete_Type(future):
    text = future.result()
    pa.typewrite(text, interval=0.25)
    print(text)
    future.done()


if __name__ == '__main__':
    TypeInformation()
