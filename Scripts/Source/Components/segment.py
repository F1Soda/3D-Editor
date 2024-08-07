import Scripts.Source.Components.component as component_m
import Scripts.Source.General.object as object_m
import Scripts.Source.Render.gizmos as gizmos_m

NAME = "Segment"
DESCRIPTION = "Responsible for rendering segment"


class Segment(component_m.Component):
    def __init__(self, rely_object: object_m.Object, point_1, point_2, ctx, color, size, camera_component,
                 save_size=True):
        super().__init__(NAME, DESCRIPTION, rely_object)
        self.gizmos_segment = gizmos_m.Gizmos.SegmentByPoints(ctx, point_1, point_2, color, camera_component, size,
                                                              save_size)

    def apply(self):
        self.gizmos_segment.draw()

    def delete(self):
        self.gizmos_segment.delete()
        super().delete()
