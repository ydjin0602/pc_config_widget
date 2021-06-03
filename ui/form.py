import threading
import time
from tkinter import *
from tkinter import messagebox

import requests
from marshmallow import ValidationError
from json import JSONDecodeError

from db_connection.db_connection_manager import DBConnectionManager
from db_connection.token_generator import get_token
from pc_configuration.collect import PCConfiguration

DB_CONNECTION_MANAGER = DBConnectionManager()


class UIForm(Tk):

    def __init__(self):
        super().__init__()
        self.title('PCCWidget')
        self.geometry('250x120')
        self.resizable(width=False, height=False)
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        self.label = Entry(self, state='readonly')
        self.label.pack(expand=1)

        self.button = Button(self, text='Connect', command=self.connection)
        self.button.pack(expand=1)

        try:
            self.token = get_token()
        except (requests.exceptions.RequestException, ValidationError, JSONDecodeError) as exception:
            self.token = None
            messagebox.showerror(title='Error', message='Error while creating token. Try again later!')
            self.destroy()

        self.configuration_object = PCConfiguration(self.token)
        self.thread = threading.Thread(target=self.update_config_process)
        self.thread.daemon = True

    def show(self):
        self.mainloop()

    def on_closing(self):
        if messagebox.askokcancel('Quit', 'Do you want to quit?'):
            self.destroy()
            sys.exit()

    def connection(self):
        self.button.config(state='disabled')
        try:
            DB_CONNECTION_MANAGER.create(self.configuration_object.config)
            self.label.configure(state='normal')
            self.label.delete(0, END)
            self.label.insert(0, self.token)
            self.label.configure(state='readonly')

            self.thread.start()
        except (requests.exceptions.RequestException, ValidationError, JSONDecodeError) as exception:
            messagebox.showerror(title='Error',
                                 message='Error while pushing your configuration on site. '
                                         'Check your internet connection or try again later!')
            self.destroy()

    def update_config_process(self):
        while True:
            self.configuration_object.update()
            try:
                DB_CONNECTION_MANAGER.update(self.configuration_object.config)
                time.sleep(5)
            except (requests.exceptions.RequestException, ValidationError, JSONDecodeError) as exception:
                messagebox.showerror(title='Error',
                                     message='Error while updating your configuration on site. '
                                             'Check your internet connection or try again later!')
                self.destroy()
