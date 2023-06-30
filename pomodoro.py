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
    print("Pomodoro started!")
    try:
        time.sleep(duration)
        print("Pomodoro finished!")
        play_alarm()
        show_notification("Pomodoro Finished!", "Take a break!")
    except KeyboardInterrupt:
        print("Pomodoro interrupted!")

def break_timer(duration):
    print("Break started!")
    try:
        time.sleep(duration)
        print("Break finished!")
        play_alarm()
        show_notification("Break Finished!", "Start another Pomodoro!")
    except KeyboardInterrupt:
        print("Break interrupted!")

def start_pomodoro():
    pomodoro_duration = 25 * 60  # 25 minutes in seconds
    break_duration = 5 * 60  # 5 minutes in seconds

    pomodoro_thread = threading.Thread(target=pomodoro_timer, args=(pomodoro_duration,))
    break_thread = threading.Thread(target=break_timer, args=(break_duration,))

    pomodoro_thread.start()
    pomodoro_thread.join()

    break_thread.start()
    break_thread.join()

    start_pomodoro()

def signal_handler(signal, frame):
    print("Pomodoro stopped!")
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    start_pomodoro()
