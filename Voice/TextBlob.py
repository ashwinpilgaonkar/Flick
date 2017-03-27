from textblob import TextBlob

wiki = TextBlob("")

print(wiki.tags)

print(wiki.noun_phrases)
