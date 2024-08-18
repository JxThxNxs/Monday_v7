import pyttsx3
import speech_recognition as sr
import webbrowser
import subprocess
import os
import difflib

# Ändern Sie das Arbeitsverzeichnis zum gewünschten Verzeichnis
os.chdir(r'C:\Users\jonas\TK PB')

# Initialize text-to-speech engine with a male German voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Adjust the index based on your preference

# Function to speak the given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech input
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Höre zu...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language="de-DE")
        print("Erkannt:", text)
        return text
    except sr.UnknownValueError:
        print("Konnte ich leider nicht verstehen.")
        return ""
    except sr.RequestError:
        print("Sorry, es gab ein Problem bei der Verbindung zum Spracherkennungsdienst.")
        return ""

# Function to put the PC into standby
def standby_pc():
    speak("Standby-Modus wird aktiviert.")
    subprocess.Popen('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')

# Function to find similar filenames
def find_similar_filename(filename, files):
    matches = difflib.get_close_matches(filename, files)
    if matches:
        return matches[0]
    else:
        return None

# Main loop
is_silent = False
while True:
    if not is_silent:
        speak("Erwarte Befehle")

    command = recognize_speech().lower()

    if "sei still" in command:
        is_silent = True
        continue

    if "rede weiter" in command:
        is_silent = False
        continue

    if is_silent:
        continue

    if "suche" in command:
        query = command.split(" ", 1)[1]
        url = "https://www.google.com/search?q=" + query
        webbrowser.open(url)
        speak("Hier sind die Suchergebnisse für " + query)

    elif "öffne" in command:
        app = command.split(" ", 1)[1]
        app = app.capitalize()  # Capitalize the first letter of the app name
        if not app.endswith(".py"):
            app += ".py"
        app = app.lower()  # Convert to lowercase
        try:
            subprocess.Popen(["python", app], creationflags=subprocess.CREATE_NEW_CONSOLE)
            speak(app + " wurde geöffnet.")
        except FileNotFoundError:
            # If the exact match is not found, try to find similar filenames
            python_files = [file for file in os.listdir() if file.endswith(".py")]
            similar_filename = find_similar_filename(app, python_files)
            if similar_filename:
                try:
                    subprocess.Popen(["python", similar_filename], creationflags=subprocess.CREATE_NEW_CONSOLE)
                    speak("Ein ähnliches Programm wurde geöffnet: " + similar_filename)
                except FileNotFoundError:
                    speak("Entschuldigung, ich konnte kein passendes Programm finden.")
            else:
                speak("Entschuldigung, ich konnte " + app + " nicht finden.")

    elif "beenden" in command:
        speak("Alles klar, Auf Wiedersehen")
        break

    elif "standby" in command:
        standby_pc()

    elif "Hallo" in command:
        speak("Hallo! Ich bin monday, dein persönlicher Assistent.")
