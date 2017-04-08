#Key 1:744c9117304442d7b6bcbf03d0603da9
#Key 2:db7b60c1b958496babf21fad95bfc4ab

from Voice.GoogleTTS import speak
import threading
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import webbrowser


def bingSearch(queryText):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '744c9117304442d7b6bcbf03d0603da9',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'q': queryText,
        'count': '10',
        'offset': '0',
        'mkt': 'en-us',
        'safesearch': 'Moderate',
    })

    try:
        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        dataInJson = json.loads(data)
        webURL = dataInJson['webPages']['value'][0]['displayUrl']
        contentSnippet = dataInJson['webPages']['value'][0]['snippet']
        print(contentSnippet, " .... ", webURL)

        t = threading.Thread(target=speak, args=(contentSnippet,))
        t.start()

        webbrowser.open_new_tab(webURL)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


#bingSearch("")