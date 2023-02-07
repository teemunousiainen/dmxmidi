
from dmxmidi import *
from st7565 import *
from gpio_controller import *
import readchar

class GUI:
    def __init__(self, dmxmidi, dmxmidi_conf) -> None:
        pass

    def run(self):
        pass


class ConsoleGUI(GUI):
    dmxmidi:DMXMidi
    dmxmidi_conf:dict

    def __init__(self, dmxmidi, dmxmidi_conf) -> None:
        self.dmxmidi = dmxmidi
        self.dmxmidi_conf = dmxmidi_conf

    def run(self):
        running = True
        chases_count = len(self.dmxmidi_conf['dmx']['chases'])
        patch = 0
        self.dmxmidi.set_patch(patch)
        while running:
            print(f"\r{self.dmxmidi_conf['patches'][patch]['name']} Tempo: {self.dmxmidi.tempo} bpm Chase: {self.dmxmidi.chase} {self.dmxmidi.step}/{len(self.dmxmidi_conf['dmx']['chases'][self.dmxmidi.chase]['sequence'])}      ", end='')
            key = readchar.readkey()
            if key >= '0' and key <= '9':
                c = int(key)
                if c < chases_count:
                    self.dmxmidi.chase = c
            elif key == 'q':
                running = False
            elif key == ' ':
                self.dmxmidi.reset()
            elif key == '<':
                patch = (patch + 1) % len(self.dmxmidi_conf['patches'])
                self.dmxmidi.set_patch(patch)
            elif key == '>':
                patch = (patch + -1) % len(self.dmxmidi_conf['patches'])
                self.dmxmidi.set_patch(patch)

class CustomGUI(GUI):
    dmxmidi:DMXMidi
    dmxmidi_conf:dict
    controller:GPIOController
    display:ST7565

    def __init__(self, dmxmidi, dmxmidi_conf) -> None:
        self.dmxmidi = dmxmidi
        self.dmxmidi_conf = dmxmidi_conf
        self.display = ST7565()
        self.controller = GPIOController([1, 2, 3])

    def run(self):
        running = True
        chases_count = len(self.dmxmidi_conf['dmx']['chases'])
        patch = 0
        self.dmxmidi.set_patch(patch)
        while running:
            patch_name = self.dmxmidi_conf['dmx']['patches']['name']
            patch_tempo = self.dmxmidi_conf['dmx']['patches']['tempo']
            self.display.lcd_ascii168_string(0,0, patch_name[0:display.width])
            self.display.lcd_ascii168_string(0,2, f"{patch_tempo} bpm  "[0:display.width])

            key = self.controller.get_key()
            if key >= 2:
                c = int(key)
                if c < chases_count:
                    self.dmxmidi.chase = c
                self.dmxmidi.reset()
            elif key == 0:
                patch = (patch + 1) % len(self.dmxmidi_conf['patches'])
                self.dmxmidi.set_patch(patch)
            elif key == 1:
                patch = (patch + -1) % len(self.dmxmidi_conf['patches'])
                self.dmxmidi.set_patch(patch)
