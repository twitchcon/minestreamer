import os
from flask import Flask, request
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SPEECH_API_KEY'] = os.getenv('SPEECH_API_KEY')
app.config['SERVICE_REGION_KEY'] = os.getenv('SERVICE_REGION_KEY')

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = app.config['SPEECH_API_KEY'], app.config['SERVICE_REGION_KEY']
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

print("Say something...")
key_phrase = "ok gamers"

# Starts speech recognition, and returns after a single utterance is recognized. The end of a
# single utterance is determined by listening for silence at the end or until a maximum of 15
# seconds of audio is processed.  The task returns the recognition text as result. 
# Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# shot recognition like command or query. 
# For long-running multi-utterance recognition, use start_continuous_recognition() instead.
result = speech_recognizer.recognize_once()

# Checks result.
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    if key_phrase in result.text.lower():
      print("Recognized: {}".format(result.text))
    else:
      print("You need to say ok gamers")
      print("This is what u said: {}".format(result.text.lower().replace(',', '')))
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("2 got called")
    print("No speech could be recognized: {}".format(result.no_match_details))
elif result.reason == speechsdk.ResultReason.Canceled:
    print("3 got called")
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))

@app.route('/')
def home():
  return "Hello, world!"

app.run(port=8080)
