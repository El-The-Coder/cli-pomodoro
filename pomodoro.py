import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import time
import threading
import pygame
import notify2
import signal
import sys

def play_sound(sound_path):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()

def play_start_sound():
    play_sound('/path/to/start_sound.wav') #isi pake suara buat nandain pomodoro dimulai

def play_short_break_sound():
    play_sound('/path/to/short_break_sound.wav') #isi pake suara buat nandain istirahat pendek dimulai

def play_long_break_sound():
    play_sound('/path/to/long_break_sound.wav') #isi pake suara buat nandain istirahat panjang dimulai

def play_finish_sound():
    play_sound('/path/to/finish_sound.wav') #isi pake suara buat nandain pomodoro selesai

def show_notification(title, message):
    notify2.init("Pomodoro")
    notification = notify2.Notification(title, message)
    notification.show()

def pomodoro_timer(duration, remaining_pomodoros):
    start_time = time.time()
    end_time = start_time + duration
    print("Pomodoro dimulai!")
    try:
        while time.time() < end_time:
            remaining_time = end_time - time.time()
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            print(f"Sisa waktu: {minutes:02d}:{seconds:02d} - Pomodoro tersisa: {remaining_pomodoros}", end='\r')
            time.sleep(1)
        print("\n\nPomodoro selesai!")
        remaining_pomodoros -= 1
        if remaining_pomodoros > 0:
            play_finish_sound()
            show_notification("Pomodoro Selesai!", f"Waktunya istirahat! Pomodoro tersisa: {remaining_pomodoros}")
        else:
            play_finish_sound()
            show_notification("Pomodoro Selesai!", "Semua pomodoro selesai!")
    except KeyboardInterrupt:
        print("\n\nPomodoro dihentikan!")

def break_timer(duration):
    start_time = time.time()
    end_time = start_time + duration
    print("Istirahat dimulai!")
    try:
        while time.time() < end_time:
            remaining_time = end_time - time.time()
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            print(f"Sisa waktu: {minutes:02d}:{seconds:02d}", end='\r')
            time.sleep(1)
        print("\n\nIstirahat selesai!")
        play_short_break_sound()
        show_notification("Istirahat Selesai!", "Mulai Pomodoro berikutnya!")
    except KeyboardInterrupt:
        print("\n\nIstirahat dihentikan!")

def long_break_timer(duration):
    start_time = time.time()
    end_time = start_time + duration
    print("Istirahat panjang dimulai!")
    try:
        while time.time() < end_time:
            remaining_time = end_time - time.time()
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            print(f"Sisa waktu: {minutes:02d}:{seconds:02d}", end='\r')
            time.sleep(1)
        print("\n\nIstirahat panjang selesai!")
        play_long_break_sound()
        show_notification("Istirahat Panjang Selesai!", "Mulai Pomodoro berikutnya!")
    except KeyboardInterrupt:
        print("\n\nIstirahat panjang dihentikan!")

def start_pomodoro():
    activity = input("Masukkan aktivitas: ")
    pomodoro_count = int(input("Berapa kali pomodoro akan dilakukan? "))
    pomodoro_duration = 25 * 60
    short_break_duration = 5 * 60
    long_break_duration = 20 * 60
    remaining_pomodoros = pomodoro_count

    while remaining_pomodoros > 0:
        pomodoro_thread = threading.Thread(target=pomodoro_timer, args=(pomodoro_duration, remaining_pomodoros))
        pomodoro_thread.start()
        pomodoro_thread.join()

        remaining_pomodoros -= 1

        if remaining_pomodoros % 4 == 0 and remaining_pomodoros > 0:
            break_thread = threading.Thread(target=long_break_timer, args=(long_break_duration,))
            break_thread.start()
            break_thread.join()
        else:
            break_thread = threading.Thread(target=break_timer, args=(short_break_duration,))
            break_thread.start()
            break_thread.join()

    print("\n\nSemua pomodoro selesai!")
    show_notification("Pomodoro Selesai!", f"Semua {pomodoro_count} pomodoro selesai untuk aktivitas: {activity}")

def signal_handler(signal, frame):
    print("\n\nPomodoro dihentikan!")
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    play_start_sound()
    start_pomodoro()
