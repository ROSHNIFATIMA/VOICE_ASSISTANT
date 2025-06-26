# 🤖 AI Voice Assistant - OIBSIP Internship Project

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)](https://github.com/yourusername/voice-assistant)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT%20Integration-orange.svg)](https://openai.com/)
[![Gmail](https://img.shields.io/badge/Gmail-API%20Integration-red.svg)](https://developers.google.com/gmail/api)

> **A sophisticated AI-powered voice assistant developed as part of the OIBSIP (Oasis Infobyte Summer Internship Program) that combines advanced speech recognition, natural language processing, and multiple API integrations to deliver an intelligent, context-aware voice-controlled experience.**

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [Project Architecture](#project-architecture)
- [API Integrations](#api-integrations)
- [Self-Learning System](#self-learning-system)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## 🎯 Overview

This AI Voice Assistant represents a comprehensive solution that demonstrates proficiency in:
- **Speech Recognition & Processing**
- **Natural Language Understanding**
- **API Integration & Management**
- **Machine Learning Concepts**
- **Software Architecture Design**
- **Security Best Practices**

The project showcases real-world application development skills through the integration of multiple cutting-edge technologies and APIs.

## ✨ Features

### 🧠 Core Intelligence
- **Advanced Voice Recognition**: Real-time speech-to-text conversion with noise filtering
- **Natural Language Processing**: Context-aware command interpretation
- **AI-Powered Conversations**: OpenAI GPT integration for intelligent responses
- **Self-Learning System**: Adaptive behavior based on user interactions
- **Context Awareness**: Personalized responses and memory retention

### 🌟 Key Capabilities

| Feature | Description | Technology Used |
|---------|-------------|-----------------|
| **Time & Date** | Natural language time queries and date information | Python datetime |
| **Weather Updates** | Real-time weather data and forecasts | Weather API |
| **AI Conversations** | Intelligent responses and problem solving | OpenAI GPT |
| **Email Management** | Voice-controlled email operations | Gmail API + OAuth2 |
| **Web Search** | Voice-activated information retrieval | PyWhatKit |
| **Reminder System** | Smart scheduling and notifications | Schedule library |

### 🔧 Technical Features
- **Multi-threaded Architecture**: Non-blocking voice processing
- **Error Handling**: Robust exception management
- **Security**: OAuth2 authentication and secure credential management
- **Scalability**: Modular design for easy feature additions
- **Cross-platform**: Compatible with Windows, macOS, and Linux

## 🛠 Technology Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **Speech Recognition**: Real-time audio processing
- **PyTTSx3**: Text-to-speech synthesis
- **PyAudio**: Audio input/output handling

### AI & ML
- **OpenAI GPT**: Natural language understanding
- **Custom Learning Algorithm**: User behavior adaptation
- **Context Management**: Conversation memory

### APIs & Services
- **Gmail API**: Email management with OAuth2
- **Weather API**: Real-time weather data
- **Web Search APIs**: Information retrieval

### Development Tools
- **Virtual Environment**: Dependency isolation
- **Environment Variables**: Secure configuration management
- **Git Version Control**: Source code management

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Ubuntu 18.04+
- **Python**: Version 3.8 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 500MB available space
- **Internet**: Stable broadband connection

### Required Accounts
- **Gmail Account**: For email functionality
- **OpenAI Account**: For AI conversations
- **Weather API Account**: For weather updates

### Hardware Requirements
- **Microphone**: Working audio input device
- **Speakers/Headphones**: Audio output capability
- **Webcam** (optional): For future video features

## 🚀 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/voice-assistant.git
cd voice-assistant
```

### Step 2: Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:
```env
# Email Configuration
SENDER_EMAIL=your_email@gmail.com
DEFAULT_SUBJECT=Message from AI Voice Assistant

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
```

### Step 5: Set Up API Credentials

#### Gmail API Setup
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Download `credentials.json` and place in project root

#### OpenAI API Setup
1. Sign up at [OpenAI Platform](https://platform.openai.com/)
2. Generate API key
3. Add to `.env` file

#### Weather API Setup
1. Choose a weather API provider (OpenWeatherMap, WeatherAPI, etc.)
2. Register and get API key
3. Add to `.env` file

## 📖 Usage Guide

### Starting the Assistant
```bash
python main.py
```

### Voice Commands Reference

| Command | Function | Example |
|---------|----------|---------|
| **Time Queries** | Get current time/date | "What time is it?" |
| **Weather** | Get weather information | "What's the weather like?" |
| **AI Chat** | Intelligent conversations | "Tell me about quantum physics" |
| **Email** | Email management | "Send email to john@example.com" |
| **Search** | Web search | "Search for Python tutorials" |
| **Reminders** | Set notifications | "Remind me to call mom at 3 PM" |
| **Exit** | Close assistant | "Goodbye" or "Exit" |

### Advanced Usage
- **Context Continuation**: The assistant remembers conversation context
- **Natural Language**: Use conversational commands instead of rigid syntax
- **Learning**: Assistant improves responses based on your usage patterns

## 🏗 Project Architecture

```
voice-assistant/
├── 📁 Core Application
│   ├── main.py                 # Main application entry point
│   ├── gmail_oauth.py          # Gmail API integration
│   └── learning_system.py      # Self-learning algorithms
│
├── 📁 Configuration
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (create)
│   ├── credentials.json        # Gmail OAuth (create)
│   └── .gitignore             # Git ignore rules
│
├── 📁 Data & Learning
│   ├── learning_data.json      # User interaction data (auto-generated)
│   └── token.pickle           # OAuth tokens (auto-generated)
│
├── 📁 Documentation
│   ├── README.md              # Project documentation
│   └── docs/                  # Additional documentation
│
└── 📁 Virtual Environment
    └── venv/                  # Python virtual environment
```

## 🔌 API Integrations

### Gmail API Integration
- **OAuth2 Authentication**: Secure email access
- **Email Operations**: Send, read, and manage emails
- **Error Handling**: Robust connection management

### OpenAI GPT Integration
- **Natural Language Processing**: Advanced conversation capabilities
- **Context Awareness**: Maintains conversation flow
- **Creative Responses**: Problem-solving and explanations

### Weather API Integration
- **Real-time Data**: Current weather conditions
- **Forecasting**: Weather predictions
- **Location Services**: GPS-based weather information

## 🧠 Self-Learning System

### Learning Components
- **Command Recognition**: Improves accuracy over time
- **User Preferences**: Adapts to individual usage patterns
- **Response Optimization**: Enhances interaction quality
- **Success Tracking**: Monitors command effectiveness

### Data Storage
- **JSON Format**: Human-readable learning data
- **Privacy Focused**: Local storage only
- **Backup Capability**: Easy data export/import

## 🔧 Troubleshooting

### Common Issues & Solutions

#### Audio Problems
```bash
# Windows PyAudio Installation
pip install pipwin
pipwin install pyaudio

# Linux Audio Issues
sudo apt-get install portaudio19-dev
pip install pyaudio
```

#### API Authentication Issues
- **Gmail**: Verify `credentials.json` location and API enablement
- **OpenAI**: Check API key validity and account credits
- **Weather**: Confirm API key and rate limits

#### Performance Issues
- **Memory**: Close unnecessary applications
- **Network**: Check internet connection stability
- **Processing**: Ensure adequate CPU resources

### Debug Mode
Enable debug logging by modifying the main configuration:
```python
DEBUG_MODE = True
```

## 🤝 Contributing

We welcome contributions to improve this project! Please follow these guidelines:

### Contribution Process
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Code Standards
- Follow PEP 8 Python style guidelines
- Add comments for complex logic
- Include error handling
- Write unit tests for new features

### Reporting Issues
- Use the GitHub Issues page
- Provide detailed error descriptions
- Include system information
- Attach relevant log files

## 🙏 Acknowledgments

### Technology Providers
- **OpenAI** for GPT integration and natural language processing
- **Google Cloud Platform** for Gmail API and OAuth2 services
- **Weather API Providers** for real-time weather data
- **SpeechRecognition** library for audio processing
- **PyAudio** for cross-platform audio handling

### Educational Resources
- **OIBSIP (Oasis Infobyte)** for the internship opportunity
- **Python Documentation** for language reference
- **GitHub Community** for open-source collaboration

### Development Tools
- **Visual Studio Code** for development environment
- **Git** for version control
- **GitHub** for project hosting and collaboration

## 📞 Support & Contact

### Getting Help
- **Documentation**: Check this README and project docs
- **Issues**: Use GitHub Issues for bug reports
- **Discussions**: Join project discussions for questions

---

<div align="center">

**Developed for OIBSIP Internship Program**

*This project demonstrates advanced Python development skills, API integration, and AI implementation.*

</div> 