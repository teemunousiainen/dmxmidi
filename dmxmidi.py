import mido
import time
import random
import math
import threading
import readchar

dmxmidi_conf = {
    'dmx': {
        'lights': {
            'ledbar_1': {'type': 'rgb', 'start_channel': 0},
            'ledbar_2': {'type': 'rgb', 'start_channel': 3},
            'ledbar_3': {'type': 'rgb', 'start_channel': 6},
            'ledbar_4': {'type': 'rgb', 'start_channel': 9},
            'par64_1': {'type': 'rgba', 'start_channel': 12},
            'par64_2': {'type': 'rgba', 'start_channel': 17}
        },
        'array': ['par64_1', 'ledbar_1', 'ledbar_2', 'ledbar_3', 'ledbar_4', 'par64_2'],
        'rgb_colors': {
            'blk': [0, 0, 0],
            'red': [1, 0, 0],
            'grn': [0, 1, 0],
            'yel': [1, 1, 0],
            'blu': [0, 0, 1],
            'mgn': [1, 0, 1],
            'cyn': [0, 1, 1],
            'wht': [1, 1, 1]
        },
        'scenes': [
            ['blk', 'blk', 'blk', 'blk', 'blk', 'blk'],
            ['blu', 'red', 'blu', 'red', 'blu', 'red'],
            ['red', 'blu', 'red', 'blu', 'red', 'blu'],
            ['wht', 'wht', 'wht', 'wht', 'wht', 'wht'],
            ['blu', 'blk', 'blk', 'blk', 'blk', 'blk'],
            ['blk', 'blu', 'blk', 'blk', 'blk', 'blk'],
            ['blk', 'blk', 'blu', 'blk', 'blk', 'blk'],
            ['blk', 'blk', 'blk', 'blu', 'blk', 'blk'],
            ['blk', 'blk', 'blk', 'blk', 'blu', 'blk'],
            ['blk', 'blk', 'blk', 'blk', 'blk', 'blu'],
            ['blu', 'blk', 'blk', 'blk', 'blk', 'blu'],
            ['blk', 'blu', 'blk', 'blk', 'blu', 'blk'],
            ['blk', 'blk', 'blu', 'blu', 'blk', 'blk'],
            ['blu', 'blu', 'blu', 'blu', 'blu', 'blu']
        ],
        'chases': [
            [0],
            [1, 2],
            [1, 1, 2, 2],
            [1, 0, 2, 0],
            [3, 0, 4, 5,  6, 7, 8, 9,  8, 7, 6, 5,  10, 11, 12, 13]
        ]
    },
    'midi': {
        'device': 'UM-1',
        'setup': [
            ['note_on', 100, 127],
            ['note_on', 102, 1],
            ['note_on', 71, 127],
            ['note_on', 90, 127],
            ['note_on', 95, 127]
        ],
        'channels': 22,
        'start_note': 73
    }
}

class DMXMidi:
    conf:dict
    channels:int
    start_note:int
    outport:object
    tempo:int
    channel_array:list[int]
    chase:int
    start_ts:float
    running:bool
    thread:threading.Thread

    def __init__(self, conf) -> None:
        self.conf = conf
        self.start_note = self.conf['midi']['start_note']
        self.channels = self.conf['midi']['channels']
        try:
            self.outport = mido.open_output(self.conf['midi']['device'])
        except IOError as e:
            print(str(e))
            self.outport = None
        self.channel_array = [0] * self.channels

    def note_on(self, note, velocity):
        if self.outport == None:
            return
        msg = mido.Message('note_on', note=note, velocity=velocity)
        self.outport.send(msg)

    def setup(self):
        for cmd in self.conf['midi']['setup']:
            if cmd[0] == 'note_on':
                self.note_on(cmd[1], cmd[2])

    def start(self, chase:int, tempo:int, fade:float):
        self.thread = threading.Thread(target=self.run, args=(chase, tempo, fade))
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def reset(self):
        self.start_ts = round(time.time() * 1000) / 1000

    def run(self, chase:int, tempo:int, fade:float):
        self.tempo = tempo
        self.chase = chase
        self.setup()
        self.start_ts = round(time.time() * 1000) / 1000
        self.fade = fade
        self.running = True

        while self.running:
            chase = self.chase
            now = round(time.time() * 1000) / 1000
            past_time = now - self.start_ts
            steps = len(self.conf['dmx']['chases'][chase])
            step = math.floor(past_time * self.tempo / 60) % steps
            frag = (past_time * self.tempo / 60) - math.floor(past_time * self.tempo / 60)
            print(f"Chase: {chase} Now:  {now}, Past {past_time},  Step: {step}, frag: {frag}")

            next_step = (step + 1) % steps
            array_size = len(self.conf['dmx']['array'])
            for i in range(0, array_size):
                light = self.conf['dmx']['lights'][self.conf['dmx']['array'][i]]
                scene = self.conf['dmx']['scenes'][self.conf['dmx']['chases'][chase][step]]
                next_scene = self.conf['dmx']['scenes'][self.conf['dmx']['chases'][chase][next_step]]
                color = self.conf['dmx']['rgb_colors'][scene[i]]
                next_color = self.conf['dmx']['rgb_colors'][next_scene[i]]

                adjusted_frag = min(1, frag / (1 - self.fade))                

                for j in range(0, 3):
                    self.channel_array[light['start_channel'] + j] = color[j] + (next_color[j] - color[j]) * adjusted_frag

                if light['type'] == 'rgba':
                    self.channel_array[light['start_channel'] + 3] = 1

            print(self.channel_array)

            for i in range(0, self.channels):
                self.note_on(self.start_note + i, int(self.channel_array[i]*127))


            time.sleep(0.05)

dmxmidi = DMXMidi(dmxmidi_conf)

dmxmidi.start(0, 120, 0)

print("DMXMidi")
print("Running")
running = True
chases_count = len(dmxmidi_conf['dmx']['chases'])
while running:
    key = readchar.readkey()
    if key >= '0' and key <= '9':
        c = int(key)
        if c < chases_count:
            dmxmidi.chase = c
    elif key == 'q':
        running = False
    elif key == ' ':
        dmxmidi.reset()

dmxmidi.stop()
