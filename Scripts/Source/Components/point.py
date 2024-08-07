import Scripts.Source.Components.component as component_m
import Scripts.Source.General.object as object_m
import Scripts.Source.Render.gizmos as gizmos_m
import glm

NAME = "Point"
DESCRIPTION = "Responsible for rendering point"


class Point(component_m.Component):
    def __init__(self, rely_object: object_m.Object, ctx, color, size, camera_component, save_size=True):
        super().__init__(NAME, DESCRIPTION, rely_object)
        self.gizmos_point = gizmos_m.Gizmos.Point(ctx, glm.vec3(), color, camera_component, size, save_size)

    def apply(self):
        self.gizmos_point.pos = self.rely_object.transformation.pos
        self.gizmos_point.draw()

    def delete(self):
        self.gizmos_point.delete()
        super().delete()
