import Scripts.Bin.General.object as object_m
import Scripts.Bin.Components.component as component_m
import Scripts.Bin.Components.transformation as transformation_m
import glm

NAME = 'Light'
DESCRIPTION = 'Источник света'


class Light(component_m.Component):
    def __init__(self, rely_object: object_m.Object, color=(1, 1, 1), enable=True):
        super().__init__(NAME, DESCRIPTION, rely_object, enable)
        self.color = glm.vec3(color)

        self.intensity_ambient = 0.1 * self.color
        self.intensity_diffuse = 0.8 * self.color
        self.intensity_specular = 1.0 * self.color

        self._transformation = rely_object.get_component_by_type(transformation_m.Transformation)

    @property
    def transformation(self):
        if self._transformation is None:
            self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)
        return self._transformation

    @transformation.setter
    def transformation(self, value):
        self._transformation = value


    def delete(self):
        self._transformation = None
        self.rely_object = None

