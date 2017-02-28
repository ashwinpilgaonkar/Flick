__author__ = 'priyanshubhatnagar'

from gtts import gTTS
import os

def speak(text):
    if text and text.strip():
        tts = gTTS(text=text, lang='en')
        print("Google converted audio successfully.")
    else:
        tts = gTTS(text="Sorry I do not get what you say!", lang='en')
    tts.save("IrisTemp.mp3")
    os.system("mpg321 IrisTemp.mp3")
