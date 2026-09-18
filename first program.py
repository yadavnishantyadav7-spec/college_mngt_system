"""
Smart Voice Assistant
Author: Nishant
Description: Professional AI-based voice assistant with modular architecture.
"""

# ==============================
# Standard Library Imports
# ==============================

import os                          # Access environment variables
import sys                         # System exit handling
import random                      # Random joke selection
import logging                     # Logging instead of print debugging
import datetime                    # Date & time functions
import webbrowser                  # Open websites
import requests                    # API calls
import smtplib                     # Send emails

# ==============================
# Third-Party Imports
# ==============================

import speech_recognition as sr    # Speech recognition
import pyttsx3                     # Text-to-speech engine
import wikipedia                   # Wikipedia summaries
from email.message import EmailMessage  # Email formatting
from dotenv import load_dotenv     # Load environment variables

# ==============================
# Load Environment Variables
# ==============================

load_dotenv()  # Load variables from .env file

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")          # Gmail address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")       # Gmail app password
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Weather API key
NEWS_API_KEY = os.getenv("NEWS_API_KEY")            # News API key

# ==============================
# Configure Logging System
# ==============================

logging.basicConfig(
    level=logging.INFO,   # Log INFO and above
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==============================
# Smart Assistant Class
# ==============================

class SmartAssistant:
    """
    Main Assistant Class
    Contains all functionality of voice assistant
    """

    def __init__(self, username="Nishant"):
        """Initialize assistant configuration"""

        self.username = username          # Store username
        self.memory = {}                  # Dictionary to store memory notes

        self.engine = pyttsx3.init()      # Initialize text-to-speech engine
        self.engine.setProperty("rate", 170)  # Set speaking speed

        self.recognizer = sr.Recognizer() # Speech recognizer object

    # ==========================
    # Text-to-Speech Function
    # ==========================

    def speak(self, text):
        """Convert text to speech and log it"""

        logging.info(f"Assistant: {text}")  # Log message
        print(f"[Assistant]: {text}")       # Print to terminal

        self.engine.say(text)               # Convert text to speech
        self.engine.runAndWait()            # Wait until speaking finishes

    # ==========================
    # Speech Recognition
    # ==========================

    def listen(self):
        """Listen to microphone input and convert speech to text"""

        try:
            with sr.Microphone() as source:   # Use default microphone
                self.speak("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5)

            # Convert speech to text using Google API
            command = self.recognizer.recognize_google(audio, language="en-IN")

            logging.info(f"User: {command}")
            return command.lower()

        except sr.UnknownValueError:
            self.speak("Sorry, I did not understand.")

        except sr.RequestError:
            self.speak("Internet connection error.")

        except Exception as e:
            logging.error(f"Speech Recognition Error: {e}")

        return ""  # Return empty string if error occurs

    # ==========================
    # Email Function
    # ==========================

    def send_email(self, to_address, subject, content):
        """Send email using Gmail SMTP"""

        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            self.speak("Email credentials are not configured.")
            return

        try:
            msg = EmailMessage()              # Create email object
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = to_address
            msg["Subject"] = subject
            msg.set_content(content)

            # Connect to Gmail SMTP server
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()             # Enable security
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)

            self.speak("Email sent successfully.")

        except Exception as e:
            logging.error(f"Email Error: {e}")
            self.speak("Failed to send email.")

    # ==========================
    # Weather Function
    # ==========================

    def get_weather(self, city):
        """Fetch weather using OpenWeather API"""

        if not OPENWEATHER_API_KEY:
            self.speak("Weather API key is missing.")
            return

        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Raise error if HTTP fails

            data = response.json()

            if data.get("cod") != 200:
                self.speak("City not found.")
                return

            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]

            self.speak(f"The temperature in {city} is {temp} degree Celsius with {desc}")

        except requests.exceptions.RequestException:
            self.speak("Network error while fetching weather.")

        except Exception as e:
            logging.error(f"Weather Error: {e}")
            self.speak("Unable to fetch weather.")

    # ==========================
    # News Function
    # ==========================

    def get_news(self):
        """Fetch top 5 news headlines"""

        if not NEWS_API_KEY:
            self.speak("News API key is missing.")
            return

        try:
            url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"

            response = requests.get(url, timeout=5)
            response.raise_for_status()

            data = response.json()
            articles = data.get("articles", [])[:5]

            if not articles:
                self.speak("No news available.")
                return

            for i, article in enumerate(articles, start=1):
                self.speak(f"Headline {i}: {article['title']}")

        except requests.exceptions.RequestException:
            self.speak("Network error while fetching news.")

        except Exception as e:
            logging.error(f"News Error: {e}")
            self.speak("Unable to fetch news.")

    # ==========================
    # Joke Function
    # ==========================

    def tell_joke(self):
        """Tell a random joke"""

        jokes = [
            "Why did the scarecrow win an award? Because he was outstanding in his field.",
            "I told my computer I needed a break, and it said no problem – it needed one too.",
            "Why don't scientists trust atoms? Because they make up everything."
        ]

        self.speak(random.choice(jokes))

    # ==========================
    # Time & Date Functions
    # ==========================

    def get_time(self):
        """Speak current time"""

        now = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"Current time is {now}")

    def get_date(self):
        """Speak today's date"""

        today = datetime.datetime.now().strftime("%d %B %Y")
        self.speak(f"Today's date is {today}")

    # ==========================
    # Command Processing
    # ==========================

    def process_command(self, command):
        """Process voice command and trigger actions"""

        if "time" in command:
            self.get_time()

        elif "date" in command:
            self.get_date()

        elif "who is" in command or "what is" in command:
            query = command.replace("who is", "").replace("what is", "").strip()

            try:
                summary = wikipedia.summary(query, sentences=2)
                self.speak(summary)
            except wikipedia.exceptions.DisambiguationError:
                self.speak("Multiple results found. Please be more specific.")
            except Exception:
                self.speak("No information found.")

        elif "weather" in command:
            self.speak("Which city?")
            city = self.listen()
            if city:
                self.get_weather(city)

        elif "news" in command:
            self.get_news()

        elif "joke" in command:
            self.tell_joke()

        elif "open youtube" in command:
            webbrowser.open("https://youtube.com")
            self.speak("Opening YouTube")

        elif "open google" in command:
            webbrowser.open("https://google.com")
            self.speak("Opening Google")

        elif "exit" in command or "bye" in command:
            self.speak("Goodbye! Have a nice day.")
            sys.exit(0)

        else:
            self.speak("I did not understand that command.")

    # ==========================
    # Run Assistant
    # ==========================

    def run(self):
        """Start assistant loop"""

        self.speak(f"Hello {self.username}, I am your smart assistant.")

        while True:
            command = self.listen()
            if command:
                self.process_command(command)


# ==============================
# Main Entry Point
# ==============================

if __name__ == "__main__":
    assistant = SmartAssistant("Nishant")  # Create assistant object
    assistant.run()                        # Start assistant




