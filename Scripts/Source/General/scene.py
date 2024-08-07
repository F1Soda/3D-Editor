import glm

import Scripts.Source.General.object_creator as object_creator_m
import Scripts.Source.Render.gizmos as gizmos_m


class Scene:
    def __init__(self, app, gui):
        self.app = app
        self.ctx = self.app.ctx
        self.objects = {}
        self.transform_axis_gizmo = {}
        self.gizmo_objects = {}

        self.light = None
        self.camera = None
        self.camera_component = None

        self.opaque_renderer = []
        self.transparency_renderer = []

        self.gui = gui

    def change_render_mode(self):
        for obj in self.objects.values():
            renderer = obj.get_component_by_name("Renderer")
            if renderer:
                renderer.change_render_mode()

    def load(self):
        self.light = object_creator_m.ObjectCreator.create_light()
        self.objects[self.light.id] = self.light
        self.camera = object_creator_m.ObjectCreator.create_camera()
        self.camera_component = self.camera.get_component_by_name("Camera")

        self.init_gizmo()
        self.init_scene()

    def add_object(self, obj):
        self.objects[obj.id] = obj
        self.gui.update_data_in_hierarchy()

    def init_scene(self):
        tetrahedron = object_creator_m.ObjectCreator.create_tetrahedron('blue')
        tetrahedron.transformation.pos = (5, 0, 5)
        self.objects[tetrahedron.id] = tetrahedron

        octahedron = object_creator_m.ObjectCreator.create_octahedron('red')
        octahedron.transformation.pos = (5, 0, 3)
        self.objects[octahedron.id] = octahedron

        cube = object_creator_m.ObjectCreator.create_cube('green')
        cube.transformation.pos = (5, 0, 1)
        self.objects[cube.id] = cube

        p1 = object_creator_m.ObjectCreator.create_point(glm.vec4(1, 0, 0, 1), size=200)
        p1.transformation.pos = glm.vec3(3, 0, 0)
        self.objects[p1.id] = p1

        p2 = object_creator_m.ObjectCreator.create_point(glm.vec4(0, 1, 0, 1), size=200)
        p2.transformation.pos = glm.vec3(0, 3, 0)
        self.objects[p2.id] = p2

        test_segment = object_creator_m.ObjectCreator.create_segment(glm.vec4(0.6, 0.1, 0.5, 1), p1, p2)
        self.objects[test_segment.id] = test_segment

        p3 = object_creator_m.ObjectCreator.create_point(glm.vec4(0, 0, 1, 1), size=200)
        p3.transformation.pos = glm.vec3(0, 0, 8)
        self.objects[p3.id] = p3

        p4 = object_creator_m.ObjectCreator.create_point(glm.vec4(1, 0, 1, 1), size=200)
        p4.transformation.pos = glm.vec3(0, 2, 10)
        self.objects[p4.id] = p4

        p5 = object_creator_m.ObjectCreator.create_point(glm.vec4(0, 1, 1, 1), size=200)
        p5.transformation.pos = glm.vec3(3, -2, 8)
        self.objects[p5.id] = p5

        plane_by_3_points = object_creator_m.ObjectCreator.create_plane_by_3_points(p3, p4, p5)
        self.objects[plane_by_3_points.id] = plane_by_3_points

    def init_gizmo(self):
        axis = gizmos_m.Gizmos.WordAxisGizmo(self.ctx, (0, 0, 0), (1, 0, 0), (1, 0, 0), self.camera_component, size=3)
        self.transform_axis_gizmo[axis.id] = axis
        axis = gizmos_m.Gizmos.WordAxisGizmo(self.ctx, (0, 0, 0), (0, 1, 0), (0, 1, 0), self.camera_component, size=3)
        self.transform_axis_gizmo[axis.id] = axis
        axis = gizmos_m.Gizmos.WordAxisGizmo(self.ctx, (0, 0, 0), (0, 0, 1), (0, 0, 1), self.camera_component, size=3)
        self.transform_axis_gizmo[axis.id] = axis

    def draw_gizmos_transformation_axis(self, transformation):
        for axis in self.transform_axis_gizmo.values():
            distance = glm.distance(self.camera.transformation.pos, transformation.pos)
            scale = distance * 1 / 7
            m_model = glm.scale(transformation.m_tr, glm.vec3(scale))
            axis.draw(m_model)

    def process_window_resize(self, new_size):
        self.camera_component.process_window_resize(new_size)
        for obj in self.objects.values():
            renderer = obj.get_component_by_name("Renderer")
            if renderer:
                renderer.update_projection_matrix(self.camera_component.m_proj)

    def apply_components(self):
        self.camera.apply_components()
        for obj in self.objects.values():
            obj.apply_components()
        for renderer in self.opaque_renderer:
            renderer.apply()
        for renderer in self.transparency_renderer:
            renderer.apply()

    def update(self):
        self.camera.update_components()
        for obj in self.objects.values():
            obj.update_components()

    def delete(self):
        for obj_id, obj in self.objects.items():
            obj.delete()
        self.objects.clear()

        for obj in self.transform_axis_gizmo.values():
            obj.delete()
        self.gizmo_objects.clear()
