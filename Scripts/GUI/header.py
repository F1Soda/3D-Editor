import Scripts.GUI.Elements.element as element_m
import Scripts.GUI.Elements.elements as elements
import Scripts.Source.General.utils as utils_m
import copy
import glm


class Header(element_m.Element):
    def __init__(self, gui, main_block):
        super().__init__('Header', main_block, gui.win_size)
        self.gui = gui
        self.main_block = main_block

        self.main_block.elements.append(self)

        self.position.relative.left_bottom = glm.vec2(0, gui.HEADER_BOTTOM)
        self.position.relative.right_top = glm.vec2(gui.LEFT_INSPECTOR_CORNER, 1)

        background = elements.Block("Background", self, self.win_size, color=(0.5, 0.5, 0.7, 0.7))
        background.position.relative.right_top = glm.vec2(1)
        self.update_position()

        self.text_header = elements.Text("Header Text", background, self.win_size,
                                         "3D Editor",
                                         font_size=2,
                                         space_between=0.1,
                                         pivot=element_m.Pivot.Center
                                         )
        self.text_header.position.relative.center = glm.vec2(0.5, 0.5)

        rlb = glm.vec2(0.005, 0.1)
        rrt = glm.vec2(0.05, 1 - 0.1)

        save_button = elements.Button("Save Button", background, self.win_size, self.gui,
                                      "Save",
                                      action=None,
                                      color=glm.vec4(0, 0.7, 0, 1),
                                      text_color=glm.vec4(1, 1, 1, 1),
                                      text_size=1
                                      )
        save_button.position.relative.left_bottom = copy.copy(rlb)
        save_button.position.relative.right_top = copy.copy(rrt)

        rlb = rlb + glm.vec2(rrt.x + rlb.x, 0)
        rrt = rrt + glm.vec2(rrt.x, 0)

        load_button = elements.Button("Load Button", background, self.win_size, self.gui,
                                      "Load",
                                      action=None,
                                      color=glm.vec4(0.7, 0.7, 0, 1),
                                      text_color=glm.vec4(1, 1, 1, 1),
                                      text_size=1
                                      )
        load_button.position.relative.left_bottom = copy.copy(rlb)
        load_button.position.relative.right_top = copy.copy(rrt)
        load_button.position.evaluate_values_by_relative()

        rrt = glm.vec2(0.995, rrt.y)
        rlb = glm.vec2(rrt.x - 0.035, 0.1)

        def render_mode_button_action(button, gui, pos):
            button.button_text = "W" if button.button_text == "S" else "S"
            gui.app.scene.change_render_mode()

        render_mode_button = elements.Button("Render Mode Button", background, self.win_size, self.gui,
                                             "S",
                                             action=render_mode_button_action,
                                             color=glm.vec4(0.7, 0.7, 0, 1),
                                             text_color=glm.vec4(1, 1, 1, 1),
                                             text_size=2
                                             )

        render_mode_button.position.relative.left_bottom = copy.copy(rlb)
        render_mode_button.position.relative.right_top = copy.copy(rrt)
        render_mode_button.position.evaluate_values_by_relative()

        def grid_off_on_action(button, gui, pos):
            button.button_text = "Grid: ON" if button.button_text == "Grid: OFF" else "Grid: OFF"
            gui.app.gizmos.draw_grid_and_center_system = not gui.app.gizmos.draw_grid_and_center_system
            pass

        grid_on_off_button = elements.Button("Grid off on button", background, self.win_size, self.gui,
                                             "Grid: ON",
                                             action=grid_off_on_action,
                                             color=glm.vec4(0.0, 0.7, 0.7, 1),
                                             text_color=glm.vec4(1, 1, 1, 1),
                                             text_size=2
                                             )

        grid_on_off_button.position.relative.size = glm.vec2(0.15, 0.8)
        grid_on_off_button.position.relative.center = glm.vec2(0.87, 0.5)
        grid_on_off_button.position.evaluate_values_by_relative()

        self.update_position()

    def render(self):
        if self.text_header:
            self.text_header.color = utils_m.rainbow_color(self.gui.app.time)
        super().render()
