import speech_recognition as sr
import pyttsx3



def text_to_speech(command):

    engine =  pyttsx3.init()
    engine.setProperty('rate', 200)
    engine.say(command)
    engine.runAndWait()

    del engine


def speech_to_text(duration):
    
    r = sr.Recognizer()

    with sr.Microphone() as source:

        r.adjust_for_ambient_noise(source, duration=0.2)
        text_to_speech("speak")
        audio = r.listen(source, phrase_time_limit=duration)

    try:
        text = r.recognize_google(audio, language="en-IN")
        
    except:
        text = 'n'

    return text.lower()



