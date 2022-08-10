import time
from watchdog.observers import Observer
from watchdog.events import FileModifiedEvent
import os


class FileModifiedEventHandler(FileModifiedEvent)
    def __init__(self, src_path, handler, args=())
        self.custom_handler = handler
        self.custom_handler_args = args
        super().__init__(src_path)

    def dispatch(self, event)
        if event.src_path == self.src_path
            self.custom_handler(self.custom_handler_args)


class FileModifiedObserver
    def __init__(self, dir_path, file_name, handler, args=())
        self.src_path = os.path.join(dir_path, file_name)
        self.dir_path = dir_path
        self.event_handler = FileModifiedEventHandler(src_path=self.src_path, handler=handler, args=args)
        self.observer = Observer()

    def start(self)
        self.observer.schedule(self.event_handler, path=self.dir_path, recursive=True)
        self.observer.start()

        try
            while True
                time.sleep(1)
        except KeyboardInterrupt
            self.observer.stop()
        self.observer.join()


