# AI Voice Assistant 

A Python-based voice assistant that uses speech recognition, text-to-speech, OpenAI GPT for AI conversations, weather updates, Gmail API for email management, and a self-learning system. 

## Features
- Voice-controlled commands (speech-to-text and text-to-speech)
- AI-powered conversations (OpenAI GPT)
- Weather updates via API
- Send and read emails (Gmail API with OAuth2)
- Self-learning: adapts to user preferences and command patterns
- Secure configuration using environment variables

## Project Structure
```
OIBSIP_project_voice_assistant/
├── gmail_oauth.py        # Gmail authentication and email functions
├── main.py               # Main assistant application
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── venv/                 # Python virtual environment (not committed)
├── .env                  # Environment variables (not committed)
├── credentials.json      # Gmail API credentials (not committed)
├── token.pickle          # Gmail OAuth2 token (not committed)
├── learning_data.json    # Self-learning data (not committed)
└── __pycache__/          # Python cache files (not committed)
```

## Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/ROSHNIFATIMA/VOICE_ASSISTANT
   cd VOICE_ASSISTANT
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Add configuration files**
   - Create a `.env` file in the project root with your API keys and email config:
     ```env
     SENDER_EMAIL=your_email@gmail.com
     OPENAI_API_KEY=your_openai_api_key
     WEATHER_API_KEY=your_weather_api_key
     ```
   - Download `credentials.json` from Google Cloud Console (for Gmail API) and place it in the project root.

## Usage
Run the assistant:
```bash
python main.py
```

## Notes
- Make sure your microphone and speakers are working.
- `.env`, `credentials.json`, `token.pickle`, `learning_data.json`, `venv/`, and `__pycache__/` should be in `.gitignore` and not committed.
- For Gmail and OpenAI API, you need valid accounts and API keys.

---
**Developed for OIBSIP Internship Program** 
