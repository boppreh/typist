import os
from datetime import date
from background import tray
import keyboard

event_template = u'{time} - {event_type} - {key_code}'
location_template = 'data/{iso_date}.txt'
if not os.path.exists('data/'):
    os.mkdir('data/')

def save_on_file(event_text):
    path = location_template.format(iso_date=date.today())
    with open(path, 'a') as keys_file:
        keys_file.write(event_text + '\n')

def handler(event):
    save_on_file(event_template.format(**event.__dict__))

tray('Typist', 'typist.ico')
keyboard.add_handler(handler)
