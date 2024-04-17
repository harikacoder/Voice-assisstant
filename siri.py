import pyttsx3 as py
import speech_recognition as sr
import pywhatkit
import randfacts
import requests
import datetime

engine = py.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 140)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()
def wishme():
  hour=int(datetime.datetime.now().hour)
  if hour>8 and hour<12:
      return("good morning")
  elif hour>=12 and hour<16 :
      return("good afternoon")
  else:
      return("good evening")


today_date = datetime.datetime.now()
r = sr.Recognizer()


def joke():
    url = 'https://official-joke-api.appspot.com/random_joke'
    json_data = requests.get(url).json()
    setup = json_data["setup"]
    punchline = json_data["punchline"]
    return setup, punchline

def weather():
    api_address = 'https://api.openweathermap.org/data/2.5/weather?q=Vishakhapatnam&appid=33b2b85b934773c225dfde666c9ed0b7'
    json_data = requests.get(api_address).json()
    temperature = round(json_data["main"]["temp"] - 273.15, 1)  
    description = json_data["weather"][0]["description"]
    return temperature, description

speak("Hello, " +wishme()+ ", I am your voice assistant.") 
temperature, description = weather()
speak(f"The current temperature in Vishakhapatnam is {temperature} degrees Celsius, with {description}.")
today_date = datetime.datetime.now()
hour_minute = today_date.strftime("%I:%M %p")  # Modified format string to include minutes and AM/PM
speak(f"Today is {today_date.strftime('%d')} of {today_date.strftime('%b')}. And it's currently {hour_minute}. {today_date.strftime('%a')}.")
speak("How are you doing?")

with sr.Microphone() as source:
    r.energy_threshold = 10000
    r.adjust_for_ambient_noise(source, 1.2)
    print("Listening to you")
    speech = r.listen(source)
    text = r.recognize_google(speech)
    print(text)

    if all(x in text.lower() for x in ["what", "about", "you"]):
        speak("I am doing well too.")
 
speak("How can I help you?")

with sr.Microphone() as source:
    r.energy_threshold = 10000
    r.adjust_for_ambient_noise(source, 1.2)
    print("Listening to you")
    speech = r.listen(source)
    text1 = r.recognize_google(speech)
    print(text1)

    if "information" in text1.lower():
        speak("You want information related to which topic?")
        speech = r.listen(source)
        text2 = r.recognize_google(speech)
        print(text2)
        speak(f"Searching {text2} on Google")
        pywhatkit.search(text2)
    elif "search" in text1.lower():
        speak("What do you want me to search for?")
        speech = r.listen(source)
        search_query = r.recognize_google(speech)
        print(f"Search query: {search_query}")
        speak(f"Searching {search_query} on Google")
        pywhatkit.search(search_query)
    elif all(keyword in text1.lower() for keyword in ["play", "video"]):
        speak("You want me to play which video?")
        speech = r.listen(source)
        video_query = r.recognize_google(speech)
        video_query = video_query.lower().replace("play video", "").strip()
        print(f"Video query: {video_query}")
        speak(f"Playing video {video_query} on YouTube.")
        try:
            pywhatkit.playonyt(video_query)
        except Exception as e:
            print(f"Error occurred: {e}")
            speak("Sorry, there was an error while playing the video.")
    elif "fact" in text1.lower() or "facts" in text1.lower():
        speak("Sure, here is a random fact.")
        x = randfacts.get_fact()
        print(x)
        speak("Did you know that " + x)
    elif "joke" in text1.lower() or "jokes" in text1.lower():
        speak("Sure, get ready for chuckles.")
        setup, punchline = joke()
        speak(setup)
        print(setup)
        speak(punchline)
        print(punchline)
