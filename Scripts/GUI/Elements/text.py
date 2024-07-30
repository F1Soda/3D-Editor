import glm

import Scripts.GUI.Elements.element as element_m
import Scripts.GUI.library as library_m
import Scripts.Source.General.data_manager as data_manager_m


class Text(element_m.Element):
    def __init__(self, name, text, rely_element, relative_left_bottom, win_size, relative_right_top=glm.vec2(1, 1),
                 size: glm.vec2 = None,
                 color=(1, 1, 1, 1),
                 stretch=False,
                 space_between=0.1,
                 centered_x=False,
                 centered_y=False,
                 ):
        super().__init__(name, rely_element, relative_left_bottom, win_size, relative_right_top, size)
        self.text = text
        self.centered_x = centered_x
        self.centered_y = centered_y
        self.size = self.win_size * (self.relative_right_top - self.relative_left_bottom)
        self.stretch = stretch
        self.vao = library_m.primitives_vao['textured_quad']
        self.font_texture = library_m.textures['font']  # ['font_boundaries']
        self.color = color
        self.shader_program = library_m.shader_programs['TextGUI']
        self.shader_program['letter_size'] = 16.0
        self.shader_program['color'].write(glm.vec4(1))
        self.char_size_in_texture = 1 / 16.0
        self.quad_size = self.size / self.win_size / (len(text) if stretch else 1)
        self.space_between = space_between
        self.letter_width = data_manager_m.DataManager.letter_width
        self._relative_size = None

    def process_window_resize(self, new_size: glm.vec2):
        super().process_window_resize(new_size)
        self.size = self.win_size * (self.relative_right_top - self.relative_left_bottom)

    @property
    def relative_size(self):
        if self._relative_size is not None:
            return self._relative_size
        self._relative_size = glm.vec2(0, self.quad_size.y)
        for char in self.text:
            index = ord(char)
            y = index // 16
            x = index % 16
            letter_width = self.letter_width[y * 16 + x]
            self._relative_size.x += self.quad_size.x * (letter_width + self.space_between)
        return self._relative_size

    def render(self):
        self.shader_program['color'] = self.color
        self.update_m_gui(self.size)
        if self.centered_x:
            self.m_gui[3][0] -= self.relative_size.x / 2
        if self.centered_y:
            self.m_gui[3][1] -= self.relative_size.y / 2

        self.shader_program['texture_0'] = 0
        self.font_texture.use()
        m_gui_c0r0 = self.m_gui[0][0]
        self.shader_program['m_gui'].write(glm.mat4())
        for char in self.text:
            index = ord(char)
            y = index // 16
            x = index % 16
            offset = glm.vec2(x * self.char_size_in_texture, (31 - y) * self.char_size_in_texture)
            self.shader_program['offset'].write(offset)
            letter_width = self.letter_width[y * 16 + x]
            if self.stretch:
                self.m_gui[0][0] /= len(self.text)
            self.shader_program['m_gui'].write(self.m_gui)
            self.m_gui[0][0] = m_gui_c0r0
            self.vao.render()
            if self.stretch:
                self.m_gui[3][0] += self.quad_size.x
            else:
                self.m_gui[3][0] += self.quad_size.x * (letter_width + self.space_between)

    def delete(self):
        self.vao = None
        self.shader_program = None
        super().delete()
