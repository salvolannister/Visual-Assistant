import dialogflow_v2 as dialogflow
import json
from google.api_core.exceptions import InvalidArgument
from google.oauth2 import service_account
from .recordAudio import record
import random
import string
import pyttsx3
import engineio
import google.protobuf as pf

#you have to give credentials in order to let it work
dialogflow_key = json.load(open(r'./assistant/accountKey.json'))
credentials = (service_account.Credentials.from_service_account_info(dialogflow_key))

"""
N=10
filename = "nuovo_audio.wav"
#degug purposess
painting = "painting.wav"
identity = "identity.wav"
vase = "vase.wav"
final =""

DIALOGFLOW_LANGUAGE_CODE = 'en-US'
DIALOGFLOW_PROJECT_ID = 'chatcv'
SESSION_ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
TRY_PHRASE = 'PAINTING'
WELCOME_STRING = "Hi, How can I help you?"
"""
# parameters for voice
engineio = pyttsx3.init()
volume = engineio.getProperty('volume')
engineio.setProperty('volume', volume+0.50)
voices = engineio.getProperty('voices')
engineio.setProperty('rate', 130)    # Aquí puedes seleccionar la velocidad de la voz
engineio.setProperty('voice',voices[1].id)


def explicit():
    from google.cloud import storage

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        'accountKey.json')

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

def speak(text):
    engineio.say(text)
    engineio.runAndWait()

def detect_intent_stream(project_id, session_id, audio_file_path,
                         language_code):
    """Returns the result of detect intent with streaming audio as input.

    Using the same `session_id` between requests allows continuation
    of the conversaion."""

    session_client = dialogflow.SessionsClient(credentials=credentials)

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 16000

    session_path = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session_path))

    def request_generator(audio_config, audio_file_path):
        query_input = dialogflow.types.QueryInput(audio_config=audio_config)

        # The first request contains the configuration.
        yield dialogflow.types.StreamingDetectIntentRequest(
            session=session_path, query_input=query_input)

        # Here we are reading small chunks of audio data from a local
        # audio file.  In practice these chunks should come from
        # an audio input device.
        with open(audio_file_path, 'rb') as audio_file:
            while True:
                chunk = audio_file.read(4096)
                if not chunk:
                    break
                # The later requests contains audio data.
                yield dialogflow.types.StreamingDetectIntentRequest(
                    input_audio=chunk)

    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)

    requests = request_generator(audio_config, audio_file_path)
    responses = session_client.streaming_detect_intent(requests)

    print('=' * 20)
    for response in responses:
        print('Intermediate transcript: "{}".'.format(
                response.recognition_result.transcript))

    # Note: The result from the last response is the final transcript along
    # with the detected content.
    query_result = response.query_result
    if query_result.fulfillment_text is "":
        return str(-1)
    print('=' * 20)
    print('Query text: {}'.format(query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        query_result.intent.display_name,
        query_result.intent_detection_confidence))
    """print('Fulfillment text: {}\n'.format(
        query_result.fulfillment_text))"""
    print("IM HERE")
    result = pf.json_format.MessageToJson(response.query_result)
    result = json.loads(result)
    return str(result["fulfillmentText"])

def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient(credentials=credentials)

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))


    text_input = dialogflow.types.TextInput(
        text=texts, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))

    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))


"""
DEBUG USE 


if __name__ == "__main__":
    try:

         #speak("Hi, how can I help you?")
         #record()
        #detect_intent_texts(DIALOGFLOW_PROJECT_ID, SESSION_ID, TRY_PHRASE, DIALOGFLOW_LANGUAGE_CODE)
         final = detect_intent_stream(DIALOGFLOW_PROJECT_ID, SESSION_ID, filename,DIALOGFLOW_LANGUAGE_CODE)
         print(final)
         print("QUI")
    except InvalidArgument:
        raise
"""