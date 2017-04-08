import speech_recognition as sr
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    flag = 0
    try:
        text = r.recognize_google(audio, )#key="AIzaSyD8yDvpfQSnfWxjXiqGpNzlFYQLq-zOGO8",language="en-US",show_all=False)
        print("Google thinks you said: " + text)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        text = "Google Speech Recognition could not understand audio"
        flag = 1

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        text = "Could not request results from Google Speech Recognition service; {0}".format(e)
        flag = 1

    return text, flag

#listen()