import pythoncom, pyHook 
import os
from datetime import date
from background import tray

event_template = '{Time} - {KeyID} ({key_name}) - {WindowName}'
location_template = 'data/{iso_date}.txt'

def save_on_file(event_text):
    if not os.path.exists(os.path.dirname(location_template)):
        os.mkdir(os.path.dirname(location_template))

    path = location_template.format(iso_date=date.today())

    with open(path, 'a') as keys_file:
        keys_file.write(event_text + '\n')

def OnKeyboardEvent(event):
    if event.Ascii:
        key_name = chr(event.Ascii).decode('latin-1')
    else:
        key_name = ''

    save_on_file(event_template.format(key_name=key_name, **event.__dict__))

    return True

tray('Typist', 'typist.ico')
hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()
