import Scripts.Source.Components.component as component_m
import glm
import copy

NAME = "Transformation"
DESCRIPTION = "Описывает положение, вращение и масштобирование объекта"


class Transformation(component_m.Component):
    def __init__(self, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), moveable=True,
                 enable=True):
        super().__init__(NAME, DESCRIPTION, enable)
        self._pos = glm.vec3(pos)
        self._rot = glm.vec3(rot)
        self._scale = glm.vec3(scale)

        self.m_model = self.get_model_matrix()
        self.moveable = moveable

        self.m_t = None
        self.m_tr = None

    @property
    def m_scale(self):
        return glm.scale(glm.mat4(), self._scale)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        if isinstance(value, glm.vec3):
            self._pos = value
        elif isinstance(value, tuple):
            self._pos = glm.vec3(*value)
        self.m_model = self.get_model_matrix()

    @property
    def rot(self):
        return self._rot

    @rot.setter
    def rot(self, value):
        if isinstance(value, glm.vec3):
            self._rot = value
        elif isinstance(value, tuple):
            self._rot = glm.vec3(*value)
        self.m_model = self.get_model_matrix()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        if isinstance(value, glm.vec3):
            self._scale = value
        elif isinstance(value, tuple):
            self._scale = glm.vec3(*value)
        self.m_model = self.get_model_matrix()

    def get_model_matrix(self):
        rot = glm.vec3([glm.radians(x) for x in self.rot])

        m_model = glm.mat4()

        # position
        m_model = self.m_t = glm.translate(m_model, self.pos)

        # rotation
        m_model = glm.rotate(m_model, rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, rot.y, glm.vec3(0, 1, 0))
        m_model = self.m_tr = glm.rotate(m_model, rot.z, glm.vec3(0, 0, 1))

        # scale
        m_model = glm.scale(m_model, self._scale)

        return m_model

    def update_model_matrix(self):
        self.m_model = self.get_model_matrix()

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self.m_model = self.get_model_matrix()

    def on_change(self):
        self.m_model = self.get_model_matrix()

    def serialize(self) -> {}:
        return {
            'pos': ('vec', self.pos.to_tuple()),
            'rot': ('vec', self.rot.to_tuple()),
            'scale': ('vec', self.scale.to_tuple()),
            'moveable': self.moveable,
            'enable': self.enable
        }
