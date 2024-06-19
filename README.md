Setting Up Your Voice-Controlled Virtual Assistant Chatbot
Welcome to the setup guide for Whisper AI Assistant, a voice-controlled virtual assistant chatbot using Python and Selenium.

Project Overview
This project integrates speech recognition and synthesis capabilities with web automation to create an interactive chatbot experience using DuckDuckGo Chat.

Requirements
Python 3.x
ChromeDriver
Selenium
gTTS (Google Text-to-Speech)
pygame
speech_recognition
Installation Steps
Install Python Dependencies

bash
Copy code
pip install selenium gTTS pygame SpeechRecognition
Download ChromeDriver

Download ChromeDriver from ChromeDriver Downloads and extract it. Replace chromedriver_path in the code with the path to chromedriver.exe.

Setup Brave Browser

Modify brave_path in the code to point to your Brave browser executable path.

Code Setup

Replace the placeholder paths in the code with your actual paths for brave_path and chromedriver_path.

python
Copy code
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
chromedriver_path = r"C:\path\to\chromedriver.exe"
Running the Code
To run the Whisper AI Assistant:

bash
Copy code
python whisper_ai.py
How It Works
Initialization

Initializes Selenium WebDriver with Brave browser.
Sets up speech recognition and text-to-speech functionalities.
User Interaction

Opens DuckDuckGo Chat page and handles initial setup.
Listens to user voice input using a microphone.
Converts user voice input to text using Google's speech recognition.
Chatbot Interaction

Sends user input to DuckDuckGo Chat, simulating user interaction.
Processes and reads back chatbot responses using text-to-speech.
Termination

Stops the browser session and exits cleanly.
Diagram Overview

Detailed Diagram Description
User Voice Input: Captures user voice input using a microphone.
Speech Recognition: Converts voice input into text using Google's SpeechRecognition library.
Chatbot Interaction: Uses Selenium WebDriver to interact with DuckDuckGo Chat, sending user queries and receiving responses.
Text-to-Speech: Converts chatbot responses into speech using gTTS and plays it using pygame.
Browser Automation: Controls Brave browser to simulate user actions on DuckDuckGo Chat.
Session Management: Manages browser session lifecycle, ensuring proper cleanup and termination.
Conclusion
Enjoy interacting with Whisper AI Assistant, your personal voice-controlled chatbot companion powered by Python and Selenium!

For any questions or issues, please reach out to [Github].

Author: [Ali]

Date: [2- June 2024]

Version: 1.0
