import urllib.request
import urllib.parse
import re
import webbrowser

def playYouTube(text):
    query_string = urllib.parse.urlencode({"search_query" : text})
    html_content = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    url = "http://www.youtube.com/watch?v=" + search_results[0]
    print(url)
    webbrowser.open_new_tab(url)

playYouTube("trap city")