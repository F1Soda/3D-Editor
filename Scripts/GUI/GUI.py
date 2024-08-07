import Scripts.GUI.Elements.element as element_m
import Scripts.GUI.Elements.block as block_m
import Scripts.Source.General.input_manager as input_manager_m

import Scripts.GUI.header as header_m
import Scripts.GUI.inspector as inspector_m
import Scripts.GUI.hierarchy as hierarchy_m
import glm

#  HEADER_BOTTOM                             LEFT_INSPECTOR_CORNER
#    |                                                0.75
#    |   ############################################################
#    ↓   #                    Header                   #            #
#   0.95 ###############################################            #
#        #                                             #            #
#        #                                             #            #
#        #                                             # Inspector  #
#        #                                             #            #
#        #                                             #            #
#        #                                             #            #
#        #                                             ############## 0.5  DIVISION_BETWEEN_INSPECTOR_AND_HIERARCHY
#        #                                             #            #
#        #                                             #            #
#        #                                             #            #
#        #                                             #            #
#        #                                             # Hierarchy  #
#        #                                             #            #
#        #                                             #            #
#        #                                       (G)   #            #
#        #                                             #            #
#        ############################################################
#                                                     0.75
#                                              LEFT_INSPECTOR_CORNER
# G - Gizmo

# def draw_box(w, h):
#     print("#"*w)
#     for i in range(h-2):
#         print("#" + " "*(w-2) + "#")
#     print("#"*w)


# Settings
DEV_MODE = True

Pivot = element_m.Pivot


class GUI:
    HEADER_BOTTOM = 0.95
    LEFT_INSPECTOR_CORNER = 0.75
    DIVISION_BETWEEN_INSPECTOR_AND_HIERARCHY = 0.5

    def __init__(self, app, win_size):
        self.app = app
        self.win_size = glm.vec2(win_size)
        self.aspect_ratio = win_size[0] / win_size[1]

        input_manager_m.InputManager.handle_right_click_event += self.handle_right_click
        input_manager_m.InputManager.handle_right_hold_event += self.handle_right_hold
        input_manager_m.InputManager.handle_right_release_event += self.handle_right_release

        input_manager_m.InputManager.handle_left_click_event += self.handle_left_click
        input_manager_m.InputManager.handle_left_hold_event += self.handle_left_hold
        input_manager_m.InputManager.handle_left_release_event += self.handle_left_release

        input_manager_m.InputManager.handle_keyboard_press += self.handle_keyboard_press

        self.main_block = block_m.Block("Main Block", None, self.win_size)
        self.main_block.position.relative_window.right_top = glm.vec2(1)
        self.main_block.position.evaluate_values_by_relative_window()


        self.last_clicked_element = None
        self.active_sub_menu = None
        self.active_input_field = None
        self.windows = []
        self.selected_elements_in_hierarchy = []

        self.header = header_m.Header(self, self.main_block)
        self.inspector = inspector_m.Inspector(self, self.main_block)
        self.hierarchy = hierarchy_m.Hierarchy(self, self.main_block)



    def update_data_in_hierarchy(self):
        self.hierarchy.update_content()

    def select_element_in_hierarchy(self, object_id):
        self.hierarchy.select_element_in_hierarchy(object_id)
    def unselect_data_in_hierarchy(self):
        self.hierarchy.unselect_all_elements_in_content()

    def process_window_resize(self, new_size: glm.vec2):
        self.win_size = new_size
        self.main_block.process_window_resize(new_size)

    def render(self):
        self.main_block.render()
        for window in self.windows:
            window.render()

    def find_clicked_element(self, mouse_pos: glm.vec2):
        if self.active_sub_menu and self.active_sub_menu.position.check_if_clicked(mouse_pos):
            return self.active_sub_menu.find_clicked_element(mouse_pos)
        return self.main_block.find_clicked_element(mouse_pos)

    def handle_left_click(self, mouse_pos: glm.vec2):
        for window in self.windows[::-1]:
            element = window.find_clicked_element(mouse_pos)
            if element:
                if self.active_input_field:
                    if element.name == self.active_input_field.name:
                        return
                    else:
                        self.active_input_field.unselect()
                self.last_clicked_element = element
                element.handle_left_click(mouse_pos)
                return

        element = self.find_clicked_element(mouse_pos)
        if self.active_sub_menu:
            self.active_sub_menu.active = False
            self.active_sub_menu = None
        if self.active_input_field:
            if element.name == self.active_input_field.name:
                return
            else:
                self.active_input_field.unselect()
        if element.name == "Main Block":
            self.last_clicked_element = None
            return False
        else:
            element.handle_left_click(mouse_pos)
            self.last_clicked_element = element
            return True

    def handle_left_hold(self, mouse_pos: glm.vec2):
        if self.last_clicked_element:
            return self.last_clicked_element.handle_left_hold(mouse_pos)
        return False

    def handle_left_release(self, mouse_pos: glm.vec2):
        res = self.last_clicked_element is not None
        if self.last_clicked_element is not None:
            self.last_clicked_element.handle_left_release(mouse_pos)
        self.last_clicked_element = None
        return res

    def handle_right_click(self, mouse_pos: glm.vec2):
        element = self.find_clicked_element(mouse_pos)
        if self.active_sub_menu:
            self.active_sub_menu.active = False
            self.active_sub_menu = None

        if element.name == "Main Block":
            self.last_clicked_element = None
            return False
        else:
            element.handle_right_click(mouse_pos)
            print(element.name)
            self.last_clicked_element = element
            return True

    def handle_right_hold(self, mouse_pos: glm.vec2):
        if self.last_clicked_element:
            return self.last_clicked_element.handle_right_hold(mouse_pos)
        return False

    def handle_right_release(self, mouse_pos: glm.vec2):
        res = self.last_clicked_element is not None
        if self.last_clicked_element is not None:
            self.last_clicked_element.handle_right_release(mouse_pos)
        self.last_clicked_element = None
        return res

    def handle_keyboard_press(self, keys, pressed_char):
        if self.active_input_field:
            self.active_input_field.handle_keyboard_press(keys, pressed_char)
            return True
        return False

# def create_window_action(button, gui, pos):
#     test_window = window_m.Window(f"Test_window_{self.count_windows}", self.main_block, gui.win_size, gui)
#     test_window.position.relative_window.size = glm.vec2(0.3, 0.2)
#     test_window.position.relative_window.center = glm.vec2(0.5)
#     test_window.position.evaluate_values_by_relative_window()
#     test_window.update_position()
#     self.windows = self.windows + [test_window]
#     self.count_windows += 1
#     return test_window
#
#
# create_window = button_m.Button("Create Window button", self.main_block, self.win_size, self,
#                                 text="Create Window",
#                                 text_size=1,
#                                 action=create_window_action
#                                 )
# create_window.position.relative_window.size = glm.vec2(0.1, 0.1)
# create_window.position.relative_window.center = glm.vec2(0.5, 0.2)
# create_window.position.evaluate_values_by_relative_window()
# create_window.update_position()
