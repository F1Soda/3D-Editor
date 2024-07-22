import Scripts.Bin.General.object as object_m
import Scripts.Bin.General.general as general
import Scripts.Bin.Components.component as component_m
import Scripts.Bin.Components.transformation as transformation_m
import glm

NAME = "Camera"
DESCRIPTION = "Компонент камеры для отрисовки"

FOV = 50  # deg
NEAR = 0.1
FAR = 100


class Camera(component_m.Component):
    def __init__(self, rely_object: general.Object, app: general.GraphicsEngine, enable=True):
        super().__init__(NAME, DESCRIPTION, rely_object, enable)
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]

        # right-handed system
        self.forward = glm.vec3(0, 0, -1)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)

        # Other
        self._transformation = rely_object.get_component_by_name(
            'Transformation')  # type: transformation_m.Transformation

        # Matrix
        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()

    def update(self):
        self.m_view = self.get_view_matrix()

    def get_view_matrix(self) -> glm.mat4x4:
        return glm.lookAt(self.transformation.pos, self.transformation.pos + self.forward, self.up)

    def get_projection_matrix(self) -> glm.mat4x4:
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)

    @property
    def transformation(self) -> transformation_m.Transformation:
        if self._transformation is None:
            self._transformation = self.rely_object.get_component_by_name('Transformation')
        return self._transformation

    @transformation.setter
    def transformation(self, value: transformation_m.Transformation):
        self._transformation = value

    def delete(self):
        self._transformation = None
        self.rely_object = None
        self.app = None


