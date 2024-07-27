import Scripts.Source.Render.library as library
import moderngl as mgl
import glm
import Scripts.Source.General.index_manager as index_manager_m


class Gizmos:
    class Segment:
        def __init__(self, ctx, start, end, color, camera, size=3.0):
            self.id = index_manager_m.IndexManager.get_id()
            self.ctx = ctx
            self.start = glm.vec3(*start)
            self._size = self.default_size = size
            self.end = glm.vec3(*end)
            self._color = glm.vec3(color)
            self.shader = library.shader_programs['word_axis_gizmo']
            self.shader['color'].write(self._color)
            self.vao = library.get_segment_vao(ctx, start, end, color)
            self.camera = camera

        @property
        def size(self):
            return self._size

        @size.setter
        def size(self, value):
            self._size = value
            self.ctx.line_width = value

        @property
        def color(self):
            return self._color

        @color.setter
        def color(self, value):
            if isinstance(value, tuple):
                self._color = glm.vec3(value)
            else:
                self._color = value
            self.shader['color'].write(self._color)

        def set_default_size(self):
            self.size = self.default_size

        def draw(self, m_model, m_proj=None, m_view=None):
            if self.shader.get('m_view'):
                self.shader.get('m_view').write(self.camera.get_view_matrix() if m_view is None else m_view)
            if self.shader.get('m_model'):
                self.shader.get('m_model').write(m_model)
            if self.shader.get('m_proj'):
                self.shader.get('m_proj').write(self.camera.m_proj if m_proj is None else m_proj)
            self.ctx.line_width = self.size
            self.shader['color'].write(self._color)
            self.vao.render(mgl.LINES)

        def delete(self):
            self.ctx = None
            self.vao.release()
            self.vao = None
            self.shader = None

    def __init__(self, ctx: mgl.Context, camera_component):
        self.ctx = ctx
        self.camera = camera_component
        self.x_axis = Gizmos.Segment(ctx, (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (1, 0, 0), self.camera)
        self.y_axis = Gizmos.Segment(ctx, (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (0, 1, 0), self.camera)
        self.z_axis = Gizmos.Segment(ctx, (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (0, 0, 1), self.camera)
        self.shader = library.shader_programs['word_axis_gizmo']

    def draw_word_axis(self):
        self.x_axis.draw(m_proj=self.camera.m_ortho, m_model=self.get_model_matrix_for_world_axis())
        self.y_axis.draw(m_proj=self.camera.m_ortho, m_model=self.get_model_matrix_for_world_axis())
        self.z_axis.draw(m_proj=self.camera.m_ortho, m_model=self.get_model_matrix_for_world_axis())

    def get_model_matrix_for_world_axis(self):
        m_model = glm.mat4()
        near = self.camera.near
        size = near / 4
        m_model = glm.translate(m_model, self.camera.transformation.pos + self.camera.forward * (
                self.camera.near + 1) + self.camera.right * (
                                        self.camera.right_bound - 1 / 4 * size / self.camera.right_bound) -
                                self.camera.up * (self.camera.top_bound - 1 / 7 * size / self.camera.top_bound))

        m_model = glm.scale(m_model, (size, size, size))
        return m_model
