import numpy as nm
import cv2
import pytesseract
import time
import math
from PIL import ImageGrab
from PIL import ImageFilter
from throttle import *
import pygame
import pygame_gui
from datetime import datetime
import re
import tkinter as tk
from tkinter import simpledialog
import threading
import pydirectinput
from playsound import playsound
import gtts
import os


ATOactive = False
TTSactive = False

spd_pos = 884, 957, 947, 985
lim_pos = 889, 987, 942, 1016
green_pos = 1440, 983, 1441, 984
yellow_pos = 1438, 1016, 1439, 1017
double_yellow_pos = 1438, 950, 1439, 951
red_pos = 1438, 1045, 1439, 1046
distance_pos = 555, 1046, 605, 1070
awsbutton_pos = 1330, 994, 1331, 995
throttle_pos = 843, 931, 845, 1074
doors_pos = 870, 822, 871, 823
loading_pos = 781, 823, 782, 824
continue_pos = 1032, 460, 1033, 461
undershoot_pos = 709, 906, 710, 907
awaiting_pos = 862, 823, 863, 824
buzzer_pos = 824, 816, 825, 817

window_surface = pygame.display.set_mode((800, 200), pygame.DOUBLEBUF)
centre = (400,300)
radius = 200
speedo_max = 125


pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
time.sleep(1)
solve = None
continuing = False
ignorelim = False
ignoreaws = False

def changeColour(button,selColour):
    button.colours['normal_bg'] = pygame.Color(selColour)
    button.rebuild()

def create_dialog(title, question):
    root = tk.Tk()
    root.withdraw()
    userInput = simpledialog.askstring(title, question)
    root.destroy()
    return userInput

def forInputClick():
    threading.Thread(target=create_dialog, daemon=True).start()

def TTSNS():
    if TTSactive == True:
        tts = gtts.gTTS("Approaching Station. Train Stopping")
        tts.save('tts.mp3')
        playsound('tts.mp3')
        os.remove("tts.mp3")

