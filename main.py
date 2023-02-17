import time
import hashlib
from urllib.request import urlopen, Request
import requests
import PySimpleGUI as psg

# Color def
Color1 = '#2E294E'
Color2 = '#FCFCFC'
Color3 = '#FFD400'

# Monitors website for changes with given cooldown
def monitor(url: str, waitTime: int):
    site = Request(url)
    state = urlopen(site).read()
    hash1 = hashlib.sha224(state).hexdigest()
    while(True):
        time.sleep(waitTime)
        state = urlopen(site).read()
        hash2 = hashlib.sha224(state).hexdigest()
        if hash2 != hash1:
            input = psg.popup_ok_cancel('Website ' + url + ' updated', background_color=Color1, text_color=Color2, button_color=(Color1, Color3))
            if input == 'Cancel':
                break

# GUI Layout
layout = [[psg.Text('Input url to monitor', background_color=Color1, text_color=Color2)],
          [psg.InputText(key='-URL-', size=(64,20), background_color=Color2)],
          [psg.Text('Choose ping cooldown [s]', background_color=Color1, text_color=Color2)],
          [psg.Slider(range=(10, 1800), default_value=60, resolution=10, orientation='horizontal', size=(50,20), key='-SLIDER-', background_color=Color1, text_color=Color2)],
          [psg.Button('Start', button_color=(Color1, Color3))]]
window = psg.Window('Website monitor', layout, background_color=Color1)

# Event handling
while(True):
    event, values = window.read()
    if event == psg.WIN_CLOSED:
        window.close()
        break
    elif event == 'Start':
        waitTime = values['-SLIDER-']
        url = values['-URL-']
        try:
            websiteCheck = requests.get(url)
        except:
            psg.popup('Website does not exist', background_color=Color1, text_color=Color2, button_color=(Color1, Color3))
            continue
        window.close()
        monitor(url, waitTime)
        break