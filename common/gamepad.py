
from dataclasses import dataclass

@dataclass
class LogitechF310State(dict):
    # Buttons
    BTN_SOUTH: int = False  # A
    BTN_EAST: int = False   # B
    BTN_NORTH: int = False  # X
    BTN_WEST: int = False   # Y
    BTN_TL: int = False     # Left Bumper
    BTN_TR: int = False     # Right Bumper
    BTN_SELECT: int = False # Back Button
    BTN_START: int = False  # Start Button
    BTN_THUMBL: int = False # Left Joystick Button
    BTN_THUMBR: int = False # Right Joystick Button

    # Joysticks
    ABS_X: int = 0  # Left X Stick (left/right)
    ABS_Y: int = 0  # Left Y Stick (up/down)
    ABS_RX: int = 0 # Right X Stick
    ABS_RY: int = 0 # Right Y Stick
    ABS_Z: int = 0  # Left Trigger
    ABS_RZ: int = 0 # Right Trigger

    # HAT
    ABS_HAT0X: int = False  # D-Pad X (left/right)
    ABS_HAT0Y: int = False  # D-Pad Y (up/down)

    def __setitem__(self, key, data):
        if key in self.__dict__.keys():
            self.__dict__[key] = data

    def __getitem__(self, key):
        return self.__dict__[key]

class LogitechF310Mapper:
    def __init__(self):
        self.gamepad_state = LogitechF310State()

    def update(self, event_list):
        for event in event_list:
            self.gamepad_state[event.code] = event.state

    def get_state(self):
        return vars(self.gamepad_state)

