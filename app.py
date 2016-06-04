#coding: utf-8
# -*- encoding: utf-8 -*-



'''
(u"アカウント(&A)->サインイン(&l)...")
GetProperties()
install pywinauto win32api PIL pillow pytesseract Flask pc( Tesseract-OCR->path)

'''
from pywinauto import application,findwindows
from PIL import ImageGrab, Image, ImageFilter
from flask import Flask, jsonify, redirect, session, request
import threading, time,pytesseract,tesseract
#from keyEvent import KeyEvent
import win32api, win32con



SYSTEM_WIDTH = win32api.GetSystemMetrics(0)                    #システム解像度width

SYSTEM_HEIGHT = win32api.GetSystemMetrics(1)                   #システム解像度height

RESTART_NUM = 2                                               #処理失敗のとき再起動する回数

ITUNES_DIRECTORY = "C:\Program Files\iTunes\iTunes.exe"  #itunesディレクトリ


CODE_CASE = {
    "must enter a": "You must enter a valid code.",
    "The code entered": "The code enter is not valid",
    "ms may VS no ‘anger ma": "This offer is no longer valid",
    "Austrahan stureﬁrunt": "The code must be redeemed in the Australian strorefront"
}

ERROR_CASE = [
    'Redeem code page time out',
    'get code time out'
]

APP = application.Application()                                #appコントローラー

flask = Flask(__name__)                                        #Flaskサーバー

def click(x,y):
    '''
    指定x,yでクリック操作をする
    '''
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)