def TTSRED():
    if TTSactive == True:
        tts = gtts.gTTS("ATO DISENGAGED. DANGER ASPECT AHEAD. TAKE MANUAL CONTROL")
        tts.save('tts.mp3')
        playsound('tts.mp3')
        os.remove("tts.mp3")

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("PyATO - v0.1 ALPHA")
    
    background = pygame.Surface((800,200))
    background.fill(('#000435'))

    manager = pygame_gui.UIManager((800, 600))
    clock = pygame.time.Clock()
    is_running = True

    lblMaxSpeed = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((30, 30), (200, 50)), text='PyATO - ATO for SCR', manager=manager)
    lblTime = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((220, 30), (150, 50)), text='', manager=manager)
    toggleATO_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 100), (150, 50)), text='ATO Toggle', manager=manager)
    setMaxSpeed_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 100), (150, 50)), text='Set Max Speed', manager=manager)
    toggleTTS = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((370, 100), (150, 50)), text='Toggle TTS', manager=manager)

    def task():
        curLim = 0
        global ATOactive
        global TTSactive

        while ATOactive == True:

            global solve
            global continuing
            global ignorelim
            global ignoreaws


            print("ignorelim", ignorelim)
            im = ImageGrab.grab(bbox=(awsbutton_pos))
            pix = im.load()
            awsbutton_value = pix[0, 0]  # Set the RGBA Value of the image (tuple)
            if awsbutton_value == (255, 255, 255):
                pydirectinput.keyDown("q")
                pydirectinput.keyUp("q")
                print("Reset the AWS")
            cap = ImageGrab.grab(bbox=(throttle_pos))
            img = cap
            count = 0
            bottom_throttle_pixel = None
            for y in range(img.height):
                for x in range(img.width):
                    pixel = img.getpixel((x, y))
                    if y == img.height - 1:
                        bottom_throttle_pixel = pixel
                    if pixel == (0, 176, 85):
                        count += 1

            currentThrottle = int(math.floor(100 * (count / 142)))

            print("Current throttle: ", currentThrottle)

            cap = ImageGrab.grab(bbox=(lim_pos))
            cap = cap.filter(ImageFilter.MedianFilter())
            cap = cv2.cvtColor(nm.array(cap), cv2.COLOR_RGB2GRAY)
            tesstr = pytesseract.image_to_string(
                cap,
                config="--psm 7")
            compareLim = [int(s) for s in re.findall(r'\b\d+\b', tesstr)]
            if curLim != compareLim[0]:
                playsound('sounds\change.wav')
            lim = 0
            lim = [int(s) for s in re.findall(r'\b\d+\b', tesstr)]
            curLim = int(lim[0])
            cap = ImageGrab.grab()
            src = nm.array(cap)
            gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
            gray = cv2.medianBlur(gray, 5)
            rows = gray.shape[0]
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                                    param1=100, param2=30,
                                    minRadius=1, maxRadius=30)
                    
            if circles is not None:
                circles = nm.uint16(nm.around(circles))
                for i in circles[0, :]:
                    x = i[0] - i[2]
                    y = i[1] - i[2]
                    w = 2*i[2]
                    h = 2*i[2]
                    center = (i[0], i[1])
                    if w > 39:
                        txt = pytesseract.image_to_string(gray[y:y+h, x:x+w], config="--psm 6")
                        if "W" in txt:
                            pydirectinput.keyDown("h")
                            pydirectinput.keyUp("h")
                    cv2.circle(src, center, 1, (0, 100, 100), 3)
                    radius = i[2]
                    cv2.circle(src, center, radius, (255, 0, 255), 3)

            templim = lim[0]
            lim = lim[0]
            lim = int(lim)
            if ignoreaws == False:
                    im = ImageGrab.grab(bbox=(red_pos))
                    pix = im.load()
                        # Set the RGBA Value of the image (tuple)
                    red_value = pix[0, 0]
                    im = ImageGrab.grab(bbox=(yellow_pos))
                    pix = im.load()
                        # Set the RGBA Value of the image (tuple)
                    yellow_value = pix[0, 0]
                    im = ImageGrab.grab(bbox=(green_pos))
                    pix = im.load()
                        # Set the RGBA Value of the image (tuple)
                    green_value = pix[0, 0]
                    im = ImageGrab.grab(bbox=(double_yellow_pos))
                    pix = im.load()
                        # Set the RGBA Value of the image (tuple)
                    double_yellow_value = pix[0, 0]
                    if red_value == (255, 0, 0):
                        print("AWS:", "red")
                        lim = 0
                        ATOactive = False
                        changeColour(toggleATO_btn,'#FF0000')
                        playsound('sounds\ATORedStop.wav')
                        threading.Thread(target=TTSRED, daemon=True).start()
                    if yellow_value == (255, 190, 0):
                        print("AWS:", "yellow")
                        if templim > 45:
                            lim = 45
                    if double_yellow_value == (255, 190, 0):
                        print("AWS:", "double_yellow")
                        if templim > 75:
                            lim = 75
                    if green_value == (0, 255, 0):
                        print("AWS:", "green")

            print("Limit: ", lim)
            limitThrottle = int((lim / max_speed) * 100)
            

            print("Limit throttle: ", limitThrottle)

            cap = ImageGrab.grab(bbox=(distance_pos))
            cap = cap.filter(ImageFilter.MedianFilter())
            cap = cv2.cvtColor(nm.array(cap), cv2.COLOR_RGB2GRAY)
            tesstr = pytesseract.image_to_string(
                cap,
                config="--psm 6")
            distance = 0
            distance = [int(s) for s in re.findall(r'\b\d+\b', tesstr)]
            try:
                    m_distance = distance[0]
                    distance = distance[1]
                    print(m_distance, distance)
                    if distance == 00 and m_distance == 0 or continuing == True:
                        im = ImageGrab.grab(bbox=(loading_pos))
                        pix = im.load()
                        loading_value = pix[0, 0]
                        im = ImageGrab.grab(bbox=(doors_pos))
                        pix = im.load()
                        doors_value = pix[0, 0]
                        im = ImageGrab.grab(bbox=(undershoot_pos))
                        pix = im.load()
                        undershoot_value = pix[0, 0]
                        im = ImageGrab.grab(bbox=(awaiting_pos))
                        pix = im.load()
                        awaiting_value = pix[0, 0]
                        im = ImageGrab.grab(bbox=(buzzer_pos))
                        pix = im.load()
                        buzzer_value = pix[0, 0]
                        print(buzzer_value)
                        if undershoot_value == (255, 255, 255):
                            print("UNDERSHOOT")
                            pydirectinput.keyDown("w")
                            time.sleep(0.4)
                            pydirectinput.keyUp("w")
                        if doors_value == (255, 255, 255):
                            print("CLOSING DOORS")
                            pydirectinput.keyDown("t")
                            pydirectinput.keyUp("t")
                            time.sleep(4)
                            continuing = False
                            ignorelim = False
                            ignoreaws = False
                        elif loading_value == (255, 255, 255):
                            print("LOADING")
                        elif awaiting_value == (255, 255, 255):
                            print("WAITING FOR GUARD")
                        elif buzzer_value == (255, 255, 255):
                            print("ACTIVATING THE BUZZER")
                            pydirectinput.keyDown("t")
                            pydirectinput.keyUp("t")
                        else:
                            print("ATO Stopping")
                            playsound('sounds\change.wav')
                            threading.Thread(target=TTSNS, daemon=True).start()
                            pydirectinput.keyDown("s")
                            pydirectinput.keyUp("s")
                            time.sleep(3)
                            pydirectinput.keyDown("s")
                            time.sleep(5)
                            pydirectinput.keyUp("s")
                            pydirectinput.keyDown("t")
                            pydirectinput.keyUp("t")
                    elif distance <= 20 and m_distance == 0:
                        if lim >= 45:
                            print("Slowing down to prepare for station arrival.")
                            ignoreaws = True
                            ignorelim = True
                            throttle(currentThrottle, int((42 / max_speed) * 100))
                        else:
                            throttle(currentThrottle, limitThrottle)
                    else:
                        throttle(currentThrottle, limitThrottle)
            except IndexError:
                pass

    def runATO():
        threading.Thread(target=task, daemon=True).start() 

    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == toggleATO_btn:
                    if ATOactive == False:
                        ATOactive = True
                        changeColour(toggleATO_btn,'#00FF00')
                        threading.Thread(target=runATO, daemon=True).start()
                    else:
                        ATOactive = False
                        changeColour(toggleATO_btn,'#FF0000')
                if event.ui_element == setMaxSpeed_btn:
                    max_speed = int(create_dialog("PyATO - Data Entry", "Enter Train's maximum speed"))
                if event.ui_element == toggleTTS:
                    if TTSactive == False:
                        TTSactive = True
                        changeColour(toggleTTS,'#00FF00')
                    else:
                        TTSactive = False
                        changeColour(toggleTTS,'#FF0000')
            
            curTime = datetime.now().strftime("%H:%M:%S")
            lblTime.set_text(curTime)

            manager.process_events(event)
            manager.update(time_delta)

        window_surface.blit(background, (0,0))
        manager.draw_ui(window_surface)

        pygame.display.update()

    
