from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime
import playsound
import os
import random
from gtts import gTTS
import contextlib
import speech_recognition as sr
from time import ctime
import time
import webbrowser
import os
from dotenv import load_dotenv, find_dotenv
import openai
import contextlib

r = sr.Recognizer()
load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPEN_AI_KEY')

# Set the model and prompt
model_engine = "text-davinci-003"

# Set the maximum number of tokens to generate in the response
max_tokens = 1024

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<string:page_name>')
def page_route(page_name):
    return render_template(page_name)


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


def listen_for_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            am_speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            am_speak('Sorry, I didn\'t get that.')
        except sr.RequestError:
            am_speak('Sorry, my speech service can\'t connect.')
        return voice_data


def say_hello_world():
    am_speak('hello world')
    return


def canned_response(voice_data):
    if 'what is your name' in voice_data:
        am_speak(f'My name is {__name__}')
    if 'what time is it' in voice_data:
        am_speak(ctime())
    if 'search the web' in voice_data:
        search = listen_for_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        am_speak(f'Here is what I found for: {search}')
    if 'find location' in voice_data:
        location = listen_for_audio('What is the location?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        am_speak(f'Here is what I found for: {location}')
    if 'goodbye' in voice_data:
        am_speak('It was good listening to you.')
        exit()
    if 'who rocks the party' in voice_data:
        am_speak('We rock the party, rock the party.')
    if 'what\'s the latest news' in voice_data:
        url = 'https://apnews.com/'
        webbrowser.get().open(url)
        am_speak('Here\'s the latest news right now.')
    else:
        # Generate a response
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=voice_data,
            max_tokens=max_tokens,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # Say response
        am_speak(completion.choices[0].text)


@app.route('/speak_computer')
def speak_computer():
    time.sleep(1)
    am_speak('Howdy! How can I help you?')
    while 1:
        voice_data = listen_for_audio()
        canned_response(voice_data)


@app.route('/stop_talking')
def stop_talking():
    am_speak('Sorry, I\'ll be quiet now.')
    exit()


def am_speak(audio):
    with contextlib.suppress(FileNotFoundError):
        # Delete previous audio files
        for file in os.listdir():
            if file.startswith('audio-') and file.endswith('.mp3'):
                os.remove(file)
    tts = gTTS(text=audio, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio)
    os.remove(audio_file)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
