import pygame as pg


class InputManager:
    _mouse_pressed = False
    _mouse_buttons = (False, False, False)

    @property
    def mouse_pressed(self):
        return self._mouse_pressed

    @property
    def mouse_buttons(self):
        return self._mouse_buttons

    @staticmethod
    def update():
        mouse_buttons = pg.mouse.get_pressed()

        if mouse_buttons[0] and not InputManager._mouse_buttons[0]:
            InputManager._mouse_pressed = True

        if not mouse_buttons[0] and InputManager._mouse_buttons[0]:
            InputManager._mouse_pressed = False

        InputManager._mouse_buttons = mouse_buttons
