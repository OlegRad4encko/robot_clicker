import logging
from trayMenu import start_tray
from multiprocessing import Process, freeze_support, Queue
from gui import start_gui

logging.basicConfig(
    filename='error_log.log',  # Имя файла для записи логов
    level=logging.ERROR,  # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат записи логов
)

freeze_support()


def main():
    queue = Queue()
    tray_process: Process = Process(target=start_tray, args=(queue,))
    tray_process.start()

    gui_process: Process = Process(target=start_gui, args=(queue,))
    gui_process.start()

    tray_process.join()
    gui_process.join()


if __name__ == '__main__':
    main()



# pyinstaller --hidden-import tkinter --onefile --noconsole  main.py
