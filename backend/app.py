from flask import Flask, request
import os

app = Flask(__name__)
app.config['SPEECH_API_KEY'] = os.getenv('SPEECH_API_KEY')

@app.route('/')
def home():
  return "Hello, world!"

app.run(port=8080, debug=True)
