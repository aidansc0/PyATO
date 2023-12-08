import numpy as nm
import cv2
import pytesseract
import time
import math
from PIL import ImageGrab
from PIL import ImageFilter
import pygame
import pygame_gui
from datetime import datetime
import re
import tkinter as tk
from tkinter import simpledialog
import threading
import keyboard

stnNamePos = 447, 985, 655, 1015
stopAlertPos = 852, 800, 1070, 839
doors_pos = 870, 822, 871, 823
loading_pos = 781, 823, 782, 824
continue_pos = 1032, 460, 1033, 461
undershoot_pos = 709, 906, 710, 907
awaiting_pos = 862, 823, 863, 824
buzzer_pos = 824, 816, 825, 817

trainingActive = False
carLength = 0
curStation = ""

window_surface = pygame.display.set_mode((800, 200), pygame.DOUBLEBUF)
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
time.sleep(1)

def changeColour(button,selColour):
    button.colours['normal_bg'] = pygame.Color(selColour)
    button.rebuild()

def create_dialog(title, question):
    root = tk.Tk()
    root.withdraw()
    userInput = simpledialog.askstring(title, question)
    root.destroy()
    return userInput

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("PyATO - Level 2 Trainer")
    
    background = pygame.Surface((800,200))
    background.fill(('#000435'))

    manager = pygame_gui.UIManager((800, 600))
    clock = pygame.time.Clock()
    is_running = True

    toggleATO_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 100), (150, 50)), text='Trainer Toggle', manager=manager)
    setCarLength_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 100), (150, 50)), text='Set Car Length', manager=manager)

    def task():
        global carLength
        global curStation

        while trainingActive == True:
            cap = ImageGrab.grab(bbox=(stnNamePos))
            cap = cap.filter(ImageFilter.MedianFilter())
            cap = cv2.cvtColor(nm.array(cap), cv2.COLOR_RGB2GRAY)
            tesstr = pytesseract.image_to_string(
                cap,
                config="--psm 7")
            curStation = str(tesstr)

            cap2 = ImageGrab.grab(bbox=(stopAlertPos))
            cap2 = cap2.filter(ImageFilter.MedianFilter())
            cap2 = cv2.cvtColor(nm.array(cap2), cv2.COLOR_RGB2GRAY)
            tesstr2 = pytesseract.image_to_string(
                cap2,
                config="--psm 7")
            curAlert = str(tesstr2)

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
            if doors_value == (255, 255, 255):
                print("CLOSING DOORS")
            elif loading_value == (255, 255, 255):
                print("LOADING")
            elif awaiting_value == (255, 255, 255):
                print("WAITING FOR GUARD")
            elif buzzer_value == (255, 255, 255):
                print("ACTIVATING THE BUZZER")
            else:
                if curAlert == "Stop to load passengers":
                    print("Platform Detected")
                    start_time = time.time()
                    while True:
                        if keyboard.is_pressed('s'):
                            end_time = time.time()
                            break
                        elif keyboard.is_pressed('esc'):
                            end_time = start_time
                            break
                    elapsed_time = end_time - start_time

                    f = open("stoppingTimes.py", "a")
                    f.write("def " + curStation + str(carLength)  + "():\n")
                    f.write("\ttime.sleep(" + str(elapsed_time) + ")\n")
                    f.write("\n")
                    f.close()

    def runTraining():
        threading.Thread(target=task, daemon=True).start()

    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == toggleATO_btn:
                    if trainingActive == False:
                        trainingActive = True
                        changeColour(toggleATO_btn,'#00FF00')
                        runTraining()
                    else:
                        trainingActive = False
                        changeColour(toggleATO_btn,'#FF0000')
                if event.ui_element == setCarLength_btn:
                    carLength = int(create_dialog("L2 Trainer - Data Entry", "Enter Train length"))

            manager.process_events(event)
            manager.update(time_delta)
    
    
        window_surface.blit(background, (0,0))
        manager.draw_ui(window_surface)

        pygame.display.update()

                    

                                           

        



