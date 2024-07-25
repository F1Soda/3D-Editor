import Scripts.Source.General.object as object_m
import Scripts.Source.General.general as general
import Scripts.Source.Components.component as component_m
import Scripts.Source.Components.transformation as transformation_m
import glm

NAME = "Camera"
DESCRIPTION = "Компонент камеры для отрисовки"


class Camera(component_m.Component):
    def __init__(self, rely_object: general.Object, app: general.GraphicsEngine, near=0.1, far=1000, fov=50,
                 enable=True):
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
        self.fov = fov
        self.near = near
        self.far = far
        self.top_bound = self.near * glm.tan(glm.radians(fov))
        self.right_bound = self.aspect_ratio * self.top_bound

        # Matrix
        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()
        self.m_ortho = self.get_orthographic_matrix()

    def update(self):
        self.m_view = self.get_view_matrix()

    def get_view_matrix(self) -> glm.mat4x4:
        return glm.lookAt(self.transformation.pos, self.transformation.pos + self.forward, self.up)

    def get_projection_matrix(self) -> glm.mat4x4:
        return glm.perspective(glm.radians(self.fov), self.aspect_ratio, self.near, self.far)

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

    def get_orthographic_matrix(self):
        return glm.ortho(-self.right_bound, self.right_bound, -self.top_bound, self.top_bound, self.near, self.far)
