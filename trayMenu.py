from PIL import Image
from pystray import Icon, Menu, MenuItem
from multiprocessing import Process, Queue
import logging
import os
import sys
from functools import partial
from tapper_profiles_execude import custom_profile
import json
import time

logging.basicConfig(
    filename='error_log.log',  # Имя файла для записи логов
    level=logging.ERROR,  # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат записи логов
)


def get_custom_profiles():
    folder_path = 'user_profiles'
    file_prefix = 'CP_'
    file_names = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)) and file_name.startswith(file_prefix):
            file_names.append(file_name)

    return file_names


def get_menu_items(names, tray):
    menu_items = []
    for name in names:
        menu_items.append(MenuItem(
            "{}".format(name.split('.txt')[0]), partial(tray.custom_profile_execute, name)
        ))
    return menu_items


class TrayMenu:
    def __init__(self, queue):
        self.queue = queue
        self.tapper_processes = {}
        self.config = {}

        custom_profiles_names = get_custom_profiles()
        menu_items = get_menu_items(custom_profiles_names, self)
        menu_items.append(MenuItem('Quit', self.on_quit))

        for item in custom_profiles_names:
            self.tapper_processes[str(item.split('.txt')[0])] = None

        self.image = Image.open("icon.png")
        self.menu = Menu(*menu_items)
        self.icon = Icon("name", self.image, menu=self.menu)

        self.start_with_tray()

    def terminate_all(self):
        for process in self.tapper_processes:
            if self.tapper_processes[process] is not None:
                self.terminate_process(process)
        time.sleep(0.1)
        self.queue.put({"work": 0})
        time.sleep(0.1)
        self.queue.put({"profile": "None"})
        time.sleep(0.1)
        self.queue.put({"action": "-"})

    def terminate_process(self, process):
        self.tapper_processes[process].terminate()
        self.tapper_processes[process].join()
        self.tapper_processes[process] = None
        time.sleep(0.1)
        self.queue.put({"work": 0})
        time.sleep(0.1)
        self.queue.put({"profile": "None"})
        time.sleep(0.1)
        self.queue.put({"action": "-"})

    def start_process(self, process, profile):
        time.sleep(0.1)
        self.queue.put({"work": 1})
        self.tapper_processes[process] = Process(target=custom_profile, kwargs={"profile": profile, "queue": self.queue})
        self.tapper_processes[process].start()

    def on_quit(self, icon):
        self.icon.stop()
        self.terminate_all()

        self.queue.put({"shutdown": 1})

        sys.exit()

    def run(self):
        self.icon.run()

    def custom_profile_execute(self, one, two, three):
        if self.tapper_processes[str(three)] is not None and not self.tapper_processes[str(three)].is_alive():
            self.tapper_processes[str(three)] = None

        if self.tapper_processes[str(three)] is not None:
            self.terminate_all()
            return 0

        if self.tapper_processes[str(three)] is None:
            self.start_process(str(three), str(one))


    def start_with_tray(self):
        with open('config.json', 'r') as file:
            self.config = json.load(file)

        if self.config['auto_start_profile'] != "0":
            self.queue.put({"work": 1})
            self.start_process(
                str(self.config['auto_start_profile'].split('.txt')[0]),
                self.config['auto_start_profile']
            )


def start_tray(queue_profile):
    tray = TrayMenu(queue_profile)
    tray.run()
