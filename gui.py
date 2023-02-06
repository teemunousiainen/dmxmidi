
from dmxmidi import *
import readchar

class GUI:
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