def keyEventWithCtrl(key):
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    win32api.keybd_event(ord(key), 0, win32con.KEYEVENTF_EXTENDEDKEY | 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(ord(key), 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)


def keyEventWithAlt(key):
    win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
    win32api.keybd_event(ord(key), 0, win32con.KEYEVENTF_EXTENDEDKEY | 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(ord(key), 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)


def keyEvent(key):
    if isinstance(key,(int)):
        cord=key
        win32api.keybd_event(cord, 0, 0, 0)
        time.sleep(0.05)
        win32api.keybd_event(cord, 0, win32con.KEYEVENTF_KEYUP, 0)
    else:
        cord=ord(c)
        win32api.keybd_event(cord, 0, win32con.KEYEVENTF_EXTENDEDKEY | 0, 0)
        time.sleep(0.05)
        win32api.keybd_event(cord, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)



def startItunes(data):
    try:
        result = None
        APP.Start(ITUNES_DIRECTORY)

        iTunes = APP.window_(title_re='iTunes',  class_name="iTunes")
        # ウィドーズを最大化表示させる

        time.sleep(1)
        iTunes.TypeKeys('%A')
        iTunes.TypeKeys('%A')
        time.sleep(1)
        iTunes.TypeKeys('{UP}')
        iTunes.TypeKeys('{ENTER}')

        login(data)

        time.sleep(2)
        iTunes.TypeKeys('%{SPACE}')
        iTunes.TypeKeys('X')
        # チャージ画面が読み終わるまで、一秒ごとにスクリーンショートをとる
        redeem_page_string = ""
        box=(SYSTEM_WIDTH/4,SYSTEM_HEIGHT/10.2857,SYSTEM_WIDTH/2.7428,SYSTEM_HEIGHT/6.5454)
        counter = 0
        while redeem_page_string != "Redeem Code":
            if counter >= 20:
                logOut()
                raise Exception("Redeem code page time out")

            redeem_page_string = imageToString(getScreenShort(box=box,image_name="redeem_page.png"))
            counter += 1

        click(int(SYSTEM_WIDTH/2.1),int(SYSTEM_HEIGHT/1.7))
        iTunes.TypeKeys(data['redeem_code'])
        iTunes.TypeKeys('{ENTER}')

        image_string = ""
        counter = 0
        while image_string == "":
            if counter >= 10:
                logOut()
                raise Exception("get code time out")
            image_string = imageToString(getScreenShort())
            counter += 1

        for str in CODE_CASE:
            if str in image_string:
                result = CODE_CASE[str]
        logOut()
        return result
    except Exception, e:
        print e.message
        APP.Kill_()
        for err in ERROR_CASE:

            if e.message == err and data['restart_num'] > 0:
                time.sleep(0.2)
                data['restart_num'] -= 1
                print "auto restart after 2 second..."
                time.sleep(2)
                startItunes(data)

        if e.message == "":
            return "login failed"
        return e.message

def getScreenShort(box=None, image_name=None):
    #スクリーンショートの場所指定
    if box is None:
        left = SYSTEM_WIDTH/2.49      #1920/2-190
        right = SYSTEM_WIDTH/1.9      #1920/2
        top = SYSTEM_HEIGHT/1.63636   #1080/2+120
        buttom = SYSTEM_HEIGHT/1.508  #1080/2+160
        time.sleep(0.5)
        box = (left,top,right,buttom)

    if image_name is None:
        image = "screen_capture.png"
    else:
        image = image_name

    ImageGrab.grab().crop(box).save(image, "PNG", quality=95)
    return image


def imageToString(image_name):
    '''
    get the image conver to string
    and return convered string
    '''
    time.sleep(1)
    image = Image.open(image_name)
    return pytesseract.image_to_string(image, lang="eng")


def login(data):
    #５回ログイン失敗したら処理を中止する
    login_count = 0
    while True:
        if login_count >= 5:
            logOut()
            raise Exception("login failed")

        try:
            #login failed窓口が現すと中止する
            handles = findwindows.find_windows(title_re='Verification Failed', class_name="#32770")
            if len(handles) > 0:
                raise Exception("Incorrect username or password")

            handles = findwindows.find_windows(title_re='iTunes', class_name="#32770")
            if len(handles) > 0:
                #Edit user,Edit2 password
                login_form = APP.window_(title_re='iTunes',  class_name="#32770")
                login_form['Edit'].SetText(data['apple_id'])
                login_form['Edit2'].SetText(data['password'])
                login_form['Edit'].SetText(data['apple_id'])
                login_form['Edit2'].SetText(data['password'])
                login_form['Button'].Click()
                keyEvent(win32con.VK_RETURN)
                return True
            else:
                time.sleep(2)
                login_count += 1
        except:
            login_count += 1
            time.sleep(2)


def logOut():
    iTunes = APP.window_(title_re='iTunes',  class_name="iTunes")
    iTunes.TypeKeys('%A')
    time.sleep(1)
    iTunes.TypeKeys('{DOWN}')
    iTunes.TypeKeys('{DOWN}')
    iTunes.TypeKeys('{DOWN}')
    iTunes.TypeKeys('{DOWN}')
    iTunes.TypeKeys('{ENTER}')
    time.sleep(1)
    APP.Kill_()

@flask.route("/", methods=['GET', 'POST'])
def main():

    result = None
    apple_id = request.args.get('apple_id')
    if apple_id == "":
        return jsonify(ResultSet=result)
    password = request.args.get('password')
    if password == "":
        return jsonify(ResultSet=result)
    redeem_code = request.args.get('redeem_code')
    if redeem_code == "":
        return jsonify(ResultSet=result)

    if (apple_id is not None and
        password is not None and
        redeem_code is not None):
        data = {
        'apple_id': apple_id,
        'password': password,
        'redeem_code': redeem_code,
        'restart_num': RESTART_NUM
        }

        return jsonify(ResultSet=startItunes(data))
    else:
        return jsonify(ResultSet=result)


# def onTopAlways():
#     while True:
#         time.sleep(1)
#         APP.Start(ITUNES_DIRECTORY)


if __name__ == "__main__":
    # data = {
    #     'apple_id': "314788851@qq.com",
    #     'password': "Wh147258369",
    #     'redeem_code': "12345679999",
    #     'restart_num': RESTART_NUM
    #     }
    # threads = []
    # start_iTunes = threading.Thread(target=startItunes(data))
    # threads.append(start_iTunes)
    # start_iTunes.start()

    #print imageToString(getScreenShort(image_name="screen_capture.png"))
    flask.config['DEBUG'] = True
    flask.run(host='0.0.0.0', port=80)
