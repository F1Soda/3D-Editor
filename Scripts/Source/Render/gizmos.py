import Scripts.Source.Render.library as library
import moderngl as mgl
import glm


class Gizmos:
    def __init__(self, ctx: mgl.Context, camera_component):
        self.x_axis = library.get_segment_vao(ctx, (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (1, 0, 0))
        self.y_axis = library.get_segment_vao(ctx, (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (0, 1, 0))
        self.z_axis = library.get_segment_vao(ctx, (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (0, 0, 1))
        self.camera = camera_component
        self.m_model = glm.mat4()
        self.shader = library.shader_programs['word_axis_gizmo']
        if self.shader.get('m_proj'):
            self.shader.get('m_proj').write(self.camera.m_ortho)

    def draw_word_axis(self):
        self.x_axis.render(mgl.LINES)
        self.y_axis.render(mgl.LINES)
        self.z_axis.render(mgl.LINES)

    def update_model_matrix(self):
        m_model = glm.mat4()
        near = self.camera.near
        size = near / 4
        m_model = glm.translate(m_model, self.camera.transformation.pos + self.camera.forward * (
                self.camera.near + 1) + self.camera.right * (self.camera.right_bound - 1/4 * size/self.camera.right_bound) -
                                self.camera.up * (self.camera.top_bound - 1/7 * size/self.camera.top_bound))


        m_model = glm.scale(m_model, (size, size, size))
        self.m_model = m_model

    def update(self):
        if self.shader.get('m_view'):
            self.shader.get('m_view').write(self.camera.get_view_matrix())
        if self.shader.get('m_model'):
            self.update_model_matrix()
            self.shader.get('m_model').write(self.m_model)
