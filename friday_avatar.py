import os
import subprocess
import random
import speech_recognition as sr
import webbrowser
from datetime import datetime, timedelta
import pyautogui
import requests
from bs4 import BeautifulSoup

def speak(text):
    voice = "en-US-AvaNeural"
    command = f'edge-tts --voice "{voice}" --text "{text}" --write-media "audio/output.mp3"'
    os.system(command)
    subprocess.run(["afplay", "audio/output.mp3"])  # Use afplay to play the audio on macOS

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognising...")
        query = r.recognize_google(audio, language='en-us')
    
    except Exception as e:
        print(e)
        return ""
    return query.lower()  # Convert the query to lowercase for easier comparison

def get_web_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()

sleep_mode = False 
previous_queries = []


# the knowledge bank
knowledge_bank = {} # will be filled with info until I can figure out how to either create an llm or integrate one wiithout any costs 


speak("Friday here!, your virtual assistant. What can I do for you?")

while True:
    query = take_command()
    print("You: " + query)
    
    if "hello" in query or "hi" in query or "yo" in query or "greetings" in query:
        responses = ["Hello! How are you today?", "Hey there! What's up?", "Hi! What can I do for you?"]
        speak(random.choice(responses))
    
    elif "how are you" in query:
        responses = ["I'm doing well, thank you!", "I'm here and ready to assist!", "Feeling great, thanks for asking!"]
        speak(random.choice(responses))

    elif any(word in query for word in ["sad", "not good", "unhappy"]):
        speak("I'm sorry to hear that. Is there anything I can do to help?")
    
    elif "hey friday" in query:
        responses = ["Yes? Is there anything you need?", "Mhm? What is it?", "Hey there! What can I assist you with?"]
        speak(random.choice(responses))

    # Add more diverse responses based on context
    elif "open" in query:
        responses = ["Sure thing!", "Opening it up for you!", "Here we go!"]
        speak(random.choice(responses))
        app_name = query.replace("open", "").strip()  # Remove "open" and any leading/trailing spaces
        try:
            # Use subprocess to open the application on macOS
            subprocess.run(["open", "-a", app_name])
        except Exception as e:
            print(e)
            speak(f"Sorry, I couldn't open {app_name}.")

    elif "close" in query:
        responses = ["Closing it down!", "Got it, shutting it!", "Closing up shop!"]
        speak(random.choice(responses))
        app_name = query.replace("close", "").strip()  # Remove "close" and any leading/trailing spaces
        try:
            # Use osascript to execute AppleScript to close the application
            os.system(f"osascript -e 'quit app \"{app_name}\"'")
        except Exception as e:
            print(e)
            speak(f"Sorry, I couldn't close {app_name}.")

    elif "play" in query:
        responses = ["Sure, playing that for you!", "Let's get some music going!", "Time for some tunes!"]
        speak(random.choice(responses))
        song_name = query.replace("play", "").strip()
        # Open YouTube URL for the song in the default web browser
        webbrowser.open(f"https://www.youtube.com/results?search_query={song_name}")
    
    elif "pause" in query:
        try:
            speak("Pausing now.")
            pyautogui.hotkey('k')
        except Exception as e:
            print(e)
            speak(f"Sorry couldn't pause it.")
    
    elif "resume" in query:
        try:
            speak("Resuming now")
            pyautogui.hotkey('k')
        except Exception as e:
            print(e)
            speak(f"Sorry couldn't pause it.")

    elif "time" in query:
        current_time = datetime.now().strftime("%I:%M %p")  # %I for 12-hour format
        responses = [f"The current time is {current_time}.", f"It's {current_time} now.", f"{current_time} at the moment."]
        speak(random.choice(responses))


    elif "what is" in query:
        query = query.replace("search", "").strip()
        speak("Searching the web for you.")
        # Perform a Google search and get the text content of the first search result
        search_url = f"https://www.google.com/search?q={query}"
        web_content = get_web_content(search_url)
        # Analyze the web content and generate a response
        # For simplicity, let's just speak the first 500 characters of the web content
        speak(web_content[:500])
    
    elif "set a reminder that" in query:
        rememberMessage = query.replace("remeber that", "")
        speak("you told me to remember that" + rememberMessage)
        remember = open("remember.txt", "a")
        remember.write(rememberMessage)
        remember.close()
    
    elif "tell me the reminder" in query:
        remember = open("remember.txt", "r")
        speak("you told me to remember" + remember.read())
    
    elif "clear reminders" in query:
        file = open("remember.txt", "w")
        file.write(f"")
        speak("all done all the reminders have been cleared. Anything else?")

    # Add more responses for interacting with tabs, setting timers, etc.
    elif "switch tab" in query:
        speak("Switching tabs now")
        pyautogui.hotkey('command', 'tab')  # Simulate Command + Tab key press to switch tabs

    elif "close tab" in query:
        speak("Closing the current tab")
        pyautogui.hotkey('command', 'w') # Command + w to close the current tab
    
    elif "swipe right" in query:
        speak("Swiping to the next window")
        pyautogui.hotkey('ctrl', 'right')
    
    elif "swipe left" in query:
        speak("Swipe to the previous window")
        pyautogui.hotkey('ctrl', 'left')
    
    elif "sleep" in query or "one second":
        speak("Ok, I am going to sleep now, you can call me anytime you need, just say wake up and I'll be there.")
        sleep_mode = True
    
    elif "goodbye" in query:
        speak("Ok, goodbye, see you next time. Have a good one!")
        break 

    else:
        speak("I'm not sure I understand. Can you repeat that?")

    while sleep_mode:
        query = take_command().lower()
        print(query)

        if "wake up" in query:
            speak("Oh hello, I am awake now, what's up?")
            sleep_mode = False 
        
        if "sorry where were we" in query:
            speak("Its alright no problem, I was going to ask if you needed anything.")
            sleep_mode = False 

        elif "hey friday" in query:
            responses = ["Yes, sorry, was a bit tired. what's up? What can I do for you?", 
                         "Hey there! Back in action. How can I assist?", 
                         "I'm up! What do you need?"]
            speak(random.choice(responses))
