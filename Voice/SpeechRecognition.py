import speech_recognition as sr
async def listen(future):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, )#key="AIzaSyD8yDvpfQSnfWxjXiqGpNzlFYQLq-zOGO8",language="en-US",show_all=False)
        print("Google thinks you said: " + text)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        text = 1

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        text = 1
    except:
        text = 1

    future.set_result(text)

#listen()