import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import pyttsx3

# --- Configuration ---
# You must obtain a Gemini API key from Google AI Studio.
# Store it as an environment variable or paste it directly below.
# The `requests` library is used to make API calls to the Gemini API.
# The `pyttsx3` library is used for offline text-to-speech.

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDruSM7gSK5T9j15VK2xAGWa6bharfGqV4")

# --- Language Mappings ---
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Arabic": "ar",
    "Hindi": "hi",
    "Portuguese": "pt",
    "Italian": "it",
    "Turkish": "tr",
    "Telugu": "te"
}


# --- Main Application Class ---
class TranslatorApp:
    def __init__(self,root):
        self.speak_btn = None
        self.copy_btn = None
        self.translated_text = None
        self.translate_btn = None
        self.text_input = None
        self.target_lang = None
        self.source_lang = None
        self.root = root
        self.root.title("Python Gemini Translator")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f4f8")

        self.style = ttk.Style(self.root)
        self.style.configure("TLabel", background="#f0f4f8", font=("Inter", 10))
        self.style.configure("TButton", font=("Inter", 10, "bold"))
        self.style.configure("TCombobox", font=("Inter", 10))

        self.engine = pyttsx3.init()
        self.setup_ui()

    def setup_ui(self):
        # Text input area
        ttk.Label(self.root, text="Enter text to translate:").pack(padx=10, pady=(10, 0), anchor="w")
        self.text_input = tk.Text(self.root, height=5, wrap="word", font=("Inter", 12), bd=1, relief="solid")
        self.text_input.pack(fill="x", padx=10, pady=5)

        # Language selectors
        lang_frame = ttk.Frame(self.root)
        lang_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(lang_frame, text="Source Language:").grid(row=0, column=0, sticky="w", padx=5)
        self.source_lang = ttk.Combobox(lang_frame, values=list(LANGUAGES.keys()), state="readonly")
        self.source_lang.current(list(LANGUAGES.keys()).index("English"))
        self.source_lang.grid(row=1, column=0, sticky="ew", padx=5)

        ttk.Label(lang_frame, text="Target Language:").grid(row=0, column=1, sticky="w", padx=5)
        self.target_lang = ttk.Combobox(lang_frame, values=list(LANGUAGES.keys()), state="readonly")
        self.target_lang.current(list(LANGUAGES.keys()).index("Spanish"))
        self.target_lang.grid(row=1, column=1, sticky="ew", padx=5)

        lang_frame.columnconfigure(0, weight=1)
        lang_frame.columnconfigure(1, weight=1)

        # Translate button
        self.translate_btn = ttk.Button(self.root, text="Translate", command=self.translate_text)
        self.translate_btn.pack(pady=10)

        # Translated text display
        ttk.Label(self.root, text="Translated text:").pack(padx=10, pady=(10, 0), anchor="w")
        self.translated_text = tk.Text(self.root, height=5, wrap="word", font=("Inter", 12), bd=1, relief="solid",
                                       state="disabled")
        self.translated_text.pack(fill="x", padx=10, pady=5)

        # Buttons for copy and speak
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)

        self.copy_btn = ttk.Button(btn_frame, text="Copy", command=self.copy_text)
        self.copy_btn.pack(side="left", padx=5)

        self.speak_btn = ttk.Button(btn_frame, text="Speak", command=self.speak_text)
        self.speak_btn.pack(side="left", padx=5)

    @staticmethod
    def show_message(title, message):
        messagebox.showinfo(title, message)

    def translate_text(self):
        text = self.text_input.get("1.0", "end-1c").strip()
        if not text:
            self.show_message("Input needed", "Please enter text to translate.")
            return

        source_code = LANGUAGES[self.source_lang.get()]
        target_code = LANGUAGES[self.target_lang.get()]

        if source_code == target_code:
            self.show_message("Info", "Source and target languages are the same.")
            return

        self.translate_btn.config(state="disabled")
        self.translated_text.config(state="normal")
        self.translated_text.delete("1.0", "end")
        self.translated_text.insert("1.0", "Translating...")
        self.translated_text.config(state="disabled")
        self.root.update()

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [{"parts": [{"text": text}]}],
            "systemInstruction": {
                "parts": [{
                              "text": f"You are a world-class translator. Translate the following text from {self.source_lang.get()} to {self.target_lang.get()}. Do not add any conversational text or explanations. Just provide the translated text."}]
            },
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            translated = response.json()['candidates'][0]['content']['parts'][0]['text']

            self.translated_text.config(state="normal")
            self.translated_text.delete("1.0", "end")
            self.translated_text.insert("1.0", translated)
            self.translated_text.config(state="disabled")

            self.show_message("Success", "Translation complete!")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to connect to API: {e}")
        except (KeyError, IndexError) as e:
            messagebox.showerror("Error", f"Invalid API response: {e}")
        finally:
            self.translate_btn.config(state="enabled")

    def copy_text(self):
        translated = self.translated_text.get("1.0", "end-1c").strip()
        if translated:
            self.root.clipboard_clear()
            self.root.clipboard_append(translated)
            self.show_message("Copied", "Translated text copied to clipboard!")

    def speak_text(self):
        translated = self.translated_text.get("1.0", "end-1c").strip()
        if not translated:
            self.show_message("Nothing to speak", "Please translate text first.")
            return

        try:
            self.engine.say(translated)
            self.engine.runAndWait()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to speak text: {e}")


# --- Main execution block ---
if __name__ == "__main__":
    if "YOUR_API_KEY_HERE" in GEMINI_API_KEY:
        messagebox.showwarning(
            "API Key Required",
            "Please replace 'YOUR_API_KEY_HERE' with your actual Gemini API key."
            "\n\nAlternatively, set the GEMINI_API_KEY environment variable."
        )
    else:
        root = tk.Tk()
        app = TranslatorApp(root)
        root.mainloop()
