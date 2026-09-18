# ---------------------------
# Import necessary libraries
# ---------------------------
import speech_recognition as sr       # For capturing and recognizing voice input
import pyttsx3                       # For text-to-speech functionality
import wikipedia                     # To fetch summaries from Wikipedia
import datetime                      # To get current date and time
import webbrowser                    # To open websites in default browser
import pywhatkit                     # To perform YouTube, Google searches and send WhatsApp messages
import smtplib                       # To send emails via SMTP
from email.message import EmailMessage  # To format email messages
import os                            # To interact with operating system (files, directories)
import subprocess                    # To run system commands or open applications
import platform                       # To detect the current operating system
import requests                      # To make HTTP requests to APIs
import json                         # To parse JSON responses from APIs
import random                        # To choose random jokes or selections
import shutil                        # To detect installed apps dynamically on Windows

# ---------------------------
# Initialize text-to-speech engine
# ---------------------------
engine = pyttsx3.init()               # Initialize pyttsx3 engine
engine.setProperty('rate', 170)       # Set speaking rate (words per minute)

# ---------------------------
# Memory dictionary to store notes
# ---------------------------
memory = {}                           # Dictionary to store remembered notes

# ---------------------------
# Function to speak and print messages
# ---------------------------
def speak(text):
    print(f"[Assistant]: {text}")     # Print the text to terminal for debugging
    engine.say(text)                  # Speak the text aloud
    engine.runAndWait()               # Wait until speech is finished

# ---------------------------
# Function to listen to user's voice
# ---------------------------
def listen():
    r = sr.Recognizer()               # Initialize recognizer
    try:
        with sr.Microphone() as source:          # Use the microphone as source
            speak("Listening...")                # Prompt user
            r.adjust_for_ambient_noise(source, duration=1)  # Adjust for background noise
            audio = r.listen(source, timeout=5)  # Listen for 5 seconds
    except Exception as e:                       # Handle errors in microphone usage
        print(f"[Error]: Microphone issue - {e}")
        speak("Microphone is not working.")     # Speak error to user
        return ""                                # Return empty string on failure

    # Try to recognize speech using Google
    try:
        command = r.recognize_google(audio, language='en-IN')  # Recognize speech in Indian English
        print(f"[User]: {command}")                              # Print recognized text
        return command.lower()                                   # Return lowercase for consistency
    except sr.UnknownValueError:         # Handle unrecognized speech
        speak("Sorry, I did not understand.")
        return ""
    except sr.RequestError:              # Handle request errors (internet issues)
        speak("Internet connection error.")
        return ""
    except Exception as e:               # Catch all other exceptions
        print(f"[Error]: Recognition issue - {e}")
        return ""

# ---------------------------
# Function to send emails
# ---------------------------
def send_email(to_address, subject, content):
    try:
        sender_email = "your_email@gmail.com"       # Sender email (replace with yours)
        password = "your_app_password"              # App password (do not use normal password)
        msg = EmailMessage()                        # Create new email message
        msg['From'] = sender_email                  # Set sender
        msg['To'] = to_address                       # Set recipient
        msg['Subject'] = subject                     # Set email subject
        msg.set_content(content)                     # Set email body
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Connect to Gmail SMTP server
        server.starttls()                            # Start TLS encryption
        server.login(sender_email, password)         # Login with credentials
        server.send_message(msg)                     # Send the email
        server.quit()                                # Quit the server connection
        speak("Email has been sent successfully.")  # Confirm to user
        print(f"[Email]: Sent to {to_address} with subject '{subject}'")  # Log action
    except Exception as e:                           # Catch email sending errors
        print(f"[Error]: Email issue - {e}")
        speak("Sorry, I could not send the email.")

# ---------------------------
# Function to send WhatsApp messages
# ---------------------------
def send_whatsapp_message(phone_number, message, hour=None, minute=None):
    try:
        if hour is None or minute is None:          # If time not specified
            now = datetime.datetime.now()           # Get current time
            hour = now.hour                         # Current hour
            minute = now.minute + 2                 # Schedule 2 minutes later
        pywhatkit.sendwhatmsg(phone_number, message, hour, minute)  # Send WhatsApp message
        speak(f"WhatsApp message scheduled to {phone_number}")      # Confirm to user
        print(f"[WhatsApp]: Message to {phone_number}: {message}")   # Log action
    except Exception as e:
        print(f"[Error]: WhatsApp issue - {e}")     # Log error
        speak("Sorry, I could not send the WhatsApp message.")

