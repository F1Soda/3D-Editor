import copy

import Scripts.GUI.Elements.block as block_m
import Scripts.GUI.Elements.text as text_m
import Scripts.Source.General.input_manager as input_manager_m
import Scripts.GUI.Elements.button as button_m
import Scripts.GUI.Elements.content as content_m
import Scripts.Source.General.utils as utils_m
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
HEADER_BOTTOM = 0.95
LEFT_INSPECTOR_CORNER = 0.75
DIVISION_BETWEEN_INSPECTOR_AND_HIERARCHY = 0.5


class GUI:
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

        self._init_main_block()

        #
        # # console = block_m.Block("Console", self.main_block,
        # #                         relative_left_bottom=glm.vec2(0, 0),
        # #                         relative_right_top=glm.vec2(0.2, 0.3),
        # #                         color=(0.1, 0.1, 0.1, 0.5),
        # #                         win_size=self.screen_size)

        self.last_clicked_element = None
        self.active_sub_menu = None

    def _init_main_block(self):
        self.main_block = block_m.Block("Main Block", None, self.win_size)

        self.main_block.position.relative_window.right_top = glm.vec2(1)
        self.main_block.position.evaluate_values_by_relative_window()

        # content_element = block_m.Block("Element_1", None, self.win_size, (1, 1, 1, 0.5))
        # content_element.position.relative_window.size = glm.vec2(0.1, 0.05)
        # content_element.position.evaluate_values_by_relative_window()
        # content.add(content_element)

        self._init_inspector()
        self._init_hierarchy()
        self._init_header()

    def _init_inspector(self):
        inspector = block_m.Block("Inspector", self.main_block, self.win_size, (0.1, 0.3, 0.1, 0.5))

        inspector.position.relative.left_bottom = glm.vec2(LEFT_INSPECTOR_CORNER,
                                                           DIVISION_BETWEEN_INSPECTOR_AND_HIERARCHY)
        inspector.position.relative.right_top = glm.vec2(1)
        inspector.position.evaluate_values_by_relative()
        text_header = text_m.Text("Header Text: `Inspector`", inspector, self.win_size,
                                  "Inspector",
                                  centered_x=True,
                                  centered_y=True,
                                  font_size=2,
                                  space_between=0.1
                                  )
        text_header.position.relative.center = glm.vec2(0.5, 0.95)
        text_header.position.evaluate_values_by_relative()

    def _init_hierarchy(self):
        self.hierarchy = block_m.Block("Hierarchy", self.main_block, self.win_size, color=(0.3, 0.1, 0.1, 0.5))

        self.hierarchy.position.relative.left_bottom = glm.vec2(LEFT_INSPECTOR_CORNER, 0)
        self.hierarchy.position.relative.right_top = glm.vec2(1, DIVISION_BETWEEN_INSPECTOR_AND_HIERARCHY)
        self.hierarchy.position.evaluate_values_by_relative()
        text_header = text_m.Text("Header Text: 'Hierarchy'", self.hierarchy, self.win_size,
                                  "Hierarchy",
                                  centered_x=True,
                                  centered_y=True,
                                  font_size=2,
                                  space_between=0.1
                                  )
        text_header.position.relative.center = glm.vec2(0.5, 0.95)
        text_header.position.evaluate_values_by_relative()

        def custom_right_click_handle(pos: glm.vec2):
            self.hierarchy_sub_menu.active = True
            self.hierarchy_sub_menu.position.absolute.center = glm.vec2(
                pos.x - self.hierarchy_sub_menu.position.absolute.size.x / 2,
                pos.y + self.hierarchy_sub_menu.position.absolute.size.y / 2
            )
            self.hierarchy_sub_menu.position.evaluate_values_by_absolute()
            self.hierarchy_sub_menu.update_position()
            self.active_sub_menu = self.hierarchy_sub_menu
            self.last_clicked_element = self.hierarchy_sub_menu

        def custom_right_hold_handle(pos: glm.vec2):
            return True

        self.hierarchy.handle_right_click = custom_right_click_handle
        self.hierarchy.handle_right_hold = custom_right_hold_handle

        self._init_right_click_sub_menu()

    def _init_right_click_sub_menu(self):
        self.hierarchy_sub_menu = content_m.Content("Sub Menu Hierarchy", self.hierarchy, self.win_size, (1, 1, 1, 0.5))
        self.hierarchy_sub_menu.position.relative.center = glm.vec2(0.5)
        self.hierarchy_sub_menu.position.evaluate_values_by_relative()

        content_element = block_m.Block("Element_1", None, self.win_size, (1, 1, 1, 0.5))
        content_element.position.relative_window.size = glm.vec2(0.1, 0.05)
        content_element.position.evaluate_values_by_relative_window()

        crete_cube = button_m.Button("Create cube Button", content_element, self.win_size, self,
                                     "Create Cube",
                                     action=None,
                                     color=glm.vec4(0.5, 0.5, 0.5, 1),
                                     text_size=1
                                     )

        crete_cube.position.relative.left_bottom = glm.vec2(0.1)
        crete_cube.position.relative.right_top = glm.vec2(0.9)
        crete_cube.position.evaluate_values_by_relative()
        crete_cube.update_position()

        self.hierarchy_sub_menu.add(content_element)

    def _init_header(self):
        header = block_m.Block("Header", self.main_block, self.win_size, color=(1, 1, 1, 0.7))

        header.position.relative.left_bottom = glm.vec2(0, HEADER_BOTTOM)
        header.position.relative.right_top = glm.vec2(LEFT_INSPECTOR_CORNER, 1)
        header.position.evaluate_values_by_relative()
        self.text_header = text_m.Text("Header Text: 'Header'", header, self.win_size,
                                       "3D Editor",
                                       centered_x=True,
                                       centered_y=True,
                                       font_size=2,
                                       space_between=0.1
                                       )
        self.text_header.position.relative.center = glm.vec2(0.5, 0.5)
        self.text_header.update_position()

        rlb = glm.vec2(0.005, 0.1)
        rrt = glm.vec2(0.05, 1 - 0.1)

        save_button = button_m.Button("Save Button", header, self.win_size, self,
                                      "Save",
                                      action=None,
                                      color=glm.vec4(0, 0.7, 0, 1),
                                      text_color=glm.vec4(1, 1, 1, 1),
                                      text_size=1
                                      )
        save_button.position.relative.left_bottom = copy.copy(rlb)
        save_button.position.relative.right_top = copy.copy(rrt)
        save_button.position.evaluate_values_by_relative()
        save_button.update_position()

        rlb = rlb + glm.vec2(rrt.x + rlb.x, 0)
        rrt = rrt + glm.vec2(rrt.x, 0)

        load_button = button_m.Button("Load Button", header, self.win_size, self,
                                      "Load",
                                      action=None,
                                      color=glm.vec4(0.7, 0.7, 0, 1),
                                      text_color=glm.vec4(1, 1, 1, 1),
                                      text_size=1
                                      )
        load_button.position.relative.left_bottom = copy.copy(rlb)
        load_button.position.relative.right_top = copy.copy(rrt)
        load_button.position.evaluate_values_by_relative()
        load_button.update_position()

        rrt = glm.vec2(0.995, rrt.y)
        rlb = glm.vec2(rrt.x - 0.035, 0.1)

        def render_mode_button_action(button, gui):
            button.button_text = "W" if button.button_text == "S" else "S"
            gui.app.scene.change_render_mode()

        render_mode_button = button_m.Button("Render Mode Button", header, self.win_size, self,
                                             "S",
                                             action=render_mode_button_action,
                                             color=glm.vec4(0.7, 0.7, 0, 1),
                                             text_color=glm.vec4(1, 1, 1, 1),
                                             text_size=2
                                             )

        render_mode_button.position.relative.left_bottom = copy.copy(rlb)
        render_mode_button.position.relative.right_top = copy.copy(rrt)
        render_mode_button.position.evaluate_values_by_relative()
        render_mode_button.update_position()

    def process_window_resize(self, new_size: glm.vec2):
        self.win_size = new_size
        self.main_block.process_window_resize(new_size)

    def render(self):
        self.text_header.color = utils_m.rainbow_color(self.app.time)
        self.main_block.render()

    def find_clicked_element(self, mouse_pos: glm.vec2):
        if self.active_sub_menu and self.active_sub_menu.position.check_if_clicked(mouse_pos):
            return self.active_sub_menu.find_clicked_element(mouse_pos)
        return self.main_block.find_clicked_element(mouse_pos)

    def handle_left_click(self, mouse_pos: glm.vec2):
        element = self.find_clicked_element(mouse_pos)
        if self.active_sub_menu:
            self.active_sub_menu.active = False
            self.active_sub_menu = None

        if element.name == "Main Block":
            self.last_clicked_element = None
            return False
        else:
            element.handle_left_click(mouse_pos)
            print(element.name)
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
