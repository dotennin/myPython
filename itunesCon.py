#coding: utf-8
# -*- encoding: utf-8 -*-
from pywinauto import findwindows, application
from PIL import ImageGrab, Image
import threading, time,pytesseract,tesseract
import win32api, win32con
class ITunes():

    def __init__(self):
        self.login_count = 0
        self.app = application.Application()
    def login(self):

        if self.login_count >= 5:
            raise Exception("login failed")
        try:
            print "helo"
            #Edit user,Edit2 password
            login_form = self.app.window_(title_re='iTunes',  class_name="#32770")
            print login_form.PrintControlIdentifiers()
            login_form['Edit'].SetText('314788851@qq.com')
            login_form['Edit2'].SetText('Wh147258369')
            login_form['Edit'].SetText('314788851@qq.com')
            login_form['Edit2'].SetText('Wh147258369')
            login_form['Button'].Click()

        except:
                self.login_count += 1
                time.sleep(2)
                return self.login()


