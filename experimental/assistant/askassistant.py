from .dialogTRY import detect_intent_stream, speak
from .recordAudio import record
from google.api_core.exceptions import InvalidArgument
import random
import string
N=10
filename = "nuovo_audio.wav"
#degug purposess
painting = "painting.wav"
identity = "identity.wav"
vase = "vase.wav"
# fine debug variables

DIALOGFLOW_LANGUAGE_CODE = 'en-US'
DIALOGFLOW_PROJECT_ID = 'chatcv'
SESSION_ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
TRY_PHRASE = 'PAINTING'
WELCOME_STRING = "Hi, How can I help you?"

def welcomeFrase():
    speak(WELCOME_STRING)


def ask():
    try:


        record()
        final = detect_intent_stream(DIALOGFLOW_PROJECT_ID, SESSION_ID, filename, DIALOGFLOW_LANGUAGE_CODE)
        print(final)
        if final == "-1":
            speak('I did not hear you, try again')
        else:
            speak('Remember to hold your red target, here we go ! Good choice \n ')
        return final
    except InvalidArgument:
        raise
        return str("error")

def speakA(text):
    speak(text)