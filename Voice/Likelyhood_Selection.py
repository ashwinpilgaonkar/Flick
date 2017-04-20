from textblob import TextBlob
from Voice.SelectTask import *
import numpy as np
import math
import json
import logging
import copy

Responses = {"search": ["who is donald trump", "what is cnc machine", "how to implement quicksort algorithm",
                         "can you search how to remove stop words", "what is the weather today"],
              "screenshot": ["screenshot"],
              "type": ["type this"],
              "youtube": ["I want to hear peaceful music", "play me a song starboy", "I want to watch a movie star wars"],
              "news": ["what is todays headlines", "tell me news about narendra modi", "what is the weather today"],
              "reminder": ["set an alarm at 8:30 pm", "remind me, I have a meeting at 8:00 pm"],
              "email": ["send an email to gmail"]
            }

# Questions = [ ["",""], ["",""], ["",""], ["",""], ["",""], ["",""], ["",""] ]

Match_Table = {
    "Interrogatives": [],#["who", "what", "how", "how", "", "what", "", "", "", "", "what", "", "", "", "", ""],
    "Verbs": [],#["", "", "implement", "implement", "search", "", "type", "  write", "hear", "play", "", "tell", "set",
              #"put", "remind", "send"],
    "Nouns": [],#["trump", "machine", "quicksort", "algorithm", "words", "weather", "", "", "", "starboy", "headline",
              #"narendra", "alarm", "alarm", "meeting", "email"],
    "Class": [],#["search", "search", "search", "search", "search", "search", "type", "type", "youtube", "youtube", "news",
              #"news", "reminder", "reminder", "email"]
}

total_Num_Class = 7
LowConfidence = 0.1
similarity_Threshold = 0.5


def pro_Class(key="search"):
    total_freq = 0
    class_freq = 0
    for eachClassName in Match_Table["Class"]:
        total_freq += 1
        if eachClassName == key:
            class_freq += 1
    return class_freq / total_freq


def cal_Each_Column_Pro(queryWord="", className="search", key="Verbs"):
    document_Frequency = 0
    total_Num_Doc = 0
    index = 0
    for eachClass in Match_Table["Class"] :
        if eachClass == className:
            total_Num_Doc += 1
            match_word = Match_Table[key][index]
            if queryWord == match_word:
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


def similarity_Matrix(big_Union, text, row, column):
    vec_list = np.zeros((row, column), dtype=np.float64)

    i = 0
    j = 0

    for eachQueryWord in text.split():
        for eachUnionWord in big_Union:
            if eachQueryWord == eachUnionWord:
                vec_list[i, j] = 1
            else:
                vec_list[i, j] = 0
            j += 1
        i += 1
        j = 0

    i = 0
    j = 0

    sim_vector = []
    for eachUnionWord in big_Union:
        max = 0
        for eachQueryWord in text.split():
            if vec_list[j, i] == 1:
                max = 1
                break
            else:
                similarity = SimilarityCheck(eachUnionWord, eachQueryWord)
                if similarity > similarity_Threshold:
                    vec_list[j, i] = similarity
                else:
                    vec_list[j, i] = 0

                if max <= vec_list[j, i]:
                    max = vec_list[j, i]

            j += 1

        sim_vector.append(max)
        i += 1
        j = 0

    return sim_vector


def match_Similarity_with_Resposes(className, queryText):
    bag_Of_Words = []
    for eachSentence in Responses[className]:
        for eachWord in eachSentence.split():
            bag_Of_Words.append(eachWord)

    big_Union = list(set().union(bag_Of_Words, queryText.split()))

    row = len(queryText.split())
    column = len(big_Union)

    s1 = similarity_Matrix(big_Union, queryText, row, column)
    row = len(bag_Of_Words)

    classResponseText = ""
    for eachWord in bag_Of_Words:
        classResponseText += eachWord
        classResponseText += " "

    s2 = similarity_Matrix(big_Union, classResponseText, row, column)

    dot_Product = np.dot(s1, s2)
    magnitude_S1 = math.sqrt(sum(i ** 2 for i in s1))
    magnitude_S2 = math.sqrt(sum(i ** 2 for i in s2))

    cosine_Sim = dot_Product / (magnitude_S1 * magnitude_S2)

    print("Cosine Similarity: ", cosine_Sim)
    return cosine_Sim


