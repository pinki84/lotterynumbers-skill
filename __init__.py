from mycroft import MycroftSkill, intent_file_handler


class Lotterynumbers(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('lotterynumbers.intent')
    def handle_lotterynumbers(self, message):
        self.speak_dialog('lotterynumbers')


def create_skill():
    return Lotterynumbers()

