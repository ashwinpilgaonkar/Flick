import codecs
import json

from Voice import gnp
import threading
from Voice.GoogleTTS import speak
def retrieveNews(query):
    try:
        news = gnp.get_google_news_query(query)
    #for i in news["stories"]:
    #    for key, value in i.items():
    #        result = { key: value }

        title = news["stories"][0]["title"].decode("utf-8")
        source = news["stories"][0]['source'].decode("utf-8")
        link = news["stories"][0]['link'].decode("utf-8")
        content = news["stories"][0]['content_snippet'].decode("utf-8")

        result =  content + ". " + "News was brought to you by " + source + ". " + ". That's all for the news."
    except:
        result = "Sorry I did not get any results!"
    #print(news["stories"][0])
    #print(title)
    #print(source)
    #print(link)
    #print(content)
    print(result)
    #print(news["stories"][0]["content"])
    t = threading.Thread(target=speak, args=(result,))
    t.start()
    return result

#retrieveNews("Narendra Modi")