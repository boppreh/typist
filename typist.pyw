import pythoncom, pyHook 
import os
from datetime import date
from background import tray

event_template = u'{Time} - {KeyID} ({key_name}) - {WindowName}'
location_template = 'data/{iso_date}.txt'
if not os.path.exists('data/'):
    os.mkdir('data/')

def save_on_file(event_text):
    path = location_template.format(iso_date=date.today())
    with open(path, 'a') as keys_file:
        keys_file.write(event_text.encode('utf-8') + '\n')

def OnKeyboardEvent(event):
    if event.Ascii > 32:
        key_name = chr(event.Ascii).decode('latin-1')
    elif event.Ascii > 0:
        key_name = 'ascii {}'.format(event.Ascii)
    else:
        key_name = event.Key

    save_on_file(event_template.format(key_name=key_name, **event.__dict__))

    return True

tray('Typist', 'typist.ico')
hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()
