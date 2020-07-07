from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler
from bs4 import BeautifulSoup
import requests

class Lotterynumbers(MycroftSkill):
    def __init__(self):
        super(Lotterynumbers, self).__init__(name="Lotterynumbers")

    @intent_handler(IntentBuilder("Lotterynumbers").require("lotterynumbers.intent"))
    def handle_lotterynumbers(self, message):
        session = requests.get('https://www.national-lottery.co.uk/results/euromillions/draw-history/xml')
        soup = BeautifulSoup(session.content, 'lxml-xml')

        for ball in soup.find_all('ball'):
            print(ball.text)
            self.speak_dialog(ball.text)
         
        for url in soup.find_all('bonus-ball'):
         
            self.speak_dialog(url.text)
       
        for url in soup.find_all('raffle'):
            self.speak_dialog(url.text)
                  
        #self.speak_dialog('lotterynumbers')


def create_skill():
    return Lotterynumbers()

