import Scripts.Bin.Components.component as component_m
import glm

NAME = "Transformation"
DESCRIPTION = "Описывает положение, вращение и масштобирование объекта"


class Transformation(component_m.Component):
    def __init__(self, rely_object, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), enable=True):
        super().__init__(NAME, DESCRIPTION, rely_object, enable)
        self._pos = glm.vec3(*pos)
        self._rot = glm.vec3(*rot)
        self._scale = glm.vec3(*scale)
        self.m_model = self.get_model_matrix()

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
        m_model = glm.translate(m_model, self.pos)

        # rotation
        m_model = glm.rotate(m_model, rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, rot.z, glm.vec3(0, 0, 1))

        # scale
        m_model = glm.scale(m_model, self._scale)

        return m_model

    def on_change(self):
        self.m_model = self.get_model_matrix()
