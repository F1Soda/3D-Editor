import typing
import numpy as np
import Scripts.Bin.Render.render as render
import Scripts.Bin.Components.components as components
import Scripts.Bin.General.object as object_m
import Scripts.Bin.General.main as main_m

class Scene:
    def __init__(self, app: main_m.GraphicsEngine):
        self.app = app
        self.ctx = self.app.ctx
        self.objects: typing.List[object_m.Object] = []
        self.light = self._create_light()
        self.camera = self._create_camera()
        self.load()

    def _create_camera(self) -> object_m.Object:
        cam = object_m.Object(self, "Camera", [])
        cam.add_component(components.Camera(cam, self.app))
        cam.add_component(components.FreeFlyMove(cam, self.app))
        cam.transformation.pos = (-2, 0, 0)

        self.objects.append(cam)
        return cam

    def _create_light(self) -> object_m.Object:
        light = object_m.Object(self, "Light", [])
        light.add_component(components.Light(light))
        light.transformation.pos = (0, 3, 0)

        self.objects.append(light)
        return light

    def load(self):
        self.create_cube()

    def create_cube(self) -> object_m.Object:
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]

        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1)]
        normals = [(0, 0, 1) * 6,
                   (1, 0, 0) * 6,
                   (0, 0, -1) * 6,
                   (-1, 0, 0) * 6,
                   (0, 1, 0) * 6,
                   (0, -1, 0) * 6, ]

        normals = np.array(normals, dtype='f4').reshape(36, 3)

        cube_mesh = render.Mesh(self.ctx, "cube", '3f', ['in_position'], vertices,
                                indices,
                                normals, tex_coord, tex_coord_indices)
        cube_material = render.Material(self.ctx, "Lit", render.ShaderProgram(self.ctx))
        obj = object_m.Object(self, "Cube", [])
        obj.add_component(components.Renderer(self.ctx, obj, cube_mesh, cube_material))
        self.objects.append(obj)
        return obj

    def _create_name(self) -> str:
        index = 0
        while True:
            yield f"object_{index}"
            index += 1

    def apply_components(self):
        for obj in self.objects:
            obj.apply_components()

    def update(self):
        for obj in self.objects:
            obj.update_components()

    def delete(self):
        for obj in self.objects:
            obj.delete()
            self.objects.remove(obj)
