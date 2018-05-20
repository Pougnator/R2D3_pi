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

"""A demo of the Google CloudSpeech recognizer."""

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import aiy.i18n
import aiy.audio

CONFIRM_SOUND_PATH = '/home/pi/Music/R2D2/R2_Understood.wav'
CONFUSED_SOUND_PATH = '/home/pi/Music/R2D2/R2_Confused.wav'
UNRECOGNISED_SOUND_PATH = '/home/pi/Music/R2D2/R2_FastBip.wav'



def main():
    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status('starting')
    
    aiy.i18n.set_language_code("fr-FR")
    
    
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('allumer le feu')
    recognizer.expect_phrase('éteindre')
    recognizer.expect_phrase('clignotter')
    recognizer.expect_phrase('cuir')
    recognizer.expect_phrase('R2')

    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()

    while True:
        status_ui.status('ready')
        print('Press the button and speak')
        button.wait_for_press()
        #aiy.voicehat.get_status_ui().set_trigger_sound_wave('/home/pi/Music/R2D2/hotword.wav')
        status_ui.status('listening')
        print('Listening...')
        text = recognizer.recognize()
        if not text:
            print('Sorry, I did not hear you.')
            aiy.audio.play_wave(CONFUSED_SOUND_PATH)
        else:
            WaitingForHotword = True
            print('You said "', text, '"')
            if 'allumer le feu' in text:
                led.set_state(aiy.voicehat.LED.ON)
            elif 'éteindre' in text:
                led.set_state(aiy.voicehat.LED.OFF)
            elif 'clignotter' in text:
                led.set_state(aiy.voicehat.LED.BLINK)
            elif 'cuir' in text:
                led.set_state(aiy.voicehat.LED.BLINK)
                aiy.audio.say('cuir cuir cuir moustache')
            elif 'goodbye' in text:
                break
            else: aiy.audio.play_wave(UNRECOGNISED_SOUND_PATH)
                     
             

if __name__ == '__main__':
    main()

