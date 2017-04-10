from textblob import TextBlob
from Voice.SelectTask import *

Responses = {"search" : ["who is donald trump", "what is cnc machine", "how to implement quicksort algorithm", "can you search how to remove stop words", "what is the weather today"] ,
            "screenshot" : [] ,
            "type": ["can you type hello how are you"] ,
            "youtube" : ["I want to hear peaceful music", "play me a song starboy"] ,
            "news" : ["what is todays headlines", "tell me news about narendra modi"] ,
            "reminder" : ["set an alarm at 8:30 pm", "remind me, I have a meeting at 8:00 pm"] ,
            "email" : ["send an email to rashika bhargava"]
            }

Questions = [ ["",""], ["",""], ["",""], ["",""], ["",""], ["",""], ["",""] ]

Match_Table = {
                "Interrogatives" : ["who", "what",     "how",     "how",      ""    ,   "what"   ,    ""   ,  "" ,   ""  ,    ""   ,   "what"   ,       "" ,      "" ,     ""    ,    ""    ,   ""         ],
                "Verbs" :          [  "",   "",     "implement",  "implement", "search",     "" , "type","  write", "hear",  "play" ,    ""     ,     "tell" ,     "set" ,  "put" ,  "remind" ,  "send"    ],
                "Nouns" :          ["trump", "machine","quicksort","algorithm","words", "weather",  ""   ,   ""  ,   ""   , "starboy", "headline",   "narendra",  "alarm" , "alarm",  "meeting",  "email"  ],
                "Class" :          ["search", "search","search",   "search",   "search","search","type", "type" ,"youtube", "youtube",  "news"   ,     "news"   ,   "reminder" ,  "reminder",    "email"   ]
              }

total_Num_Class = 7



def ask_Question():
    return

def pro_Class(key="search"):
    total_freq = 0
    class_freq = 0
    for eachClassName in Match_Table["Class"]:
        total_freq += 1
        if eachClassName == key:
            class_freq += 1
    return class_freq / total_freq

def cal_Each_Column_Pro(queryWord = "", className="search", key="Verbs"):
    document_Frequency = 0
    total_Num_Doc = 0
    index = 0
    for eachClass in Match_Table["Class"]:
        if eachClass == className:

            total_Num_Doc += 1
            match_word = Match_Table[key][index]
            if queryWord == match_word or SimilarityCheck(queryWord, match_word) > 0.7:
                document_Frequency += 1

        index += 1

    return (document_Frequency + 1) / (total_Num_Doc + total_Num_Class)


def cal_total_Pro(queryInterrogatives=[], queryVerbs=[], queryNouns=[], className="search"):
    interrogatives_result = 1
    verbs_result = 1
    nouns_result = 1
    for eachQueryInterrogative in queryInterrogatives:
        interrogatives_result *= cal_Each_Column_Pro(eachQueryInterrogative, className, "Interrogatives")

    for eachQueryVerb in queryVerbs:
        verbs_result *= cal_Each_Column_Pro(eachQueryVerb, className, "Verbs")

    for eachQueryNoun in queryNouns:
        nouns_result *= cal_Each_Column_Pro(eachQueryNoun, className, "Nouns")

    return float(interrogatives_result) * float(verbs_result) * float(nouns_result) * float(pro_Class(className))

def similiarity_eachClass_Response(blob, classname="search"):
    nouns = GetNoun(blob)
    for noun in nouns:
        for eachSentences in Responses[classname]:
            #if
                if noun in GetNoun(eachSentences):
                    break

    return

def match_Similarity_with_Resposes(blob):
    interrogatives = GetInterrogatives(blob)
    if len(interrogatives) > 0:
        pass#similiarity_eachClass_Response(blob, "search")
    else:
        pass
    return

def remove_StopWords(text):
    StopWords = "a about above after again against all am an and any are aren't as at be because been before being below between both\
but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have\
haven't having he he'd he'll he's her here here's hers herself him himself his how's i i'd i'll i'm i've if in into isn't it it's\
its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours"

    blob = TextBlob(text)
    stripped_Sentence = ""
    for eachWord in blob.words:
        if eachWord in StopWords.split():
            print("Stopword: ", eachWord)
        else:
            stripped_Sentence = stripped_Sentence + " " + eachWord
    return TextBlob(stripped_Sentence)

def GetInterrogatives(blob):
    interrogatives = ["what", "when", "why", "which", "who", "how", "whose"]
    listOfInterrogatives = []
    for eachWord in blob.words:
        if eachWord in interrogatives:
            listOfInterrogatives.append(eachWord)

    return listOfInterrogatives

def bernoulli_Selection(text):
    blob = remove_StopWords(text.lower())
    verbs = GetVerbs(blob)
    nouns = GetNoun(blob)
    interrogatives = GetInterrogatives(blob)

    if len(verbs) is 0:
        verbs, nouns, interrogatives = match_Similarity_with_Resposes(blob)

    selection_list = [0,0,0,0,0,0,0]

    selection_list[0] = cal_total_Pro(interrogatives,verbs, nouns, "search")
    selection_list[1] = cal_total_Pro(interrogatives, verbs, nouns, "screenshot")
    selection_list[2] = cal_total_Pro(interrogatives, verbs, nouns, "type")
    selection_list[3] = cal_total_Pro(interrogatives, verbs, nouns, "youtube")
    selection_list[4] = cal_total_Pro(interrogatives, verbs, nouns, "news")
    selection_list[5] = cal_total_Pro(interrogatives, verbs, nouns, "reminder")
    selection_list[6] = cal_total_Pro(interrogatives, verbs, nouns, "email")

    print("Max Index: ", selection_list.index(max(selection_list)), "Probabilities: ", selection_list)

def main():
    bernoulli_Selection("I want to listen shape of you")


if __name__ == '__main__':
    main()