# ---------------------------
# Function to open apps or files on laptop
# ---------------------------
def open_on_laptop(app_name):
    try:
        os_name = platform.system()                 # Detect OS
        if os_name == "Windows":
            # Predefined paths for some apps (Excel and PowerPoint use full paths)
            paths = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "chrome": "chrome.exe",
                "command prompt": "cmd.exe",
                "paint": "mspaint.exe",
                "excel": "C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
                "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
                "store": "store"   # Special handling below
            }
            if app_name in paths:
                if app_name == "store":          # Open Microsoft Store
                    os.startfile("ms-windows-store://home")
                else:
                    subprocess.Popen(paths[app_name], shell=True)  # Open other apps
                speak(f"Opening {app_name}")
                print(f"[Open App]: {app_name}")
            else:
                # Attempt to auto-find installed app
                exe_path = shutil.which(app_name)
                if exe_path:
                    subprocess.Popen(exe_path, shell=True)
                    speak(f"Opening {app_name}")
                    print(f"[Open App]: {app_name}")
                else:
                    speak(f"Cannot find {app_name} on this system.")
        elif os_name == "Linux":                    # Linux systems
            subprocess.Popen([app_name])
            speak(f"Opening {app_name}")
            print(f"[Open App]: {app_name}")
        elif os_name == "Darwin":                   # macOS
            subprocess.Popen(["open", "-a", app_name])
            speak(f"Opening {app_name}")
            print(f"[Open App]: {app_name}")
        else:
            speak("OS not supported")
    except Exception as e:
        print(f"[Error]: Open app issue - {e}")      # Log errors
        speak("Could not open the app.")

# ---------------------------
# Function to open Gmail in browser
# ---------------------------
def open_gmail():
    webbrowser.open("https://mail.google.com")       # Open Gmail URL
    speak("Opening Gmail")                            # Confirm to user
    print("[Web]: Gmail")                              # Log action

# ---------------------------
# Function to check system updates
# ---------------------------
def check_system_update():
    os_name = platform.system()                       # Detect OS
    if os_name == "Windows":                          # Windows update
        try:
            speak("Checking for Windows updates. This may take a while...")
            subprocess.run("powershell.exe Get-WindowsUpdate", shell=True)
            print("[System]: Checked for updates")
        except Exception as e:
            print(f"[Error]: System update check - {e}")
            speak("Could not check system updates.")
    elif os_name == "Linux":                          # Linux update
        try:
            speak("Checking for system updates...")
            subprocess.run(["sudo", "apt", "update"], check=True)
            print("[System]: Updates checked")
        except Exception as e:
            print(f"[Error]: System update check - {e}")
            speak("Could not check system updates.")
    else:
        speak("System update feature not supported on your OS.")

# ---------------------------
# Function to get weather information
# ---------------------------
def get_weather(city):
    try:
        api_key = "your_openweathermap_api_key"      # Replace with your API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data["cod"] != 200:
            speak("City not found.")
            return
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp}°C with {desc}")
        print(f"[Weather]: {city} - {temp}°C, {desc}")
    except Exception as e:
        print(f"[Error]: Weather issue - {e}")
        speak("Could not fetch weather.")

# ---------------------------
# Function to get latest news headlines
# ---------------------------
def get_news():
    try:
        api_key = "your_newsapi_key"                 
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
        response = requests.get(url)
        data = response.json()
        articles = data["articles"][:5]             
        for i, article in enumerate(articles, 1):
            speak(f"Headline {i}: {article['title']}")
            print(f"[News {i}]: {article['title']}")
    except Exception as e:
        print(f"[Error]: News issue - {e}")
        speak("Could not fetch news.")

