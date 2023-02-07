import RPi.GPIO as GPIO

class GPIOController:
    pinmap:list[int]
    status:list

    def __init__(self, pinmap:list) -> None:
        self.pinmap = pinmap
        self.status = [0] * len(pinmap)
        for i in range(0, len(pinmap)):
            GPIO.setup(self.pinmap[i], GPIO.OUT)
    
    def get_key(self) -> int:
        new_status = [0] * len(self.pinmap)

        for i in range(0, len(self.pinmap)):
            new_status[i] = GPIO.input(self.pinmap[i])

        if sum(new_status) == 0 or sum(self.status) > 0:
            key = None

        key = 0
        for i in range(0, len(self.pinmap)):
            key = key | new_status[i]
            key = key << 1

        return key
