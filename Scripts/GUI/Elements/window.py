import copy

import Scripts.GUI.Elements.element as element_m
import Scripts.GUI.Elements.text as text_m
import Scripts.GUI.Elements.input_field as input_field_m
import Scripts.GUI.Elements.button as button_m
import Scripts.GUI.Elements.block as block_m
import glm

#  HEADER_BOTTOM                 BUTTON_LEFT_CORNER
#    |                             0.95
#    |   #################################
#    ↓   #           Header          # X #
#   0.95 #################################
#        #                               #
#        #                               #
#        #                               #
#        #                               #
#        #                               #
#        #################################

HEADER_BOTTOM = 0.8
BUTTON_LEFT_CORNER = 0.95


class Window(element_m.Element):
    def __init__(self, name, rely_element, win_size: glm.vec2, gui, header_text=""):
        super().__init__(name, rely_element, win_size)
        self.gui = gui

        self.background = block_m.Block(f"{name}_background", self, win_size, (1, 1, 1, 0.7))

        self.background.position.relative.right_top = glm.vec2(1)
        self.inner_data_block = block_m.Block(f"{name}_inner_block", self.background, win_size)
        self.inner_data_block.position.relative.right_top = glm.vec2(1, HEADER_BOTTOM)

        self.header = block_m.Block(f'{name}_header', self.background, win_size, (0.1, 0.1, 0.1, 0.7))
        self.header.position.relative.left_bottom = glm.vec2(0, HEADER_BOTTOM)
        self.header.position.relative.right_top = glm.vec2(1)

        self.header_text = text_m.Text("Header_text", self.header, win_size, header_text, pivot=element_m.Pivot.Center)
        self.header_text.position.relative.center = glm.vec2(0.5)

        def _return_header(pos):
            return self.header

        self.header_text.find_clicked_element = _return_header

        self._last_clicked_header_pos = glm.vec2()

        def handle_left_click_header(pos):
            self._last_clicked_header_pos = copy.copy(pos)
            gui.windows.remove(self)
            self.gui.windows = self.gui.windows + [self]

        def handle_left_hold_header(pos):
            self.position.absolute.transform(pos - self._last_clicked_header_pos)
            self._last_clicked_header_pos = copy.copy(pos)
            self.position.evaluate_values_by_absolute()
            self.update_position()

        self.header.handle_left_hold = handle_left_hold_header
        self.header.handle_left_click = handle_left_click_header

        def close_button_action(button, gui, pos):
            self.close()

        close_button = button_m.Button(f"{name}_close_button", self.header, win_size, gui, "X", 2,
                                       action=close_button_action,
                                       color=(1, 0, 0, 1),
                                       text_color=(1, 1, 1, 1)
                                       )
        close_button.position.relative.size = glm.vec2(0.1, 1)
        close_button.position.relative.center = glm.vec2(0.95, 0.5)

    def find_clicked_element(self, mouse_pos: glm.vec2):
        if self.position.check_if_clicked(mouse_pos):
            return super().find_clicked_element(mouse_pos)
        else:
            return None

    def close(self):
        self.active = False
        self.gui.last_clicked_element = None
        self.gui.windows.remove(self)
        self.delete()

    def delete(self):
        self.gui.main_block.elements.remove(self)
        self.gui = None
        self.background = None
        super().delete()
