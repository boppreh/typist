from background import tray
tray('Typist', 'typist.ico')

import pythoncom, pyHook 

event_template = '{Time} - {KeyID} ({key_name}) - {WindowName}'

def OnKeyboardEvent(event):
    if event.Ascii:
        key_name = chr(event.Ascii).decode('latin-1')
    else:
        key_name = ''

    event_text = event_template.format(key_name=key_name, **event.__dict__)
    with open('keys.txt', 'a') as keys_file:
        keys_file.write(event_text + '\n')

    return True

hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()