def remove_StopWords(text):
    StopWords = "a about above after again against all am an and any are aren't as at be because been before being below between both\
but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have\
haven't having he he'd he'll he's her here here's hers herself him himself his how's i i'd i'll i'm i've if in into isn't it it's\
its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours"

    blob = TextBlob(text)
    stripped_Sentence = ""
    for eachWord in blob.words:
        if eachWord in StopWords.split():
            #print("Stopword: ", eachWord)
            logging.info("Stopword found: ", eachWord)
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
    global Responses, Match_Table
    auto_append(Responses)

    try:
        with open('Responses.json', 'r') as inputFile:
            Responses = json.load(inputFile)
    except:
        print("Responses.json file not found")

    try:
        with open('Match_Table.json', 'r') as inputFile:
            Match_Table = json.load(inputFile)
    except:
        print("Match Table.json file not found")

    blob = remove_StopWords(text.lower())
    verbs = GetVerbs(blob)
    nouns = GetNoun(blob)
    interrogatives = GetInterrogatives(blob)

    selection_list = [0, 0, 0, 0, 0, 0, 0]

    selection_list[0] = cal_total_Pro(interrogatives, verbs, nouns, "search")
    selection_list[1] = cal_total_Pro(interrogatives, verbs, nouns, "screenshot")
    selection_list[2] = cal_total_Pro(interrogatives, verbs, nouns, "type")
    selection_list[3] = cal_total_Pro(interrogatives, verbs, nouns, "youtube")
    selection_list[4] = cal_total_Pro(interrogatives, verbs, nouns, "news")
    selection_list[5] = cal_total_Pro(interrogatives, verbs, nouns, "reminder")
    selection_list[6] = cal_total_Pro(interrogatives, verbs, nouns, "email")

    Objects = []
    for i in list(range(7)):
        object = Rank()
        object.probability = max(selection_list)
        object.index = selection_list.index(object.probability)
        Objects.append(object)
        selection_list.insert(object.index, 0)
        print("Rank ", i + 1, object.index, object.probability)

    max_Similarity_Index = 0
    checkFlag = False

    for i in list(range(6)):
        try:
            if Objects[i].probability == Objects[i + 1].probability or Objects[i].probability - Objects[
                        i + 1].probability <= 0.1:
                checkFlag = True
                similarity1 = match_Similarity_with_Resposes(ClassName[Objects[i].index], text)
                similarity2 = match_Similarity_with_Resposes(ClassName[Objects[i + 1].index], text)

                if max_Similarity_Index < similarity1:
                    max_Similarity_Index = Objects[i].index

                if max_Similarity_Index < similarity2:
                    max_Similarity_Index = Objects[i + 1].index

            else:
                break
        except:
            pass

    if checkFlag == True:
        append_In_MatchTable(blob, ClassName[max_Similarity_Index], text)
        thread = threading.Thread(target=switchExecuteTask, args=(max_Similarity_Index,text))
        thread.start()
    else:
        thread = threading.Thread(target=switchExecuteTask, args=(Objects[0].index,text))
        thread.start()
    try:
        with open('Responses.json', 'w') as outfile:
            json.dump(Responses, outfile)
    except:
        print("Could not write Response.json")
    try:
        with open('Match_Table.json', 'w') as outfile:
            json.dump(Match_Table, outfile)
    except:
        print("Could not write Match_Table.json")

    if checkFlag == True:
        return max_Similarity_Index, selection_list[max_Similarity_Index]
    else:
        return Objects[0].index, selection_list[Objects[0].index]


def append_In_MatchTable(blob, className, text):
    nouns = GetNoun(blob)
    verbs = GetVerbs(blob)
    interrogatives = GetInterrogatives(blob)

    lengths = []
    lengths.append(len(nouns))
    lengths.append(len(verbs))
    lengths.append(len(interrogatives))

    try:
        last_Index = Match_Table["Interrogatives"].index(Match_Table["Interrogatives"][-1]) + 1
    except:
        last_Index = 0

    max_Length = max(lengths)

    for i in list(range(max_Length)):
        try:
            if interrogatives[i] in Match_Table["Interrogatives"] and className in Match_Table["Class"]:
                Match_Table["Interrogatives"].insert(last_Index," ")
            else:
                Match_Table["Interrogatives"].insert(last_Index,interrogatives[i])
        except:
            Match_Table["Interrogatives"].insert(last_Index," ")

        try:
            if verbs[i] in Match_Table["Verbs"] and className in Match_Table["Class"]:
                Match_Table["Verbs"].insert(last_Index," ")
            else:
                Match_Table["Verbs"].insert(last_Index,verbs[i])
        except:
            Match_Table["Verbs"].insert(last_Index," ")

        try:
            if nouns[i] in Match_Table["Nouns"] and className in Match_Table["Class"]:
                Match_Table["Nouns"].insert(last_Index," ")
            else:
                Match_Table["Nouns"].insert(last_Index,nouns[i])
        except:
            Match_Table["Nouns"].insert(last_Index," ")


        Match_Table["Class"].insert(last_Index,className)

        if Match_Table["Interrogatives"][i] == " " and Match_Table["Verbs"][i] == " "  and Match_Table["Nouns"][i] == " ":
            Match_Table["Interrogatives"].remove(Match_Table["Interrogatives"][i])
            Match_Table["Verbs"].remove(Match_Table["Verbs"][i])
            Match_Table["Nouns"].remove(Match_Table["Nouns"][i])
            Match_Table["Class"].remove(Match_Table["Class"][i])

        #print(len(Match_Table["Interrogatives"]), len(Match_Table["Verbs"]), len(Match_Table["Nouns"]),len(Match_Table["Class"]))

    if text in Responses[className]:
        logging.info("Response found")
    else:
        Responses[className].append(text)

    if len(Match_Table["Interrogatives"]) != len(Match_Table["Verbs"]) and len(Match_Table["Verbs"]) != len(Match_Table["Nouns"]) and len(Match_Table["Nouns"]) != len(Match_Table["Class"]):
        logging.debug("Sync failed!")
    #print(Match_Table["Interrogatives"], Match_Table["Verbs"], Match_Table["Nouns"], Match_Table["Class"])


def auto_append(Responses):
    for i in list(range(7)):
        for eachText in Responses[ClassName[i]]:
            append_In_MatchTable(blob=remove_StopWords(eachText), className=ClassName[i], text=eachText)

ClassName = {
    0: "search",
    1: "screenshot",
    2: "type",
    3: "youtube",
    4: "news",
    5: "reminder",
    6: "email"
}


class Rank:
    index = 0
    probability = 0


def main():
    bernoulli_Selection("what is the weather today")
    # Automate Responses

if __name__ == '__main__':
    main()