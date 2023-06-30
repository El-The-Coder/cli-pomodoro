import time
import threading
import pyglet
import notify2
import signal
import sys


def play_alarm():
    # Load an alarm sound file (change the path to your own sound file)
    sound = pyglet.media.load('/path/to/alarm_sound.wav')
    sound.play()

def show_notification(title, message):
    notify2.init("Pomodoro")
    notification = notify2.Notification(title, message)
    notification.show()

def pomodoro_timer(duration):
    start_time = time.time()
    end_time = start_time + duration
    print("Pomodoro started!")
    try:
        while time.time() < end_time:
            remaining_time = end_time - time.time()
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            print(f"Time remaining: {minutes:02d}:{seconds:02d}", end='\r')
            time.sleep(1)
        print("\n\nPomodoro finished!")
        play_alarm()
        show_notification("Pomodoro Finished!", "Take a break!")
    except KeyboardInterrupt:
        print("\n\nPomodoro interrupted!")

def break_timer(duration):
    start_time = time.time()
    end_time = start_time + duration
    print("Break started!")
    try:
        while time.time() < end_time:
            remaining_time = end_time - time.time()
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            print(f"Time remaining: {minutes:02d}:{seconds:02d}", end='\r')
            time.sleep(1)
        print("\n\nBreak finished!")
        play_alarm()
        show_notification("Break Finished!", "Start another Pomodoro!")
    except KeyboardInterrupt:
        print("\n\nBreak interrupted!")

def start_pomodoro():
    pomodoro_duration = 25 * 60  # 25 minutes in seconds
    short_break_duration = 5 * 60  # 5 minutes in seconds
    long_break_duration = 20 * 60  # 20 minutes in seconds

    pomodoros_completed = 0

    while True:
        pomodoro_thread = threading.Thread(target=pomodoro_timer, args=(pomodoro_duration,))
        break_duration = long_break_duration if pomodoros_completed % 5 == 0 else short_break_duration
        break_thread = threading.Thread(target=break_timer, args=(break_duration,))

        pomodoro_thread.start()
        pomodoro_thread.join()

        break_thread.start()
        break_thread.join()

        pomodoros_completed += 1

def signal_handler(signal, frame):
    print("\n\nPomodoro stopped!")
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    start_pomodoro()
