try:
    from Queue import Queue
except:
    from queue import Queue
import os
from datetime import date
from threading import Thread
from tray import tray
from simpleserver import serve
import keyboard

event_template = u'{time} - {event_type} - {keycode}'
location_template = 'data/{iso_date}.txt'
if not os.path.exists('data/'):
    os.mkdir('data/')

# The keyboard handler will be called for each keystroke, in a blocking manner,
# so it must be the lightest possible to avoid slowing down the typing. To
# achieve this the handler puts the event in a Queue to be processed in
# parallel, effectively making the handling asynchronous. 
#
# To give an idea of how important this concurrency is important, the events
# queue sometimes grows to tens of items in just a few seconds of burst typing.
# Without multiple threads it would have slowed the typing significantly.

events = Queue()
service = {'typed': ''}

def keyboard_event_handler(event):
    events.put(event)

def keyboard_event_writer():
    while True:
        try:
            event = events.get()
            event_text = event_template.format(**event.__dict__)
            path = location_template.format(iso_date=date.today())
            
            with open(path, 'a') as keys_file:
                keys_file.write(event_text + '\n')

            if event.char and event.event_type == 'key down':
                service['typed'] = (service['typed'] + event.char)[-100:]
        except Exception as e:
            # In case of error, print and continue. We don't want the logging
            # to stop permanently because of some temporary error.
            print(e)

tray('Typist', 'typist.ico')
serve(service, port=2341)
keyboard.add_handler(keyboard_event_handler)
Thread(target=keyboard_event_writer).start()
