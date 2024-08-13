import glm

import Scripts.Source.General.object_creator as object_creator_m
import Scripts.Source.Render.gizmos as gizmos_m
import Scripts.Source.General.data_manager as data_manager_m
import Scripts.Source.General.index_manager as index_manager_m
import Scripts.Source.Components.components as components_m


class Scene:
    def __init__(self, app, gui):
        self.app = app
        self.ctx = self.app.ctx
        self.objects = {}
        self.transform_axis_gizmo = {}

        self.index_manager = index_manager_m.IndexManager()

        self.light = None
        self.camera = None
        self.camera_component = None

        self.opaque_renderer = []
        self.transparency_renderer = []
        self.test_saving_object = None

        self.gui = gui

    def change_render_mode(self):
        for obj in self.objects.values():
            renderer = obj.get_component_by_name("Renderer")
            if renderer:
                renderer.change_render_mode()

    def _default_load(self):
        light = object_creator_m.ObjectCreator.create_light()
        self.objects[light.id] = light

        cube = object_creator_m.ObjectCreator.create_cube('transparency_white_unlit')
        cube_renderer = cube.get_component_by_name('Renderer')
        # self.opaque_renderer.remove(cube_renderer)
        # self.transparency_renderer.append(cube_renderer)
        cube.transformation.pos = (3, 0, 3)
        cube.transformation.scale = glm.vec3(2)
        secateur = cube.add_component(components_m.Secateur())
        self.objects[cube.id] = cube

        p1 = object_creator_m.ObjectCreator.create_point(glm.vec4(1, 0, 0, 1), size=200)
        p1.transformation.pos = glm.vec3(4, 0.5, 4)
        self.objects[p1.id] = p1

        p2 = object_creator_m.ObjectCreator.create_point(glm.vec4(0, 1, 0, 1), size=200)
        p2.transformation.pos = glm.vec3(0, 0.5, 4)
        self.objects[p2.id] = p2

        p3 = object_creator_m.ObjectCreator.create_point(glm.vec4(0, 0, 1, 1), size=200)
        p3.transformation.pos = glm.vec3(0, 0.5, 8)
        self.objects[p3.id] = p3

        plane = object_creator_m.ObjectCreator.create_plane_by_3_points(p1, p2, p3)
        plane.add_component(components_m.Section(secateur))
        self.objects[plane.id] = plane

    def load(self, file_path=None):
        self.camera = object_creator_m.ObjectCreator.create_camera()
        self.camera_component = self.camera.get_component_by_name("Camera")

        self.init_gizmo()

        if file_path:
            data_manager_m.DataManager.load_scene(self, file_path)
        else:

            self._default_load()
        for obj in self.objects.values():
            light = obj.get_component_by_name("Light")
            if light:
                self.light = light

    def add_object(self, obj):
        self.objects[obj.id] = obj
        self.gui.update_data_in_hierarchy()
        return obj

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
            section = obj.get_component_by_name("Section")
            if section:
                section.process_resize_window(new_size)
                continue

    def apply_components(self):
        self.camera.apply_components()
        for obj in self.objects.values():
            obj.apply_components()

    def render_opaque_objects(self):
        for renderer in self.opaque_renderer:
            if renderer.rely_object.enable and renderer.enable:
                renderer.apply()

    def render_transparent_objects(self):
        for renderer in self.transparency_renderer:
            if renderer.rely_object.enable and renderer.enable:
                renderer.apply()

    # @profiler_m.profile
    def delete(self):
        for obj_id, obj in self.objects.items():
            obj.delete()
        self.objects.clear()

        for obj in self.transform_axis_gizmo.values():
            obj.delete()
        self.transform_axis_gizmo.clear()

        self.camera.delete()
        self.camera_component = None
