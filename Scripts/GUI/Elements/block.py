import Scripts.GUI.Elements.element as element_m
import Scripts.GUI.library as library_m
import glm
import moderngl as mgl


class Block(element_m.Element):
    def __init__(self, name, rely_element, relative_left_bottom, win_size, relative_right_top=glm.vec2(1, 1),
                 size: glm.vec2 = None,
                 color=(0, 0, 0, 0)):
        super().__init__(name, rely_element, relative_left_bottom, win_size, relative_right_top, size)
        self.vao = library_m.primitives_vao['quad']  # type: mgl.VertexArray
        self.shader_program = library_m.shader_programs['BlockGUI']
        self.color = glm.vec4(color)

    def render(self):
        self.update_m_gui()
        self.shader_program['color'].write(self.color)
        self.shader_program['m_gui'].write(self.m_gui)
        self.vao.render()
        super().render()

    def delete(self):
        self.vao = None
        self.shader_program = None
        super().delete()
