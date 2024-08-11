import Scripts.Source.Components.component as component_m
import Scripts.Source.Components.transformation as transformation_m
import glm

NAME = "Camera"
DESCRIPTION = "Компонент камеры для отрисовки"


class Camera(component_m.Component):
    def __init__(self, near=0.1, far=1000, fov=50, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)

        # right-handed system
        self.forward = glm.vec3(0, 0, -1)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)

        self.fov = fov
        self.near = near
        self.far = far

        # Matrix
        self.m_ortho = None
        self.m_proj = None
        self.m_view = None

        self._transformation = None
        self.aspect_ratio = None
        self.top_bound = None
        self.right_bound = None

    def process_window_resize(self, new_size):
        self.aspect_ratio = new_size[0] / new_size[1]
        self.m_proj = self.get_projection_matrix()
        self.right_bound = self.aspect_ratio * self.top_bound
        self.m_ortho = self.get_orthographic_matrix()

    def init(self, app, rely_object):
        super().init(app, rely_object)
        self.aspect_ratio = app.win_size[0] / app.win_size[1]
        self._transformation = self.rely_object.get_component_by_name(
            'Transformation')  # type: transformation_m.Transformation

        self.top_bound = self.near * glm.tan(glm.radians(self.fov / 2))
        self.right_bound = self.aspect_ratio * self.top_bound

        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()
        self.m_ortho = self.get_orthographic_matrix()

    def apply(self):
        self.m_view = self.get_view_matrix()

    def get_view_matrix(self) -> glm.mat4x4:
        return glm.lookAt(self.transformation.pos, self.transformation.pos + self.forward, self.up)

    def get_projection_matrix(self) -> glm.mat4x4:
        return glm.perspective(glm.radians(self.fov), self.aspect_ratio, self.near, self.far)

    def get_orthographic_matrix(self):
        return glm.ortho(-self.right_bound, self.right_bound, -self.top_bound, self.top_bound, self.near, self.far)

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

    def serialize(self) -> {}:
        return {
            'near': self.near,
            'far': self.far,
            'fov': self.fov,
            'enable': self.enable
        }
