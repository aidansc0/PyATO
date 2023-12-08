# PyATO - Level 2 Trainer
Software to provide timing details to allow for the ATO to stop at correct car markers within specific times at 45 mph.

## How to use
- Run the python trainer.py script
- Set the Car length, in cars. For example, a class 380/0 you would type in 3, for 3 cars.
- Toggle the trainer.
- Approach a station at 45mph, then in one keystroke, stop at any station, stopping at the correct car marker.

## Getting Started
Level2Trainer works on Optical Character Recognition (OCR) to identify signal aspects, speed limits and distances. As a result the following libraries are required.
These can be installed using the command "pip install (library)"

numpy, cv2, pytesseract, time, math, PIL - ImageGrab/ImageFilter, pygame, pygame_gui, datetime, re, tkinter, threading, pydirectinput, playsound, gtts.

To run the script, in a command line, run "python trainer.py"

## Requirements for use
For OCR to correctly identify in-game UI elements:
Your monitor must be 1920x1080 or be set to this resolution, Roblox must be within fullscreen, SCR's Driving HUD should be set to large within the main-menu settings.

