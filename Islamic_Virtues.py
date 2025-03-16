import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk
import requests
import pyttsx3
from pygame import mixer
import os

# Initialize audio
engine = pyttsx3.init()
mixer.init()

# Global variables
reveal_count = 0
current_word_list = []
entry = None
current_theme = "dark"
animation_enabled = True
sidebar = None
main_frame = None
content_area = None
content_canvas = None
entry_frame = None
title_label = None

# Static fallback Islamic words and meanings
fallback_islamic_words = [
    "Salam", "Rahma", "Barakah", "Taqwa", "Iman", 
    "Sabr", "Jannah", "Dua", "Zakat", "Hidayah"
]
fallback_meanings = {
    "Salam": "Peace",
    "Rahma": "Mercy",
    "Barakah": "Blessing",
    "Taqwa": "God-consciousness",
    "Iman": "Faith",
    "Sabr": "Patience",
    "Jannah": "Paradise",
    "Dua": "Supplication",
    "Zakat": "Charity",
    "Hidayah": "Guidance"
}
superpowers = ["Flight", "Invisibility", "Super Strength", "Telekinesis", "Speed"]
traits = {
    "Salam": "Calm",
    "Rahma": "Compassionate",
    "Barakah": "Prosperous",
    "Taqwa": "Pious",
    "Iman": "Steadfast",
    "Sabr": "Resilient",
    "Jannah": "Hopeful",
    "Dua": "Prayerful",
    "Zakat": "Generous",
    "Hidayah": "Wise"
}

def fetch_online_words():
    url = "https://api.example.com/islamic-words"  # Replace with real API
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            words = [word.strip().capitalize() for word in response.text.splitlines()]
            return words if words else fallback_islamic_words
        return fallback_islamic_words
    except requests.RequestException as e:
        print(f"Failed to fetch online words: {e}. Using fallback.")
        return fallback_islamic_words

def get_word_meaning(word):
    url = f"https://en.wiktionary.org/w/api.php?action=query&titles={word}&prop=extracts&exintro&explaintext&format=json"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        pages = data["query"]["pages"]
        page_id = next(iter(pages))
        if page_id != "-1" and "extract" in pages[page_id]:
            meaning = pages[page_id]["extract"].split(".")[0]
            return meaning.strip()
        return fallback_meanings.get(word.capitalize(), "Meaning not available")
    except requests.RequestException as e:
        print(f"Failed to fetch meaning for '{word}': {e}. Using fallback.")
        return fallback_meanings.get(word.capitalize(), "Meaning not available")

def add_custom_word():
    global current_word_list
    if entry and entry.winfo_ismapped():
        new_word = entry.get().capitalize()
        if new_word:
            current_word_list.append(new_word)
            meaning = get_word_meaning(new_word)
            entry.delete(0, tk.END)
            play_sound("click")
            scroll_text(f"Added: {new_word}\nMeaning: {meaning}")

def adjust_entry_size(event):
    if entry and entry.winfo_ismapped():
        text_length = len(entry.get())
        entry.config(width=max(25, text_length + 2))

def play_sound(effect="pow"):
    try:
        mixer.Sound(f"{effect}.wav").play()
    except:
        pass

def toggle_animation():
    global animation_enabled
    animation_enabled = not animation_enabled
    status = "enabled" if animation_enabled else "disabled"
    scroll_text(f"Animation {status}")

def switch_theme():
    global current_theme
    if not sidebar:
        return
    if current_theme == "dark":
        current_theme = "neon"
        sidebar.config(bg="#ff00ff")
        main_frame.config(bg="#0f0f0f")
        content_area.config(bg="#0f0f0f")
        content_canvas.config(bg="#0f0f0f")
        entry_frame.config(bg="#0f0f0f")
        title_label.config(bg="#ff00ff", fg="#00ff00")
    else:
        current_theme = "dark"
        sidebar.config(bg="#1e2a38")
        main_frame.config(bg="#15202b")
        content_area.config(bg="#15202b")
        content_canvas.config(bg="#15202b")
        entry_frame.config(bg="#15202b")
        title_label.config(bg="#1e2a38", fg="#1da1f2")
    scroll_text(f"Switched to {current_theme} theme")

def show_quran_verse():
    try:
        verse_num = random.randint(1, 6236)
        response = requests.get(f"http://api.quran.com/api/v4/verses/by_key/{verse_num}?language=en&words=false&translations=131")
        data = response.json()
        verse = data["verse"]
        arabic_text = verse["text_uthmani"]
        english_text = verse["translations"][0]["text"]
        reference = verse["verse_key"]
        display_text = f"{reference}\nArabic: {arabic_text}\nEnglish: {english_text}"
        scroll_text(display_text)
    except Exception as e:
        scroll_text(f"Error fetching verse: {e}")

def show_result():
    global reveal_count
    name = entry.get()
    if not name:
        return
    assigned_word = random.choice(current_word_list)
    power = random.choice(superpowers)
    trait = traits.get(assigned_word, "Mysterious")
    result_text = f"{name}, You Are {assigned_word} with {power}!\nTrait: {trait}"
    reveal_count += 1
    glitch_text(result_text)
    play_sound("pow")

def show_stats():
    content_canvas.delete("content_text")
    stats_text = f"Reveals: {reveal_count}\nWords: {len(current_word_list)}"
    scroll_text(stats_text)

def show_help():
    help_text = (
        "Welcome to Islamic Virtues!\n\n"
        "Instructions:\n"
        "1. Add custom Islamic words using the entry field.\n"
        "2. Click 'Show Result' to reveal your assigned word, superpower, and trait.\n"
        "3. Use 'Toggle Animation' to enable or disable animations.\n"
        "4. Switch between dark and neon themes using the 'Switch Theme' button.\n"
        "5. Click 'Show Quran Verse' to display a random verse from the Quran.\n"
        "6. View stats by clicking 'Show Stats'.\n"
    )
    scroll_text(help_text)

# Initialize the main Tkinter window
root = tk.Tk()

# Define the scroll_text function
def scroll_text(text):
    content_canvas.delete("content_text")
    content_canvas.create_text(10, 10, anchor="nw", text=text, fill="white", font=("Segoe UI", 12), tags="content_text")
    content_canvas.config(scrollregion=content_canvas.bbox("all"))

# Define the glitch_text function
def glitch_text(text):
    # Simple implementation of glitch effect
    content_canvas.delete("content_text")
    for i in range(3):
        x_offset = random.randint(-5, 5)
        y_offset = random.randint(-5, 5)
        content_canvas.create_text(10 + x_offset, 10 + y_offset, anchor="nw", text=text, fill="red", font=("Segoe UI", 12), tags="content_text")
    content_canvas.config(scrollregion=content_canvas.bbox("all"))

# Add a button to show help
help_button = tk.Button(sidebar, text="Help", command=show_help, bg="#1e2a38", fg="#1da1f2")
help_button.pack(pady=(10, 10), padx=10, anchor="n")

# Add a button to toggle animation
toggle_animation_button = tk.Button(sidebar, text="Toggle Animation", command=toggle_animation, bg="#1e2a38", fg="#1da1f2")
toggle_animation_button.pack(pady=(10, 10), padx=10, anchor="n")

# Update program name and UI for Islamic theme
title_label = tk.Label(sidebar, text="Islamic Virtues", font=("Segoe UI", 16, "bold"), bg="#1e2a38", fg="#1da1f2")
title_label.pack(pady=(20, 10), padx=10, anchor="n")

root.title("Islamic Virtues")

# Start the Tkinter main loop
root.mainloop()
