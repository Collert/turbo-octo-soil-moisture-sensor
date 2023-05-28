import pygame
import os
import random
from datetime import datetime, timedelta

def pickRandomDry():
    sound=random.choice(os.listdir("/home/pi/Desktop/voicelines/Thirsty"))
    playSound(f"/home/pi/Desktop/voicelines/Thirsty/{sound}")
    
def pickRandomEnough():
    sound=random.choice(os.listdir("/home/pi/Desktop/voicelines/Refilled"))
    playSound(f"/home/pi/Desktop/voicelines/Refilled/{sound}")
    
def pickRandomWet():
    sound=random.choice(os.listdir("/home/pi/Desktop/voicelines/Too_much"))
    playSound(f"/home/pi/Desktop/voicelines/Too_much/{sound}")
    
def playSound(path):
	pygame.mixer.init()
	pygame.mixer.music.load(path)
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
		continue

def quiet_hours():
    now = datetime.now()
    if now.weekday() < 5 and now.hour < 18:
        return True
    elif now.weekday() >= 5 and now.hour < 8:
        return True
    else:
        return False
    
