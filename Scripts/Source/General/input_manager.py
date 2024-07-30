import pygame as pg
import Scripts.Source.General.object_picker as object_picker_m
import enum
import glm


class MouseButtonState(enum.Enum):
    Idle = 0
    Pressed = 1
    Hold = 2
    Released = 3


class InputManager:
    # Mouse
    mouse_states = [MouseButtonState.Idle, MouseButtonState.Idle, MouseButtonState.Idle]
    past_mouse_buttons = (False, False, False)
    mouse_position = glm.vec2(0, 0)

    # Other
    _app = None
    _gui = None

    @staticmethod
    def init(app):
        InputManager._app = app
        InputManager._gui = app.gui

    @staticmethod
    def update_mouse_status():
        mouse_buttons = pg.mouse.get_pressed()

        for i in range(3):
            if mouse_buttons[i]:
                if InputManager.mouse_states[i] == MouseButtonState.Idle:
                    InputManager.mouse_states[i] = MouseButtonState.Pressed
                elif InputManager.mouse_states[i] == MouseButtonState.Pressed:
                    InputManager.mouse_states[i] = MouseButtonState.Hold
            if not mouse_buttons[i]:
                if InputManager.past_mouse_buttons[i]:
                    InputManager.mouse_states[i] = MouseButtonState.Released
                else:
                    InputManager.mouse_states[i] = MouseButtonState.Idle

        InputManager.past_mouse_buttons = mouse_buttons
        InputManager.mouse_position = glm.vec2(pg.mouse.get_pos())
        InputManager.mouse_position.y = InputManager._app.win_size.y - InputManager.mouse_position.y

    @staticmethod
    def process():
        InputManager.update_mouse_status()
        if InputManager.mouse_states[0] == MouseButtonState.Pressed:
            if InputManager._gui.process_left_click(InputManager.mouse_position):
                return
            if object_picker_m.ObjectPicker.process_left_click(InputManager.mouse_position):
                pass
        if InputManager.mouse_states[0] == MouseButtonState.Released:
            if object_picker_m.ObjectPicker.process_release_left_mouse_button():
                pass

        if InputManager.mouse_states[0] == MouseButtonState.Hold:
            if object_picker_m.ObjectPicker.process_hold_left_mouse_button(InputManager.mouse_position):
                return

