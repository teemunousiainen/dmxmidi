import mido
import time
import math
import threading

class DMXMidi:
    conf:dict
    channels:int
    start_note:int
    outport:object
    tempo:int
    channel_array:list[int]
    chase:int
    start_ts:float
    step:int
    running:bool
    thread:threading.Thread
    division:int

    def __init__(self, conf) -> None:
        self.conf = conf
        self.start_note = self.conf['midi']['start_note']
        self.channels = self.conf['midi']['channels']
        try:
            ports = mido.get_output_names()
            print(f"Midi ports: {str(ports)}")
            self.outport = mido.open_output(ports[0])
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

    def start(self, chase:int, tempo:int, fade:float, division:int=4):
        self.thread = threading.Thread(target=self.run, args=(chase, tempo, fade))
        self.division = division
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def reset(self):
        self.start_ts = round(time.time() * 1000) / 1000

    def set_patch(self, patch:int):
        self.tempo = self.conf['patches'][patch]['tempo']
        self.reset()

    def run(self, chase:int, tempo:int, fade:float):
        self.tempo = tempo
        self.chase = chase
        self.setup()
        self.start_ts = round(time.time() * 1000) / 1000
        self.fade = fade
        self.running = True

        while self.running:
            chase = self.chase
            division = self.conf['dmx']['chases'][chase]['division']
            now = round(time.time() * 1000) / 1000
            past_time = now - self.start_ts
            steps = len(self.conf['dmx']['chases'][chase]['sequence'])
            step = math.floor(past_time * self.tempo / 60 * division / 4) % steps
            self.step = step
            frag = (past_time * self.tempo / 60 * division / 4) - math.floor(past_time * self.tempo / 60 * division / 4)
            # print(f"Chase: {chase} Now:  {now}, Past {past_time},  Step: {step}, frag: {frag}")

            next_step = (step + 1) % steps
            array_size = len(self.conf['dmx']['array'])
            for i in range(0, array_size):
                light = self.conf['dmx']['lights'][self.conf['dmx']['array'][i]]
                scene = self.conf['dmx']['scenes'][self.conf['dmx']['chases'][chase]['sequence'][step]]
                next_scene = self.conf['dmx']['scenes'][self.conf['dmx']['chases'][chase]['sequence'][next_step]]
                color = self.conf['dmx']['rgb_colors'][scene[i]]
                next_color = self.conf['dmx']['rgb_colors'][next_scene[i]]

                adjusted_frag = min(1, frag / (1 - self.fade))                

                for j in range(0, 3):
                    self.channel_array[light['start_channel'] + j] = color[j] + (next_color[j] - color[j]) * adjusted_frag

                if light['type'] == 'rgba':
                    self.channel_array[light['start_channel'] + 3] = 1

            # print(self.channel_array)

            for i in range(0, self.channels):
                self.note_on(self.start_note + i, int(self.channel_array[i]*127))


            time.sleep(0.05)

