#!/usr/bin/env python3
# Copyright 2017 Cyber-Renegade.
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

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import miaHotword
import random
import aiy.i18n
import signal
import time
import serial
import logging
import platform
import subprocess
import sys

CONFIRM_SOUND_PATH = '/home/pi/Music/R2D2/R2_Understood.wav'
CONFUSED_SOUND_PATH = '/home/pi/Music/R2D2/R2_Confused.wav'
UNRECOGNISED_SOUND_PATH = '/home/pi/Music/R2D2/R2_FastBip.wav'




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

def main():
    aiy.i18n.set_language_code("fr-FR")
    aiy.voicehat.get_status_ui().status('starting')
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('cuir')
    recognizer.expect_phrase('cuire')
    recognizer.expect_phrase('oui')
    recognizer.expect_phrase('non')
    recognizer.expect_phrase('salut')

    
    led = aiy.voicehat.get_led()
    voice_only=False
    seconds=0
         
    miaHot=miaHotword.miaHotword()
    with aiy.audio.get_recorder() as recorder:    
      while True:
          aiy.voicehat.get_status_ui().status('ready')
          print('Ready to listen')
          miaHot.waitForHotword(recorder,voice_only,seconds)
          if not(voice_only) or seconds > 0:
              aiy.audio.play_wave(CONFIRM_SOUND_PATH)
          reply=""
          print('Listening to what you actually have to say')
          aiy.voicehat.get_status_ui().status('listening')
          text = recognizer.recognize()
          aiy.voicehat.get_status_ui().status('thinking')
          print('thinking')
          if not text:
              aiy.voicehat.get_status_ui().status('error')
              aiy.audio.play_wave(UNRECOGNISED_SOUND_PATH)
          else:
              print('You said "', text, '"')
              if 'cuir' in text or 'cuire' in text:
                  reply = "Cuir cuir cuir moustache"
                  voice_only=True
              elif 'salut' or 'Salut' in text:
                  reply = "je viens de loin, mais vu mon teint je dois faire les choses bien. Ciao"
                  break
              elif 'eteindre' in text:
                  power_off_pi()
              elif text == 'redemarre':
                  reboot_pi()
                  break
              elif text == 'ip address':
                  say_ip()
                  break
              elif text == 'avance':
                  send_data_to_arduino("Go Straight")
                  break
              elif text == 'tourne a droite':
                  send_data_to_arduino("Turn Right")
                  break
              elif text == 'tourner a droite':
                  send_data_to_arduino("Turn Right")
                  break
              elif text == 'tourne a gauche':
                  send_data_to_arduino("Turn Left")
              elif text == 'tourner a gauche':
                  send_data_to_arduino("Turn Left")
              elif text == 'recule':
                  send_data_to_arduino("Go Backwards")
              elif text == 'recul':
                  send_data_to_arduino("Go Backwards")
          if len(reply) > 0:
            aiy.audio.say(reply)
    if len(reply) > 0:
        aiy.audio.say(reply)
    aiy.voicehat.get_status_ui().status('stopping')
    aiy.voicehat.get_status_ui().status('power-off')
    
if __name__ == '__main__':
    main()
    # To run the demo say the hotword and then ask about a holiday
