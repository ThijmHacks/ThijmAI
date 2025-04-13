import os
import yt_dlp
import pygame
import time
import sys
import threading
from dotenv import load_dotenv
from queue import Queue

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

music_queue = Queue()
is_paused = False
current_song = None
playing_thread = None

def play_mp3(file_path):
    global is_paused, current_song, playing_thread, playlist_first

    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    print(f"🎧 Now playing: {file_path}")

    while pygame.mixer.music.get_busy():
        time.sleep(0.5)

    if not music_queue.empty() and not is_paused:
        next_song = music_queue.get()
        playing_thread = threading.Thread(target=play_mp3, args=(next_song,))
        playing_thread.daemon = True
        playing_thread.start()

    else:
        print("🎶 Playlist finished!")

def play_song(song_name):
    global playlist_first
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

    print(f"✅ Downloaded! Saving as {song_filename} in './music' folder...")

    music_queue.put(song_playpath)

    if not pygame.mixer.music.get_busy() and not is_paused:
        playing_thread = threading.Thread(target=play_mp3, args=(song_playpath,))
        playing_thread.daemon = True
        playing_thread.start()
        playlist_first = True

def pause_music():
    global is_paused
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        is_paused = True
        print("⏸️ Music paused.")
    else:
        print("❌ No music is playing to pause.")

def resume_music():
    global is_paused
    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
        print("▶️ Music resumed.")
    else:
        print("❌ Music is not paused.")

def stop_music():
    pygame.mixer.music.stop()
    global is_paused, playing_thread
    is_paused = False
    playing_thread = None
    print("❌ Music stopped and playlist cleared.")

    while not music_queue.empty():
        music_queue.get()

def next_song():
    global is_paused, playing_thread, playlist_first
    if pygame.mixer.music.get_busy():
        print("⏭️ Skipping to next song...")
        pygame.mixer.music.stop()
        if playlist_first:
            next_song()
            playlist_first = False
        if not music_queue.empty():
            next_song_path = music_queue.get()
            playing_thread = threading.Thread(target=play_mp3, args=(next_song_path,))
            playing_thread.daemon = True
            playing_thread.start()

        else:
            print("❌ No more songs in the queue.")
    else:
        print("❌ No song is playing to skip.")

def find_song_in_queue(song_name):
    """
    Check if the song name is partially or fully contained in any of the songs in the queue.
    """
    for song in list(music_queue.queue):
        if song_name.lower() in song.lower():
            return song
    return None

if __name__ == "__main__":
    while True:

        command = input("Enter a command (play, pause, resume, stop, next, find <song_name>, or 'exit' to quit): ").lower()

        if command == 'exit':
            print("Goodbye!")
            break

        elif command.startswith("play "):
            song_name = command[5:]
            play_song(song_name)

        elif command == 'pause':
            pause_music()

        elif command == 'resume':
            resume_music()

        elif command == 'stop':
            stop_music()

        elif command == 'next':
            next_song()

        elif command.startswith("find "):
            song_name = command[5:]
            found_song = find_song_in_queue(song_name)
            if found_song:
                print(f"✅ Found: {found_song}")
                pygame.mixer.music.load(found_song)
                pygame.mixer.music.play()
            else:
                print(f"❌ No song found containing '{song_name}'.")

        else:
            print("❌ Invalid command. Try again.")