import Scripts.Source.Components.component as component_m
import Scripts.Source.General.object as object_m
import Scripts.Source.General.utils as utils_m
import Scripts.Source.Render.library as library_m
import moderngl as mgl
import glm
import copy

NAME = "Plane"
DESCRIPTION = "Responsible for rendering plane"


class Plane(component_m.Component):
    def __init__(self, rely_object: object_m.Object, ctx, color, p1, p2, p3, camera_component, save_size=False):
        super().__init__(NAME, DESCRIPTION, rely_object)
        self.ctx = ctx
        self.color = color
        self.camera_component = camera_component
        self.save_size = save_size
        self.mesh = library_m.meshes['plane']
        self.shader_program = library_m.shader_programs['unlit']
        self.vao = ctx.vertex_array(self.shader_program.bin_program,
                                    [(self.mesh.vbo, self.mesh.data_format, *self.mesh.attributes)])

        self.point1 = p1
        self.point2 = p2
        self.point3 = p3

        self._last_p1 = copy.copy(p1)
        self._last_p2 = copy.copy(p2)
        self._last_p3 = copy.copy(p3)

        self._n = glm.vec3()

        self._white_texture = library_m.textures['white']

        def custom_update_model_matrix():
            self._n = glm.cross(self.p3 - self.p1, self.p2 - self.p1)
            if glm.length(self._n) == 0:
                self._n = glm.vec3(0, 1, 0)
            self._n /= glm.length(self._n)
            u = utils_m.get_non_parallel_vector(self._n)
            v = glm.cross(self._n, u)
            center = (self.p1 + self.p2 + self.p3) / 3
            T = glm.mat4(glm.vec4(1, 0, 0, 0), glm.vec4(0, 1, 0, 0), glm.vec4(0, 0, 1, 0),
                         glm.vec4(center.x, center.y, center.z, 1))
            R = glm.mat4x4(glm.vec4(u, 0), glm.vec4(self._n, 0), glm.vec4(v, 0), glm.vec4(0, 0, 0, 1))
            S = self.rely_object.transformation.m_scale
            res = self.rely_object.transformation.m_model = T * R * S
            self.rely_object.transformation.m_model = res
            return res

        self.rely_object.transformation.moveable = False

        self.rely_object.transformation.get_model_matrix = custom_update_model_matrix

    @property
    def n(self):
        return self._n

    @property
    def p1(self):
        return self.point1.transformation.pos

    @p1.setter
    def p1(self, value):
        self.point1.transformation.pos = value

    @property
    def p2(self):
        return self.point2.transformation.pos

    @p2.setter
    def p2(self, value):
        self.point2.transformation.pos = value

    @property
    def p3(self):
        return self.point3.transformation.pos

    @p3.setter
    def p3(self, value):
        self.point3.transformation.pos = value

    def apply(self):
        if self._last_p1 != self.p1 or self._last_p2 != self.p2 or self._last_p3 != self.p3:
            self._last_p1 = copy.copy(self.p1)
            self._last_p2 = copy.copy(self.p2)
            self._last_p3 = copy.copy(self.p3)
            self.rely_object.transformation.get_model_matrix()

        self.shader_program['color'].write(self.color)
        self.shader_program['m_proj'].write(self.camera_component.m_proj)
        self.shader_program['m_view'].write(self.camera_component.m_view)

        self.shader_program['m_model'].write(self.rely_object.transformation.m_model)
        self._white_texture.use()
        self.shader_program['texture1'] = 0
        self.ctx.enable(mgl.BLEND)
        self.vao.render()
        self.ctx.disable(mgl.BLEND)

    def delete(self):
        self.ctx = None
        self.camera_component = None
        self.vao.release()
        self._white_texture = None
        self.mesh = None
        self.shader_program = None
        self.point1 = None
        self.point2 = None
        self.point3 = None
        super().delete()
