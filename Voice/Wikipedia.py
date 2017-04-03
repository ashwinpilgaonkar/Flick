import wikipedia
from Voice.GoogleTTS import speak
import threading

def wikiSearch(text):
    try:
        result = wikipedia.summary(text, sentences=1)
    except wikipedia.exceptions.PageError:
        result = "Sorry, I did not find anything on wikipedia!"
    print(result)
    t = threading.Thread(target=speak, args=(result,))
    t.start()
    return result

#print (wikipedia.summary("Wikipedia"))
# Wikipedia (/ˌwɪkɨˈpiːdiə/ or /ˌwɪkiˈpiːdiə/ WIK-i-PEE-dee-ə) is a collaboratively edited, multilingual, free Internet encyclopedia supported by the non-profit Wikimedia Foundation...

#print(wikipedia.search("Barack"))
# [u'Barak (given name)', u'Barack Obama', u'Barack (brandy)', u'Presidency of Barack Obama', u'Family of Barack Obama', u'First inauguration of Barack Obama', u'Barack Obama presidential campaign, 2008', u'Barack Obama, Sr.', u'Barack Obama citizenship conspiracy theories', u'Presidential transition of Barack Obama']

#ny = wikipedia.page("New York")
#ny.title
# u'New York'
#ny.url
# u'http://en.wikipedia.org/wiki/New_York'
#ny.content
# u'New York is a state in the Northeastern region of the United States. New York is the 27th-most exten'...
#ny.links[0]
# u'1790 United States Census'

#wikipedia.set_lang("fr")
#wikiSearch("Thomas edison")