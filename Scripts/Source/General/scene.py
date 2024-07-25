import typing

import glm

import Scripts.Source.Components.components as components
import Scripts.Source.General.object as object_m
import Scripts.Source.General.main as main_m
import Scripts.Source.Render.library as library_m


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
        self.camera_component = components.Camera(cam, self.app)
        cam.add_component(self.camera_component)
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
        # for i in range(10):
        #     for j in range(10):
        #         cube = self.create_cube()
        #         cube.transformation.pos = (i * 3, 1, j * 3)
        cube = self.create_cube('cube1', 'green')
        cube.transformation.pos = (5, 0, 5)
        cube = self.create_cube('cube2', 'red')
        cube.transformation.pos = (-5, 0, -5)
        cube = self.create_cube('cube3', 'blue')
        cube.transformation.pos = (-5, 0, 5)
        cube = self.create_cube('cube4', 'cyan')
        cube.transformation.pos = (5, 0, -5)
        # plane = self.create_plane()
        # plane.transformation.scale = (10_000, 1, 10_000)

    def create_cube(self, name: str, color: str) -> object_m.Object:
        cube = object_m.Object(self, name, [])
        cube_renderer = components.Renderer(self.ctx, cube, library_m.meshes['cube'], library_m.materials[color],
                                            self.camera_component)
        cube.add_component(cube_renderer)

        self.objects.append(cube)
        return cube

    def create_plane(self):
        plane = object_m.Object(self, "Plane", [])
        plane.add_component(
            components.Renderer(self.ctx, plane, library_m.meshes['plane'], library_m.materials['unlit']))
        self.objects.append(plane)
        return plane

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
