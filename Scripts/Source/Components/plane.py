import Scripts.Source.Components.component as component_m
import Scripts.Source.General.utils as utils_m
import Scripts.Source.General.object as object_m
import Scripts.Source.Render.library as library_m
import moderngl as mgl
import glm
import copy

NAME = "Plane"
DESCRIPTION = "Responsible for rendering plane"


class Plane(component_m.Component):
    def __init__(self, color: glm.vec4, p1: object_m.Object, p2: object_m.Object, p3: object_m.Object, save_size=False,
                 enable=True):
        super().__init__(NAME, DESCRIPTION, enable)

        self.color = color
        self.camera_component = None
        self.save_size = save_size
        self.mesh = library_m.meshes['plane']
        self.shader_program = library_m.shader_programs['unlit']

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self._last_p1_pos = copy.copy(self.p1)
        self._last_p2_pos = copy.copy(self.p2)
        self._last_p3_pos = copy.copy(self.p3)

        self._n = glm.vec3()

        self._white_texture = library_m.textures['white']
        self.vao = None

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self.camera_component = self.rely_object.scene.camera_component
        self.vao = app.ctx.vertex_array(self.shader_program.bin_program,
                                        [(self.mesh.vbo, self.mesh.data_format, *self.mesh.attributes)])

        def custom_update_model_matrix():
            p1 = self.p1.transformation.pos
            p2 = self.p2.transformation.pos
            p3 = self.p3.transformation.pos

            self._n = glm.cross(p3 - p1, p2 - p1)
            if glm.length(self._n) == 0:
                self._n = glm.vec3(0, 1, 0)
            self._n /= glm.length(self._n)
            u = utils_m.get_non_parallel_vector(self._n)
            v = glm.cross(self._n, u)
            center = (p1 + p2 + p3) / 3
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
    def p1_pos(self):
        return self.point1.transformation.pos

    @p1_pos.setter
    def p1_pos(self, value):
        self.point1.transformation.pos = value

    @property
    def p2_pos(self):
        return self.point2.transformation.pos

    @p2_pos.setter
    def p2_pos(self, value):
        self.point2.transformation.pos = value

    @property
    def p3_pos(self):
        return self.point3.transformation.pos

    @p3_pos.setter
    def p3_pos(self, value):
        self.point3.transformation.pos = value

    def apply(self):
        if self._last_p1_pos != self.p1 or self._last_p2_pos != self.p2 or self._last_p3_pos != self.p3:
            self._last_p1_pos = copy.copy(self.p1)
            self._last_p2_pos = copy.copy(self.p2)
            self._last_p3_pos = copy.copy(self.p3)
            self.rely_object.transformation.get_model_matrix()

        self.shader_program['color'].write(self.color)
        self.shader_program['m_proj'].write(self.camera_component.m_proj)
        self.shader_program['m_view'].write(self.camera_component.m_view)

        self.shader_program['m_model'].write(self.rely_object.transformation.m_model)
        self._white_texture.use()
        self.shader_program['texture1'] = 0
        self.app.ctx.enable(mgl.BLEND)
        self.vao.render()
        self.app.ctx.disable(mgl.BLEND)

    def serialize(self) -> {}:
        return {
            "color": ('vec', self.color.to_tuple()),
            "p1": ('id', self.p1.id),
            "p2": ('id', self.p2.id),
            "p3": ('id', self.p3.id),
            "save_size": self.save_size,
            'enable': self.enable
        }

    def delete(self):
        self.app = None
        self.camera_component = None
        self.vao.release()
        self._white_texture = None
        self.mesh = None
        self.shader_program = None
        self.point1 = None
        self.point2 = None
        self.point3 = None
        super().delete()
