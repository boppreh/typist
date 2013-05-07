import pythoncom, pyHook 
import os
import sqlite3
from background import tray

event_template = '{Time} - {KeyID} ({key_name}) - {WindowName}'
location_template = 'data/{iso_date}.txt'

db_exists = os.path.exists('keys.db')
db = sqlite3.connect('keys.db')
if not db_exists:
    c = db.cursor()
    c.execute("""CREATE TABLE key_events
                 (id integer primary key autoincrement,
                  timestamp integer,
                  event_time integer,
                  window text,
                  ascii text,
                  key text,
                  key_id integer)""")
    db.commit()

def OnKeyboardEvent(event):
    data = (event.Time, event.Window, event.Ascii, event.Key, event.KeyID)
    db.execute('INSERT INTO key_events VALUES\
                (null, datetime(), ?, ?, ?, ?, ?)', data)
    db.commit()
    return True

tray('Typist', 'typist.ico')
hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()
try:
    pythoncom.PumpMessages()
finally:
    db.close()
