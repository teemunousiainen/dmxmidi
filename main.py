from dmxmidi import *
from conf import *
from gui import *

dmxmidi = DMXMidi(dmxmidi_conf)

dmxmidi.start(0, 120, 0)

print("DMXMidi 1.0")

gui = GUI(dmxmidi, dmxmidi_conf)

gui.run()

dmxmidi.stop()
