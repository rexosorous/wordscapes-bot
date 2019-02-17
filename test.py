from pynput.keyboard import Key, Listener
import threading
import os

def stop(key):
    if key == Key.esc:
        print('hello')
        os._exit(1)


def listen():
    with Listener(on_press=stop) as listener:
        listener.join()

listen_thread = threading.Thread(target=listen)
listen_thread.daemon = True
listen_thread.start()

while(True):
    print('a')