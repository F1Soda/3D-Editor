import pympler.tracker

import Scripts.GUI.Elements.element as element_m
import Scripts.GUI.Elements.block as block_m
import Scripts.Source.General.input_manager as input_manager_m
import Scripts.GUI.Elements.elements as elements
import Scripts.Source.General.data_manager as data_manager_m

import Scripts.GUI.header as header_m
import Scripts.GUI.inspector as inspector_m
import Scripts.GUI.hierarchy as hierarchy_m
import Scripts.Experemental.profiler as profiler_m
import glm
import easygui

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

        self.ask_save_file_before_exit_window = None

    def update_data_in_hierarchy(self):
        self.hierarchy.update_content()

    def select_element_in_hierarchy(self, object_id):
        self.hierarchy.select_element_in_hierarchy(object_id)

    def unselect_data_in_hierarchy(self):
        self.hierarchy.unselect_all_elements_in_content()

    def process_window_resize(self, new_size: glm.vec2):
        self.win_size = new_size
        self.main_block.process_window_resize(new_size)
        self.update_data_in_hierarchy()

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

    def ask_save_file_before_exit(self):
        if self.ask_save_file_before_exit_window:
            self.ask_save_file_before_exit_window.position.relative.center = glm.vec2(0.85)
            self.ask_save_file_before_exit_window.update_position()
            return
        window = elements.Window(f"Ask_save_or_not_window_{len(self.windows)}", self.main_block,
                                 self.win_size,
                                 self, "Warning")
        self.ask_save_file_before_exit_window = window
        window.position.relative_window.size = glm.vec2(0.2, 0.15)
        window.position.relative_window.center = glm.vec2(0.85)
        window.position.evaluate_values_by_relative_window()
        window.init()

        hint_text = elements.Text(f"Save scene before exit?", window.inner_data_block, self.win_size,
                                  f"Save scene before exit?",
                                  font_size=1)
        hint_text.color = glm.vec4(0.1, 0.1, 0.1, 1)
        hint_text.pivot = Pivot.Center
        hint_text.position.relative.center = glm.vec2(0.5, 0.8)
        hint_text.update_position()

        def Save(button, gui, pos):
            file_path = easygui.fileopenbox(title='Save', filetypes='\\*.json')
            if file_path:
                if file_path.endswith(".json"):
                    data_manager_m.DataManager.save_scene(gui.app.scene, file_path)
                    self.app.exit()
                else:
                    window = elements.Window(f"Error_saving_file_window{len(self.gui.windows)}", self.main_block,
                                             gui.win_size,
                                             gui, "Error")
                    window.position.relative_window.size = glm.vec2(0.2, 0.1)
                    window.position.relative_window.center = glm.vec2(0.5)
                    window.position.evaluate_values_by_relative_window()
                    window.init()

                    hint_text = elements.Text(f"Incorrect format selected", window.inner_data_block, self.win_size,
                                              f"Incorrect format selected",
                                              font_size=1)
                    hint_text.color = glm.vec4(0.1, 0.1, 0.1, 1)
                    hint_text.pivot = element_m.Pivot.Center
                    hint_text.position.relative.center = glm.vec2(0.5)
                    hint_text.update_position()

                    window.update_position()
                    self.windows.append(window)

        button_apply = elements.Button("Save", window.inner_data_block, self.win_size, self, 'Save', 1.5,
                                       Save,
                                       color=glm.vec4(0, 0.8, 0.1, 1), text_color=glm.vec4(1))
        button_apply.position.relative.center = glm.vec2(0.65, 0.15)
        button_apply.position.relative.size = glm.vec2(0.3)
        button_apply.update_position()

        def no_save_action(button, gui, pos):
            self.app.exit()

        button_clear = elements.Button("Exit", window.inner_data_block, self.win_size, self, 'Exit', 1.5,
                                       no_save_action,
                                       color=glm.vec4(0.8, 0.1, 0.1, 1), text_color=glm.vec4(1))
        button_clear.position.relative.center = glm.vec2(0.05, 0.15)
        button_clear.position.relative.size = glm.vec2(0.3)
        button_clear.update_position()

        temp = window.close

        def _extension_to_close():
            self.ask_save_file_before_exit_window = None
            temp()

        window.close = _extension_to_close

        window.update_position()

        self.windows.append(window)

    def delete(self):
        self.main_block.delete()
        self.app = None
        self.main_block = None
        self.header = None
        self.inspector = None
        self.hierarchy = None
        self.ask_save_file_before_exit_window = None
