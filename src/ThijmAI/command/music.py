import os
import yt_dlp
import pygame
import time
import sys
from dotenv import load_dotenv

load_dotenv()

FFMPEG_PATH = os.getenv("FFMPEG_PATH")

if not FFMPEG_PATH:
    print("❌ Error: FFMPEG_PATH is not set in the .env file.")
    exit(1)

def suppress_pygame_init():

    old_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    pygame.mixer.init()
    sys.stdout = old_stdout

suppress_pygame_init()

def play_mp3(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    print("🎧 Now playing...")

    while pygame.mixer.music.get_busy():
        time.sleep(0.5)

def play_song(song_name):
    print(f"🔍 Searching for: {song_name}")

    music_folder = os.path.join(os.getcwd(), "music")
    if not os.path.exists(music_folder):
        os.makedirs(music_folder)

    song_filename = f"{song_name.replace(' ', '_')}"
    song_path = os.path.join(music_folder, song_filename)

    song_playpath = f"{song_path}.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': song_path,
        'ffmpeg_location': FFMPEG_PATH,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{song_name}"])
    except Exception as e:
        print(f"❌ Failed to download song: {e}")
        return

    print(f"✅ Downloaded! Saving as {song_filename} in './music' folder... Starting playback...")
    play_mp3(song_playpath)

if __name__ == "__main__":
    while True:

        song = input("Enter the name of the song you want to play (or type 'exit' to quit): ")

        if song.lower() == 'exit':
            print("Goodbye!")
            break

        play_song(song)