from tkinter import *
from tkinter import messagebox

import requests
from marshmallow import ValidationError

from db_connection.token_generator import get_token


class UIForm:
    def __init__(self):

        try:
            self.token = get_token()
        except (requests.exceptions.RequestException, ValidationError) as exception:
            self.token = None
            messagebox.showerror(title='error', message=exception)

        self.window = Tk()
        self.window.title('PCCWidget')
        self.window.geometry('250x120')
        self.window.resizable(width=False, height=False)

        self.label = Entry(self.window, state='readonly')
        self.label.pack()

        self.button = Button(self.window, text='Connect', command=self.connection)
        self.button.pack()

    def show(self):
        self.window.mainloop()

    def connection(self):


        self.label.configure(state='normal')
        self.label.delete(0, END)
        self.label.insert(0, self.token)
        self.label.configure(state='readonly')
