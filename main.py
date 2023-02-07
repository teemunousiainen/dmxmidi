from dmxmidi import *
from conf import *
from gui import *

print("DMXMidi 1.0")

dmxmidi = DMXMidi(dmxmidi_conf)

print("Stage 1")

dmxmidi.start(0, 120, 0)

print("Stage 2")

gui = CustomGUI(dmxmidi, dmxmidi_conf)

print("Stage 3")

gui.run()

dmxmidi.stop()
