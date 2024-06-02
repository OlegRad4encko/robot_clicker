import tkinter as tk
from tkinter import ttk
from multiprocessing import Process, Queue
import time
import sys
import json


class TransparentWindow(tk.Tk):
    def __init__(self, queue_profile):
        super().__init__()
        self.queue_profile = queue_profile

        self.settings = {}
        with open('config.json', 'r') as file:
            self.settings = json.load(file)

        # Настройки окна
        self.title("Полупрозрачное окно")
        self.geometry(f'250x200+{self.settings["start_gui_position"]["x"]}+{self.settings["start_gui_position"]["y"]}')
        self.attributes("-alpha", 0.8)  # Устанавливаем прозрачность
        self.configure(bg='#000000')
        self.attributes('-topmost', True)  # Окно всегда поверх других окон
        self.overrideredirect(True)  # Убираем заголовок окна

        self.text1 = tk.Label(self, text="Rest", fg="red", bg=self["bg"], font=("Helvetica", 20))
        self.text1.pack(pady=10)

        self.text2 = tk.Label(self, text="Profile: None", fg="white", bg=self["bg"], font=("Helvetica", 15))
        self.text2.pack(pady=10)

        self.text3 = tk.Label(self, text="Action: -", fg="white", bg=self["bg"], font=("Helvetica", 15))
        self.text3.pack(pady=10)

        # # Перетаскивание окна
        self.bind("<B1-Motion>", self.do_move)
        self.bind("<ButtonPress-1>", self.start_move)

        self.update_idletasks()  # Обновить все геометрии
        if self.text1.cget('text') == 'Rest':
            self.geometry(f"{self.winfo_reqwidth() + 100}x{self.winfo_reqheight()}")
        else:
            self.geometry(f"650x{self.winfo_reqheight()}")

        # Проверка очереди
        self.after(10, self.check_queue)

    def do_move(self, event):
        x = self.winfo_pointerx() - self.x
        y = self.winfo_pointery() - self.y
        self.geometry(f"+{x}+{y}")

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def set_text1(self, text):
        self.update_idletasks()  # Обновить все геометрии)
        if text['work'] == 0:
           self.text1.config(fg="red")
           self.text1.config(text="Rest")
           self.geometry(f"{self.winfo_reqwidth() + 100}x{self.winfo_reqheight()}")
        else:
           self.text1.config(fg="green")
           self.text1.config(text="Work")
           self.geometry(f"650x{self.winfo_reqheight()}")



    def set_text2(self, text):
        new_text = "Profile: "+text['profile']
        self.text2.config(text=new_text)
        self.update_idletasks()  # Обновить все геометрии
        if self.text1.cget('text') == 'Rest':
            self.geometry(f"{self.winfo_reqwidth() + 100}x{self.winfo_reqheight()}")
        else:
            self.geometry(f"650x{self.winfo_reqheight()}")

    def set_text3(self, text):
        new_text = "Action: "+text['action']
        self.text3.config(text=new_text)
        self.update_idletasks()  # Обновить все геометрии

        if self.text1.cget('text') == 'Rest':
            self.geometry(f"{self.winfo_reqwidth() + 100}x{self.winfo_reqheight()}")
        else:
            self.geometry(f"650x{self.winfo_reqheight()}")

    def check_queue(self):
        while not self.queue_profile.empty():
            message = self.queue_profile.get()
            if 'work' in message:
                self.set_text1(message)
            if 'profile' in message:
                self.set_text2(message)
            if 'action' in message:
                self.set_text3(message)
            if 'shutdown' in message:
                sys.exit()

        self.after(10, self.check_queue)



def start_gui(queue_profile):
    app = TransparentWindow(queue_profile)
    app.mainloop()
