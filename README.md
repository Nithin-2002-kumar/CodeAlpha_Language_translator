### Python Translator
This is a desktop translator application built with Python using the `tkinter` library for the graphical user interface (GUI). It leverages the *Gemini API* for text translation and uses the local `pyttsx3` engine for text-to-speech functionality.

The application allows users to translate text between a variety of languages and hear the translated text spoken aloud, making it a versatile and useful tool.

## Features
* Accurate Translation: Utilizes the advanced Gemini API for high-quality, up-to-date translations.

* Offline Text-to-Speech: The pyttsx3 library provides fast, offline audio playback of translated text.

* Intuitive GUI: A clean and simple user interface built with tkinter that makes the application easy to use.

* Multi-language Support: Supports a wide range of popular languages, including English, Spanish, French, German, Chinese, and many more.

## Prerequisites
To run this application, you need to have Python installed on your system. You also need to install the required libraries.

Open your terminal or command prompt and run the following commands:

```` pip install requests````
 ````pip install pyttsx3 ````

# Setup and Running the Application

Obtain a Gemini API Key:
Go to the Google AI Studio and sign in with your Google account. You can generate a free API key there.

# Add Your API Key to the Script:

Open the translator_app.py file. Find the GEMINI_API_KEY variable at the top of the script:


``GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")``

Replace "YOUR_API_KEY_HERE" with the key you generated. For example:

``GEMINI_API_KEY = "AIzaSyC_XXXXXXXXXXXXXXXXXXXX"``

# Run the Application:
Navigate to the project directory in your terminal and execute the script:

```language_translator.py```

## Usage
* Enter Text: Type or paste the text you wish to translate into the upper text box.

* Select Languages: Choose your source and target languages from the dropdown menus.

* Translate: Click the "Translate" button. The translated text will appear in the lower text box.

* Speak: Click the "Speak" button to hear the translated text spoken aloud.

* Copy: Click the "Copy" button to copy the translated text to your clipboard.
