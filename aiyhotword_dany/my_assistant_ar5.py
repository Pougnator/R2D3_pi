#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import platform
import subprocess
import sys
import signal
import time
import serial
import miaHotword

import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.audio
import aiy.voicehat
from google.assistant.library.event import EventType


CONFIRM_SOUND_PATH = '/home/pi/Music/R2D2/R2_Understood.wav'
CONFUSED_SOUND_PATH = '/home/pi/Music/R2D2/R2_Confused.wav'
UNRECOGNISED_SOUND_PATH = '/home/pi/Music/R2D2/R2_FastBip.wav'

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted
'''
if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]
'''
signal.signal(signal.SIGINT, signal_handler)

voice_only=False
seconds=0
miaHot=miaHotword.miaHotword()



ser = serial.Serial(
                      
                       port='/dev/ttyAMA0',
                       baudrate = 9600,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
                       bytesize=serial.EIGHTBITS,
                       timeout=1
                   )


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)
def send_data_to_arduino(write_string):
    print(write_string)
    write_bytes = write_string.encode('ascii')
    ser.write(write_bytes)

def power_off_pi():
    aiy.audio.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    aiy.audio.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    aiy.audio.say('My IP address is %s' % ip_address.decode('utf-8'))


def process_event(assistant, event):
    status_ui = aiy.voicehat.get_status_ui()
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        
        #if sys.stdout.isatty():
         #   print('Say "OK, Google" then speak, or press Ctrl+C to quit...')
            

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        #aiy.audio.play_wave(CONFIRM_SOUND_PATH)
        status_ui.status('listening')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if text == 'eteindre':
            assistant.stop_conversation()
            power_off_pi()
        elif text == 'redemarre':
            assistant.stop_conversation()
            reboot_pi()
        elif text == 'ip address':
            assistant.stop_conversation()
            say_ip()
        elif text == 'avance':
            assistant.stop_conversation() 
            send_data_to_arduino("Go Straight")
        elif text == 'tourne a droite':
            assistant.stop_conversation() 
            send_data_to_arduino("Turn Right")
        elif text == 'tourner a droite':
            assistant.stop_conversation() 
            send_data_to_arduino("Turn Right")
        elif text == 'tourne a gauche':
            assistant.stop_conversation() 
            send_data_to_arduino("Turn Left")
        elif text == 'tourner a gauche':
            assistant.stop_conversation() 
            send_data_to_arduino("Turn Left")
        elif text == 'recule':
            assistant.stop_conversation() 
            send_data_to_arduino("Go Backwards")
        elif text == 'recul':
            assistant.stop_conversation() 
            send_data_to_arduino("Go Backwards")
            
        aiy.audio.play_wave(UNRECOGNISED_SOUND_PATH)
    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        status_ui.status('ready')
       # miaHot.waitForHotword(recorder,voice_only,seconds)

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    if platform.machine() == 'armv6l':
        print('Cannot run hotword demo on Pi Zero!')
        exit(-1)
    status_ui = aiy.voicehat.get_status_ui()
    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
                
        for event in assistant.start():
            process_event(assistant, event)
    with aiy.audio.get_recorder() as recorder:
        while True:
            status_ui.status('ready')
            miaHot.waitForHotword(recorder,voice_only,seconds)
            status_ui.status('listening')
            print('Listening...')
            assistant.start_conversation()
            #assistant.send_text_query("Quelle heure est-il?")
            
       
if __name__ == '__main__':
    main()
