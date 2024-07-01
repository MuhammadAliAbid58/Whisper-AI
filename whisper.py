import os
from gtts import gTTS
import pygame
import tempfile
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Path to the chrome browser executable
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Path to the ChromeDriver executable
chromedriver_path = r"C:\Users\username\Downloads\Compressed\chromedriver-win64\chromedriver.exe"

# Set up options to use chrome browser
options = webdriver.ChromeOptions()
options.binary_location = chrome_path

# Runs the Browser in Hidden Mode
options.add_argument("--headless")

# Set up the ChromeDriver service
service = ChromeService(executable_path=chromedriver_path)

# Initialize the WebDriver with the options
driver = webdriver.Chrome(service=service, options=options)

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def text_to_speech(text, lang='hi', slow=False):
    # Generate speech
    tts = gTTS(text=text, lang=lang, slow=slow)
    
    # Save the speech to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    temp_file.close()
    return temp_file.name

def play_audio(file, speed=1.0):
    try:
        # Initialize pygame mixer
        pygame.mixer.init()

        # Load the audio file
        pygame.mixer.music.load(file)

        # Play the audio file
        pygame.mixer.music.play()

        # Keep the script running until the audio finishes playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        # Stop the mixer and unload the audio
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        # Clean up the audio file
        os.remove(file)

def recognize_speech():
    while True:
        with sr.Microphone() as source:
            print("Listening...")            
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            user_input = recognizer.recognize_google(audio)
            print(f"You (Voice): {user_input}")
            return user_input.lower()
        except sr.UnknownValueError:
            print("Could not understand audio.")
            audio_file = text_to_speech("I didn't catch that. Please speak again.")
            play_audio(audio_file)
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            audio_file = text_to_speech("There was an error processing your request. Please try again.")
            play_audio(audio_file)

def send_initial_query():
    initial_query = "only respond in one line"
    input_text_area = driver.find_element(By.XPATH, input_text_locator)
    input_text_area.send_keys(initial_query)
    input_text_area.send_keys(Keys.ENTER)  # Simulate pressing Enter

    # Wait for new responses to appear
    time.sleep(3)  # Adjust as needed based on response time


try:
    # Open DuckDuckGo Chat page
    driver.get('https://duckduckgo.com/chat')

    # Wait for the "Get Started" button to be clickable
    get_started_button_locator = "//button[contains(text(), 'Get Started')]"
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, get_started_button_locator))
    )

    # Find and click the "Get Started" button
    get_started_button = driver.find_element(By.XPATH, get_started_button_locator)
    get_started_button.click()

    # Wait for the "Next" button to be clickable
    next_button_locator = "//button[contains(text(), 'Next')]"
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, next_button_locator))
    )

    # Find and click the "Next" button
    next_button = driver.find_element(By.XPATH, next_button_locator)
    next_button.click()

    # Wait for the "I Agree" button to be clickable
    agree_button_locator = "//button[contains(text(), 'I Agree')]"
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, agree_button_locator))
    )

    # Find and click the "I Agree" button
    agree_button = driver.find_element(By.XPATH, agree_button_locator)
    agree_button.click()

    # Wait for the input text area to be visible and interactable
    input_text_locator = "//textarea[@name='user-prompt']"
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, input_text_locator))
    )

    # Start the interaction loop
    previous_responses = set()

    time.sleep(1)
    # Send initial query
    send_initial_query()

    # Start the interaction loop
    while True:
        # Use speech recognition for user input
        user_input = recognize_speech()

        # Check if user wants to exit
        if user_input.lower() == "exit":
            break

        # Find the input text area and send the message
        input_text_area = driver.find_element(By.XPATH, input_text_locator)
        input_text_area.send_keys(user_input)
        input_text_area.send_keys(Keys.ENTER)  # Simulate pressing Enter

        # Wait for new responses to appear
        time.sleep(3)  # Adjust as needed based on response time

        # Read and print all new response divs
        response_div_locator = "//div[contains(@class, 'NRbLelmqTtXumYt6vkvs')]//div[contains(@class, 'JXNYs5FNOplxLlVAOswQ')]"
        response_divs = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, response_div_locator))
        )

        if response_divs:
            print("\nResponses from DuckDuckGo Chat:")
            for response_div in response_divs:
                # Check for both <p> and <ol> elements
                response_texts = []
                paragraphs = response_div.find_elements(By.TAG_NAME, 'p')
                for p in paragraphs:
                    response_texts.append(p.text.strip())

                lists = response_div.find_elements(By.TAG_NAME, 'li')
                if lists:
                    list_text = "\n".join([li.text.strip() for li in lists])
                    response_texts.append(list_text)

                # Join all response texts and process
                response_text = "\n".join(response_texts)

                if response_text.strip() and response_text not in previous_responses:
                    print("-", response_text)
                    # Convert response_text to speech
                    audio_file = text_to_speech(response_text)
                    play_audio(audio_file)
                    previous_responses.add(response_text)
        else:
            print("\nNo new responses found.")

finally:
    # Close the browser session
    driver.quit()
