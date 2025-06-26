import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import pyaudio
import schedule
import time
import os
import re
import json
import random
from dotenv import load_dotenv
from gmail_oauth import get_gmail_service, send_email, read_emails

# Load environment variables
load_dotenv()

class VoiceAssistant:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.setup_voice()
        self.setup_microphone()
        
        # Initialize email configuration
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.default_subject = os.getenv('DEFAULT_SUBJECT', 'msg from vc assistant')
        
        # Initialize Gmail service
        try:
            if not os.path.exists('credentials.json'):
                print("Error: credentials.json file not found!")
                print("Please make sure you have downloaded the credentials.json file from Google Cloud Console")
                print("and placed it in the same directory as main.py")
                self.gmail_service = None
            else:
                self.gmail_service = get_gmail_service()
                print("Gmail service initialized successfully!")
                print(f"Using email: {self.sender_email}")
        except Exception as e:
            print(f"Error initializing Gmail service: {e}")
            print("Please check your credentials.json file and make sure it's valid")
            self.gmail_service = None

        # Initialize learning system
        self.learning_data = self.load_learning_data()
        self.user_preferences = self.load_user_preferences()
        self.conversation_history = []
        self.last_interaction_time = time.time()
        self.thinking_time = random.uniform(0.5, 1.5)  # Random thinking time for more natural feel
        self.interaction_count = 0
        self.learning_threshold = 5  # Number of interactions before saving learning data

    def load_learning_data(self):
        """Load or create learning data file"""
        try:
            if os.path.exists('learning_data.json'):
                with open('learning_data.json', 'r') as f:
                    data = json.load(f)
                    print("Successfully loaded existing learning data")
                    return data
            else:
                print("Creating new learning data file")
                initial_data = {
                    'common_phrases': {},
                    'user_preferences': {},
                    'interaction_patterns': {},
                    'response_patterns': {},
                    'time_based_patterns': {},
                    'command_success_rate': {},
                    'last_updated': datetime.datetime.now().isoformat(),
                    'total_interactions': 0,
                    'learning_progress': {
                        'phrases_learned': 0,
                        'patterns_recognized': 0,
                        'successful_commands': 0
                    }
                }
                self.save_learning_data(initial_data)
                return initial_data
        except Exception as e:
            print(f"Error loading learning data: {e}")
            return self.create_default_learning_data()

    def create_default_learning_data(self):
        """Create default learning data structure"""
        return {
            'common_phrases': {},
            'user_preferences': {},
            'interaction_patterns': {},
            'response_patterns': {},
            'time_based_patterns': {},
            'command_success_rate': {},
            'last_updated': datetime.datetime.now().isoformat(),
            'total_interactions': 0,
            'learning_progress': {
                'phrases_learned': 0,
                'patterns_recognized': 0,
                'successful_commands': 0
            }
        }

    def save_learning_data(self, data=None):
        """Save learning data to file"""
        try:
            if data is None:
                data = self.learning_data
            with open('learning_data.json', 'w') as f:
                json.dump(data, f, indent=4)
            print("Learning data saved successfully")
        except Exception as e:
            print(f"Error saving learning data: {e}")

    def load_user_preferences(self):
        """Load or create user preferences"""
        try:
            if os.path.exists('user_preferences.json'):
                with open('user_preferences.json', 'r') as f:
                    return json.load(f)
            return {
                'name': None,
                'preferred_greeting': None,
                'reminder_preferences': {},
                'email_preferences': {},
                'interaction_preferences': {
                    'preferred_voice_speed': 150,
                    'preferred_voice_volume': 1.0,
                    'preferred_response_style': 'concise'
                },
                'last_updated': datetime.datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error loading user preferences: {e}")
            return {}

    def save_user_preferences(self):
        """Save user preferences to file"""
        try:
            with open('user_preferences.json', 'w') as f:
                json.dump(self.user_preferences, f, indent=4)
            print("User preferences saved successfully")
        except Exception as e:
            print(f"Error saving user preferences: {e}")

    def learn_from_interaction(self, command, response, success=True):
        """Learn from user interactions with enhanced learning capabilities"""
        # Only learn from non-command phrases
        if any(keyword in command.lower() for keyword in [
            "time", "date", "reminder", "search", "email", "send", "check", "read",
            "exit", "goodbye", "bye", "hello", "hi", "hey"
        ]):
            return

        self.interaction_count += 1
        current_time = datetime.datetime.now()
        hour = current_time.hour
        day_of_week = current_time.strftime("%A")

        # Update common phrases with more detailed tracking
        if command not in self.learning_data['common_phrases']:
            self.learning_data['common_phrases'][command] = {
                'count': 1,
                'responses': [response],
                'success_rate': 1.0 if success else 0.0,
                'last_used': current_time.isoformat(),
                'context': {
                    'hour': hour,
                    'day': day_of_week
                }
            }
            self.learning_data['learning_progress']['phrases_learned'] += 1
        else:
            self.learning_data['common_phrases'][command]['count'] += 1
            if response not in self.learning_data['common_phrases'][command]['responses']:
                self.learning_data['common_phrases'][command]['responses'].append(response)
            self.learning_data['common_phrases'][command]['last_used'] = current_time.isoformat()
            # Update success rate with weighted average
            current_success = self.learning_data['common_phrases'][command]['success_rate']
            self.learning_data['common_phrases'][command]['success_rate'] = (current_success * 0.7 + (1.0 if success else 0.0) * 0.3)

        # Update time-based patterns with more context
        if hour not in self.learning_data['time_based_patterns']:
            self.learning_data['time_based_patterns'][hour] = []
        self.learning_data['time_based_patterns'][hour].append({
            'command': command,
            'day': day_of_week,
            'timestamp': current_time.isoformat(),
            'success': success,
            'response': response
        })

        # Update command success rate with more detailed tracking
        if command not in self.learning_data['command_success_rate']:
            self.learning_data['command_success_rate'][command] = {
                'successful': 1 if success else 0,
                'total': 1,
                'last_success': current_time.isoformat() if success else None,
                'context': {
                    'hour': hour,
                    'day': day_of_week
                }
            }
        else:
            self.learning_data['command_success_rate'][command]['total'] += 1
            if success:
                self.learning_data['command_success_rate'][command]['successful'] += 1
                self.learning_data['command_success_rate'][command]['last_success'] = current_time.isoformat()

        # Update learning progress
        self.learning_data['total_interactions'] += 1
        if success:
            self.learning_data['learning_progress']['successful_commands'] += 1

        # Save learning data periodically
        if self.interaction_count >= self.learning_threshold:
            print("Saving learning data...")  # Debug print
            self.save_learning_data()
            self.interaction_count = 0
            print("Learning data updated and saved")

    def get_personalized_response(self, command):
        """Get a personalized response based on enhanced learning data"""
        # Only use personalized responses for non-command phrases
        if any(keyword in command.lower() for keyword in [
            "time", "date", "reminder", "search", "email", "send", "check", "read",
            "exit", "goodbye", "bye", "hello", "hi", "hey"
        ]):
            return None

        current_time = datetime.datetime.now()
        hour = current_time.hour
        day_of_week = current_time.strftime("%A")

        # Check for exact match in common phrases with success rate threshold
        if command in self.learning_data['common_phrases']:
            phrase_data = self.learning_data['common_phrases'][command]
            if phrase_data['success_rate'] > 0.8:  # Increased threshold for better accuracy
                print(f"Found personalized response for command: {command}")  # Debug print
                return random.choice(phrase_data['responses'])

        # Check time-based patterns with context
        if hour in self.learning_data['time_based_patterns']:
            time_patterns = self.learning_data['time_based_patterns'][hour]
            similar_commands = [p['command'] for p in time_patterns 
                             if p['day'] == day_of_week and p.get('success', False)]
            if similar_commands:
                most_common = max(set(similar_commands), key=similar_commands.count)
                if most_common in self.learning_data['common_phrases']:
                    print(f"Found time-based response for command: {command}")  # Debug print
                    return random.choice(self.learning_data['common_phrases'][most_common]['responses'])

        return None

    def format_email_address(self, email_text):
        """Format and validate email address from voice input"""
        # Remove any spaces
        email_text = email_text.strip().replace(" ", "")
        
        # Common voice-to-text corrections
        replacements = {
            "at": "@",
            "dot": ".",
            "underscore": "_",
            "dash": "-",
            "minus": "-",
            "plus": "+",
            "equals": "=",
            "hash": "#",
            "dollar": "$",
            "percent": "%",
            "ampersand": "&",
            "star": "*",
            "asterisk": "*",
            "exclamation": "!",
            "question": "?",
            "caret": "^",
            "tilde": "~",
            "backtick": "`",
            "pipe": "|",
            "backslash": "\\",
            "forward slash": "/",
            "comma": ",",
            "semicolon": ";",
            "colon": ":",
            "quote": "'",
            "double quote": '"',
            "single quote": "'",
            "apostrophe": "'",
            "left parenthesis": "(",
            "right parenthesis": ")",
            "left bracket": "[",
            "right bracket": "]",
            "left brace": "{",
            "right brace": "}",
            "less than": "<",
            "greater than": ">",
            "space": "",
        }
        
        # Apply replacements
        for word, symbol in replacements.items():
            email_text = email_text.replace(word, symbol)
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email_text):
            return None
        
        return email_text

    def get_email_address(self):
        """Get and validate email address from user"""
        max_attempts = 3
        for attempt in range(max_attempts):
            self.speak("Please provide the recipient's email address.")
            email_text = self.listen()
            if email_text:
                formatted_email = self.format_email_address(email_text)
                if formatted_email:
                    self.speak(f"I understood the email address as: {formatted_email}")
                    return formatted_email
                else:
                    self.speak("I couldn't understand the email address format. Please try again.")
            else:
                self.speak("I didn't catch that. Please try again.")
        
        self.speak("Failed to get a valid email address after multiple attempts.")
        return None

    def setup_voice(self):
        """Configure the text-to-speech voice settings"""
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)

    def setup_microphone(self):
        """Setup and configure microphone"""
        try:
            # Initialize PyAudio
            p = pyaudio.PyAudio()
            
            # List all audio input devices
            print("\nAvailable audio input devices:")
            input_devices = []
            for i in range(p.get_device_count()):
                dev_info = p.get_device_info_by_index(i)
                if dev_info.get('maxInputChannels') > 0:  # Only show input devices
                    print(f"Device {i}: {dev_info.get('name')}")
                    input_devices.append((i, dev_info.get('name')))
            
            # Try to find a physical microphone
            self.mic_index = None
            for index, name in input_devices:
                if "virtual" not in name.lower() and "audio relay" not in name.lower():
                    self.mic_index = index
                    print(f"\nSelected microphone: {name}")
                    break
            
            if self.mic_index is None:
                print("\nNo physical microphone found. Using default device.")
                self.mic_index = None
            
            p.terminate()
            
        except Exception as e:
            print(f"Error setting up microphone: {e}")
            self.mic_index = None

    def speak(self, text):
        """Convert text to speech with natural pauses and timing"""
        try:
            print(f"Assistant: {text}")
            
            # Add natural pauses for longer sentences
            sentences = text.split('. ')
            for i, sentence in enumerate(sentences):
                self.engine.say(sentence)
                if i < len(sentences) - 1:
                    time.sleep(0.3)  # Natural pause between sentences
            
            self.engine.runAndWait()
            
            # Add thinking time for more natural interaction
            time.sleep(self.thinking_time)
            
        except Exception as e:
            print(f"Error in speech: {e}")

    def listen(self):
        """Listen for voice commands with improved recognition"""
        try:
            listener = sr.Recognizer()
            # Adjust these values for better recognition
            listener.energy_threshold = 300  # Lower threshold for better sensitivity
            listener.dynamic_energy_threshold = True
            listener.pause_threshold = 0.8  # Longer pause threshold for more natural speech
            listener.phrase_threshold = 0.3  # Lower phrase threshold
            listener.non_speaking_duration = 0.5  # Longer non-speaking duration
            
            with sr.Microphone(device_index=self.mic_index) as source:
                print("\nListening... (Speak now)")
                # Adjust for ambient noise
                print("Adjusting for ambient noise...")
                listener.adjust_for_ambient_noise(source, duration=2)
                print("Ready to capture your voice...")
                
                try:
                    print("Waiting for your voice...")
                    voice = listener.listen(source, timeout=10, phrase_time_limit=10)  # Increased timeouts
                    print("Voice detected! Processing...")
                    command = listener.recognize_google(voice)
                    print(f"You said: {command}")
                    
                    # Add to conversation history
                    self.conversation_history.append({
                        'timestamp': datetime.datetime.now().isoformat(),
                        'command': command,
                        'type': 'user'
                    })
                    
                    return command.lower()
                except sr.WaitTimeoutError:
                    print("No speech detected within timeout period")
                    return ""
                except sr.UnknownValueError:
                    print("Could not understand audio - please speak clearly")
                    return ""
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service: {e}")
                    return ""
                
        except Exception as e:
            print(f"Error in listening: {e}")
            return ""

    def set_reminder(self, time_str):
        """Set a reminder for a specific time"""
        try:
            # Parse the time string
            reminder_time = datetime.datetime.strptime(time_str, "%H:%M").time()
            current_time = datetime.datetime.now().time()
            
            # Calculate time difference
            time_diff = datetime.datetime.combine(datetime.date.today(), reminder_time) - \
                       datetime.datetime.combine(datetime.date.today(), current_time)
            
            if time_diff.total_seconds() < 0:
                self.speak("That time has already passed today.")
                return
            
            # Schedule the reminder
            schedule.every().day.at(time_str).do(self.speak, "Reminder! Time to check your tasks.")
            self.speak(f"Reminder set for {time_str}")
            
            # Save to user preferences
            if 'reminders' not in self.user_preferences:
                self.user_preferences['reminders'] = []
            self.user_preferences['reminders'].append({
                'time': time_str,
                'created_at': datetime.datetime.now().isoformat()
            })
            self.save_user_preferences()
            
        except ValueError:
            self.speak("Please specify the time in HH:MM format (e.g., 14:30)")

    def process_command(self, command):
        """Process the voice command and execute appropriate action"""
        if not command:
            return

        # Convert command to lowercase for consistent matching
        command = command.lower().strip()
        print(f"Processing command: {command}")  # Debug print

        success = True
        response = ""

        # Command matching with debug prints
        if any(greeting in command for greeting in ["hello", "hi", "hey", "greetings"]):
            print("Matched greeting command")  # Debug print
            greeting = f"Hello! How can I assist you today?"
            self.speak(greeting)
            response = greeting
            self.learn_from_interaction(command, greeting, True)
        
        elif "what time" in command or "current time" in command or "tell me the time" in command:
            print("Matched time command")  # Debug print
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response = f"The current time is {current_time}"
            self.speak(response)
            self.learn_from_interaction(command, response, True)
        
        elif "what date" in command or "today's date" in command or "what day" in command:
            print("Matched date command")  # Debug print
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            response = f"Today is {current_date}"
            self.speak(response)
            self.learn_from_interaction(command, response, True)
        
        elif "set reminder" in command or "create reminder" in command or "remind me" in command:
            print("Matched reminder command")  # Debug print
            self.speak("What time would you like to set the reminder for? (Please say the time in 24-hour format)")
            time_str = self.listen()
            if time_str:
                try:
                    self.set_reminder(time_str)
                    response = f"Reminder set for {time_str}"
                    self.speak(response)
                    self.learn_from_interaction(command, response, True)
                except:
                    response = "Failed to set reminder"
                    self.speak(response)
                    self.learn_from_interaction(command, response, False)
        
        elif "search for" in command or "look up" in command or "search" in command:
            print("Matched search command")  # Debug print
            # Extract search term from command
            search_term = command
            for prefix in ["search for", "look up", "search"]:
                search_term = search_term.replace(prefix, "").strip()
            
            if search_term:
                print(f"Searching for: {search_term}")  # Debug print
                self.speak(f"Searching for {search_term}")
                pywhatkit.search(search_term)
                response = f"Searched for {search_term}"
                self.learn_from_interaction(command, response, True)
            else:
                self.speak("What would you like me to search for?")
                search_term = self.listen()
                if search_term:
                    print(f"Searching for: {search_term}")  # Debug print
                    self.speak(f"Searching for {search_term}")
                    pywhatkit.search(search_term)
                    response = f"Searched for {search_term}"
                    self.learn_from_interaction(command, response, True)
                else:
                    response = "No search term provided"
                    self.speak(response)
                    self.learn_from_interaction(command, response, False)
        
        elif "send email" in command or "write email" in command or "compose email" in command:
            print("Matched send email command")  # Debug print
            if not self.gmail_service:
                response = "Gmail service is not initialized. Please check your credentials."
                self.speak(response)
                self.learn_from_interaction(command, response, False)
                return

            to_email = self.get_email_address()
            if to_email:
                self.speak("What should be the message?")
                body = self.listen()
                if body:
                    if send_email(self.gmail_service, to_email, self.default_subject, body):
                        response = "Email sent successfully!"
                        self.speak(response)
                        self.learn_from_interaction(command, response, True)
                    else:
                        response = "Failed to send email. Please check the console for details."
                        self.speak(response)
                        self.learn_from_interaction(command, response, False)
        
        elif "check email" in command or "read email" in command or "check inbox" in command:
            print("Matched check email command")  # Debug print
            if not self.gmail_service:
                response = "Gmail service is not initialized. Please check your credentials."
                self.speak(response)
                self.learn_from_interaction(command, response, False)
                return

            self.speak("Reading your latest emails.")
            emails = read_emails(self.gmail_service, 3)  # Read latest 3 emails
            if emails:
                response = f"You have {len(emails)} recent emails."
                self.speak(response)
                for email in emails:
                    self.speak(f"From: {email['sender']}")
                    self.speak(f"Subject: {email['subject']}")
                    self.speak(f"Content: {email['content']}")
                self.learn_from_interaction(command, response, True)
            else:
                response = "No emails found or there was an error reading your inbox."
                self.speak(response)
                self.learn_from_interaction(command, response, False)
        
        elif "exit" in command or "goodbye" in command or "bye" in command:
            print("Matched exit command")  # Debug print
            response = "Goodbye! Have a great day!"
            self.speak(response)
            self.learn_from_interaction(command, response, True)
            exit()
        
        else:
            print(f"No specific command matched for: {command}")  # Debug print
            # If no specific command is matched, ask for clarification
            response = "I'm not sure I understand. Could you please rephrase that?"
            self.speak(response)
            self.learn_from_interaction(command, response, False)

    def run(self):
        """Main loop to run the voice assistant"""
        self.speak("Voice assistant is ready. How can I help you?")
        
        while True:
            schedule.run_pending()  # Check for scheduled reminders
            command = self.listen()
            self.process_command(command)
            time.sleep(1)

def main():
    try:
        print("Starting Voice Assistant...")
        print("Checking configuration...")
        
        # Check for required files
        if not os.path.exists('.env'):
            print("Error: .env file not found!")
            print("Please create a .env file with your configuration")
            return
            
        if not os.path.exists('credentials.json'):
            print("Error: credentials.json file not found!")
            print("Please download credentials.json from Google Cloud Console")
            return
            
        print("Configuration check complete!")
        assistant = VoiceAssistant()
        assistant.run()
    except Exception as e:
        print(f"Error starting voice assistant: {e}")

if __name__ == "__main__":
    main()
