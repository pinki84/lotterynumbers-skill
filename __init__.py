from adapt.intent import IntentBuilder
from mycroft.configuration import Configuration
from mycroft import MycroftSkill, intent_handler, intent_file_handler
from bs4 import BeautifulSoup
import requests
import time
import mycroft.audio
from datetime import datetime
from mycroft.util.log import LOG
from mycroft.util.format import nice_date, nice_duration, nice_time
from mycroft import MycroftSkill, intent_handler, intent_file_handler
from mycroft.util.parse import (extract_datetime, fuzzy_match, extract_number,
                                normalize)


__author__ = 'okticom'

class Lotterynumbers(MycroftSkill):
    def __init__(self):
        super(Lotterynumbers, self).__init__(name="Lotterynumbers")
        
        
        
    def initialize(self):
        self.config_core = Configuration.get()
        location = self.config_core.get('location')
        loc = location
        locationcode = 'not selected'
        if type(loc) is dict and loc["city"]:
            locationcode = loc["city"]["state"]["country"]["code"]
        LOG.error(locationcode)
        self.timebetwen = self.settings.get('timebetwen')
         

    @intent_handler(IntentBuilder("euromillions").require("euromillions"))
    
    def handler_euromillions(self, message):
        session = requests.get('https://www.national-lottery.co.uk/results/euromillions/draw-history/xml')
        soup = BeautifulSoup(session.content, 'xml')
        numbers = list()
        
        
        for drawdate in soup.find_all('draw-date'):
            date_time_obj = datetime.strptime(drawdate.text, '%Y-%m-%d').date()
            speak_date = nice_date(date_time_obj, lang=self.lang)
        self.speak_dialog("numbers.normal", data={"time": speak_date})
        mycroft.audio.wait_while_speaking()
        self.enclosure.deactivate_mouth_events()
        for ball in soup.find_all('ball'):
            numbers.append(ball.text)
            self.speak(ball.text)
            self.enclosure.mouth_text(ball.text)
            #self.enclosure.reset()
            time.sleep(1)   
        self.speak_dialog("numbers.luckystar")
        mycroft.audio.wait_while_speaking()
        for url in soup.find_all('bonus-ball'):
            #self.speak_dialog(url.text)
            self.enclosure.mouth_text(url.text)
            self.speak(url.text)
            time.sleep(1)
            #self.enclosure.reset()
        
        for url in soup.find_all('raffle'):
            #self.speak_dialog(url.text)
            p = (url.text)
        self.enclosure.activate_mouth_events()
        self.speak_dialog("string.raffle")
        #self.speak("Raffle is ")
        mycroft.audio.wait_while_speaking()
        self.enclosure.deactivate_mouth_events()
        self.enclosure.mouth_text(p)   
        for letter in p:
            self.speak(letter)
            time.sleep(0.6)
        self.enclosure.activate_mouth_events()
        self.enclosure.mouth_reset()
        
    @intent_handler(IntentBuilder("lottery").require("lottery"))
    def handler_lotterynumbers(self, message):
        session = requests.get('https://www.national-lottery.co.uk/results/lotto/draw-history/xml')
        soup = BeautifulSoup(session.content, 'xml')
        numbers = list()
        self.enclosure.deactivate_mouth_events()
        for drawdate in soup.find_all('draw-date'):
            date_time_obj = datetime.strptime(drawdate.text, '%Y-%m-%d').date()
            speak_date = nice_date(date_time_obj, lang=self.lang)
        self.speak_dialog("numbers.normal.lottery", data={"time": speak_date})
        mycroft.audio.wait_while_speaking()
        for ball in soup.find_all('ball'):
            numbers.append(ball.text)
            self.speak(ball.text)
            self.enclosure.mouth_text(ball.text)
            #self.enclosure.reset()
            time.sleep(1) 
            
        self.speak_dialog("numbers.bonus")
        mycroft.audio.wait_while_speaking()
        for url in soup.find_all('bonus-ball'):
            #self.speak_dialog(url.text)
            self.speak(url.text)
            self.enclosure.mouth_text(url.text)
            #self.enclosure.reset()
            time.sleep(1)
        #mycroft.audio.wait_while_speaking()
        self.enclosure.activate_mouth_events()
        self.enclosure.mouth_reset()
def create_skill():
    return Lotterynumbers()