# ---------------------------
# Function to tell random jokes
# ---------------------------
def tell_joke():
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field.",
        "I told my computer I needed a break, and it said no problem – it needed one too.",
        "Why don't scientists trust atoms? Because they make up everything."
    ]
    joke = random.choice(jokes)
    speak(joke)
    print(f"[Joke]: {joke}")

# ---------------------------
# Function to search files on laptop
# ---------------------------
def find_file(filename, path=None):
    try:
        path = path or os.path.expanduser("~")
        matches = []
        for root, dirs, files in os.walk(path):
            if filename.lower() in [f.lower() for f in files]:
                matches.append(os.path.join(root, filename))
        if matches:
            speak(f"Found {len(matches)} result(s).")
            for match in matches:
                print(f"[File]: {match}")
        else:
            speak("No matching files found.")
            print("[File]: No matches")
    except Exception as e:
        print(f"[Error]: File search - {e}")
        speak("Could not search files.")

# ---------------------------
# Main assistant function
# ---------------------------
def run_assistant():
    speak("Hello Nishant, I am your smart assistant. How can I help you today?")
    while True:
        command = listen()
        if command == "":
            continue

        # ---------------------------
        # Time and Date
        # ---------------------------
        if "time" in command:
            speak(datetime.datetime.now().strftime("Current time is %I:%M %p"))
        elif "date" in command:
            speak(datetime.datetime.now().strftime("Today's date is %d %B %Y"))

        # ---------------------------
        # Wikipedia search
        # ---------------------------
        elif "who is" in command or "what is" in command:
            query = command.replace("who is", "").replace("what is", "").strip()
            try:
                info = wikipedia.summary(query, sentences=2)
                speak(info)
            except Exception:
                speak("Could not find information.")

        # ---------------------------
        # Google search
        # ---------------------------
        elif "search" in command or "google" in command:
            query = command.replace("search", "").replace("google", "").strip()
            speak(f"Searching Google for {query}")
            pywhatkit.search(query)

        # ---------------------------
        # Open websites
        # ---------------------------
        elif "open google" in command:
            webbrowser.open("https://www.google.com")
        elif "open youtube" in command:
            webbrowser.open("https://www.youtube.com")
        elif "open gmail" in command:
            open_gmail()

        # ---------------------------
        # Open apps
        # ---------------------------
        elif "open" in command:
            app_name = command.replace("open", "").strip()
            open_on_laptop(app_name)

        # ---------------------------
        # Weather, news, jokes
        # ---------------------------
        elif "weather" in command:
            speak("Which city?")
            city = listen()
            get_weather(city)
        elif "news" in command:
            get_news()
        elif "joke" in command:
            tell_joke()

        # ---------------------------
        # Email and WhatsApp
        # ---------------------------
        elif "send email" in command:
            speak("To whom should I send the email?")
            to_address = listen()
            speak("What is the subject?")
            subject = listen()
            speak("What is the message?")
            content = listen()
            send_email(to_address, subject, content)
        elif "send whatsapp" in command:
            speak("Enter recipient number with country code")
            phone_number = listen()
            speak("Enter message")
            message = listen()
            send_whatsapp_message(phone_number, message)

        # ---------------------------
        # System updates
        # ---------------------------
        elif "check updates" in command or "system update" in command:
            check_system_update()

        # ---------------------------
        # Remember / Recall Notes
        # ---------------------------
        elif "remember" in command:
            speak("What should I remember?")
            item = listen()
            memory['note'] = item
            speak(f"I will remember: {item}")
        elif "do you remember" in command:
            note = memory.get('note', 'Nothing yet.')
            speak(f"You asked me to remember: {note}")

        # ---------------------------
        # Find files
        # ---------------------------
        elif "find file" in command:
            speak("What is the filename?")
            filename = listen()
            find_file(filename)

        # ---------------------------
        # Exit assistant
        # ---------------------------
        elif "exit" in command or "stop" in command or "bye" in command:
            speak("Goodbye! Have a nice day.")
            break

        # ---------------------------
        # Unknown commands
        # ---------------------------
        else:
            speak("I did not understand that command.")

# ---------------------------
# Run the assistant
# ---------------------------
run_assistant()

