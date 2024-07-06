# import queue
import threading


def run_in_thread(function):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=function, args=args, kwargs=kwargs)
        thread.daemon=True
        thread.start()
    return wrapper