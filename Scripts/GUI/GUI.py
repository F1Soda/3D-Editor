import Scripts.GUI.Elements.block as block_m
import Scripts.GUI.Elements.text as text_m
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
    def __init__(self, app, screen_size):
        self.app = app
        self.screen_size = glm.vec2(screen_size)
        self.aspect_ratio = screen_size[0] / screen_size[1]
        self.main_block = block_m.Block("Main Block", None, glm.vec2(0, 0), size=self.screen_size,
                                        win_size=self.screen_size)
        inspector = block_m.Block("Inspector", self.main_block,
                                  glm.vec2(LEFT_INSPECTOR_CORNER, DIVISION_BETWEEN_INSPECTOR_AND_HIERARCHY),
                                  color=(0.1, 0.3, 0.1, 0.5),
                                  win_size=self.screen_size)
        hierarchy = block_m.Block("Hierarchy", self.main_block, relative_left_bottom=glm.vec2(LEFT_INSPECTOR_CORNER, 0),
                                  relative_right_top=glm.vec2(1, DIVISION_BETWEEN_INSPECTOR_AND_HIERARCHY),
                                  color=(0.3, 0.1, 0.1, 0.5),
                                  win_size=self.screen_size)
        header = block_m.Block("Header", self.main_block, relative_left_bottom=glm.vec2(0, HEADER_BOTTOM),
                               relative_right_top=glm.vec2(LEFT_INSPECTOR_CORNER, 1),
                               color=(1, 1, 1, 0.5),
                               win_size=self.screen_size)

        # sub_header = block_m.Block("sub_header", header,
        #                            relative_left_bottom=glm.vec2(0.1),
        #                            relative_right_top=glm.vec2(0.9),
        #                            color=(1, 1, 1, 0.5),
        #                            win_size=self.screen_size)

        text_size = 0.02
        rlb = glm.vec2(0.5, 0.95)

        rrt = rlb + glm.vec2(text_size, text_size * self.aspect_ratio)

        # background = block_m.Block("Headersss", self.main_block,
        #                            relative_left_bottom=rlb,
        #                            relative_right_top=rrt,
        #                            color=(0.5, 0.5, 0.5, 1),
        #                            win_size=self.screen_size
        #                            )

        text_inspector = text_m.Text("Text Header Inspector", "Inspector", inspector,
                                     relative_left_bottom=rlb,
                                     relative_right_top=rrt,
                                     win_size=self.screen_size,
                                     centered_x=True,
                                     centered_y=True,
                                     )

        rlb = glm.vec2(0.5, 0.95)
        rrt = rlb + glm.vec2(text_size, text_size * self.aspect_ratio)

        text_hierarchy = text_m.Text("Text Header Hierarchy", "Hierarchy", hierarchy,
                                     relative_left_bottom=rlb,
                                     relative_right_top=rrt,
                                     win_size=self.screen_size,
                                     centered_x=True,
                                     centered_y=True,
                                     )

        rlb = glm.vec2(0.5, 0.5)
        rrt = rlb + glm.vec2(text_size, text_size * self.aspect_ratio)

        self.text_hierarchy = text_m.Text("Text Header Header", "3D Editor", header,
                                          relative_left_bottom=rlb,
                                          relative_right_top=rrt,
                                          win_size=self.screen_size,
                                          centered_x=True,
                                          centered_y=True,
                                          )

    def process_window_resize(self, new_size: glm.vec2):
        self.screen_size = new_size
        self.main_block.process_window_resize(new_size)

    def render(self):
        self.text_hierarchy.color = utils_m.rainbow_color(self.app.time)
        self.main_block.render()
