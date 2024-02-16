# PyATO
A functional rendition of Automatic Train Operation capability.

## Getting Started
PyATO works on Optical Character Recognition (OCR) to identify signal aspects, speed limits and distances. As a result the following libraries are required.
These can be installed using the command "pip install (library)"

numpy, cv2, pytesseract, time, math, PIL - ImageGrab/ImageFilter, pygame, pygame_gui, datetime, re, tkinter, threading, pydirectinput, playsound, gtts.

To run the script, in a command line, run "python main.py"

No support is offered with PyATO, as per licence.

## Capabilities
PyATO is in a Alpha Stage, but at this time it is able to:
Drive any train to a certain speed limit, Acknowledge AWS, Stop at Stations with automatic opening and closing of doors, Drive at caution according to AWS signals.
At this time, PyATO cannot do the following:
Stop at specific car stop markers (sorry dispatchers), stop within the full platform length at certain stations, drive up at caution to danger aspect signals.

## Requirements for use
For OCR to correctly identify in-game UI elements:
Your monitor must be 1920x1080 or be set to this resolution, be within fullscreen, Driving HUD should be set to large within the main-menu settings.

## Acknowledgements 
This is a fork of matrndev's "scr-autopilot" and much of the ATO driving logic is written by Matyáš, as a result, full credit goes to him for the self-driving capabilities.
The GUI based on pygame and pygame-ui was implemented by myself.
