import copy

import glm

import Scripts.GUI.Elements.element as element_m
import Scripts.GUI.library as library_m
import Scripts.Source.General.data_manager as data_manager_m

FONT_SIZE_SCALE = 0.01


class Text(element_m.Element):
    def __init__(self, name, rely_element, win_size: glm.vec2,
                 text,
                 font_size=1,
                 color=(1, 1, 1, 1),
                 space_between=0.1,
                 centered_x=False,
                 centered_y=False,
                 ):
        super().__init__(name, rely_element, win_size)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.space_between = space_between
        self.centered_x = centered_x
        self.centered_y = centered_y

        # Rendering
        self.vao = library_m.primitives_vao['textured_quad']
        self.font_texture = library_m.textures['font']  # ['font_boundaries']
        self.shader_program = library_m.shader_programs['TextGUI']
        self.shader_program['letter_size'] = 16.0
        self.shader_program['color'].write(glm.vec4(1))

        self.abs_quad_size = FONT_SIZE_SCALE * glm.vec2(font_size,
                                                        font_size * self.win_aspect_ratio) * self.win_size
        self.relative_quad_size = self.abs_quad_size / self.win_size

        # List with width for all letters
        self.letters_width = data_manager_m.DataManager.letters_width

        # Properties
        self._relative_size = None

    def process_window_resize(self, new_size: glm.vec2):
        self.abs_quad_size = self.abs_quad_size * new_size/self.win_size
        super().process_window_resize(new_size)
        # self.size = self.win_size * (self.relative_right_top - self.relative_left_bottom)

    def evaluate_text_size(self):
        size = glm.vec2(0, self.abs_quad_size.y)
        for char in self.text:
            index = ord(char)
            y = index // 16
            x = index % 16
            letter_width = self.letters_width[y * 16 + x]
            size.x += self.abs_quad_size.x * (letter_width + self.space_between)
        past_center = copy.copy(self.position.relative.center)
        self.position.relative.size = size / self.rely_element.position.absolute.size
        self.position.relative.center = past_center

    def update_position(self):
        self.evaluate_text_size()
        self.position.evaluate_values_by_relative()

    def render(self):
        self.shader_program['color'] = self.color
        self.shader_program['texture_0'] = 0
        self.font_texture.use()

        m_gui = copy.deepcopy(self.position.m_gui)
        m_gui[0][0] = self.relative_quad_size.x

        for char in self.text:
            index = ord(char)
            y = index // 16
            x = index % 16

            # Offset In Texture
            offset = glm.vec2(x * 1 / 16, (31 - y) * 1 / 16)
            self.shader_program['offset'].write(offset)

            # M_GUI
            self.shader_program['m_gui'].write(m_gui)

            self.vao.render()

            # Shift Quad
            letter_width = self.letters_width[y * 16 + x]
            m_gui[3][0] += self.relative_quad_size.x * (letter_width + self.space_between)

    @staticmethod
    def precalculate_block_height(text, text_size):
        pass

    def delete(self):
        self.vao = None
        self.shader_program = None
        super().delete()
