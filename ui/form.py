import time
from tkinter import *
from tkinter import messagebox

import requests
from marshmallow import ValidationError
from simplejson import JSONDecodeError

from db_connection.db_connection_manager import DBConnectionManager
from db_connection.token_generator import get_token
from pc_configuration.collect import PCConfiguration


class UIForm:
    __DB_CONNECTION_MANAGER = DBConnectionManager()

    def __init__(self):
        self.window = Tk()
        self.window.title('PCCWidget')
        self.window.geometry('250x120')
        self.window.resizable(width=False, height=False)

        self.label = Entry(self.window, state='readonly')
        self.label.pack()

        self.button = Button(self.window, text='Connect', command=self.connection)
        self.button.pack()

        try:
            self.token = get_token()
        except (requests.exceptions.RequestException, ValidationError, JSONDecodeError) as exception:
            self.token = None
            messagebox.showerror(title='Error', message='Error while creating token. Try again later!')
            exit()

    def show(self):
        self.window.mainloop()

    def connection(self):
        try:
            configuration_object = PCConfiguration(self.token)
            self.__DB_CONNECTION_MANAGER.create(configuration_object.config)
        except (requests.exceptions.RequestException, ValidationError, JSONDecodeError) as exception:
            messagebox.showerror(title='Error',
                                 message='Error while pushing your configuration token on site. '
                                         'Check your internet connection or try again later!')
            exit()

        self.label.configure(state='normal')
        self.label.delete(0, END)
        self.label.insert(0, self.token)
        self.label.configure(state='readonly')
