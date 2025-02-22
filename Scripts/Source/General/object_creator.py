import Scripts.Source.Components.components as components
import Scripts.Source.General.object as object_m
import Scripts.Source.Render.library as library_m
import Scripts.Source.Render.render as render
import glm


class ObjectCreator:
    app = None
    camera_component = None
    rely_scene = None

    @staticmethod
    def init(app, scene):
        ObjectCreator.app = app
        ObjectCreator.rely_scene = scene

    @staticmethod
    def create_camera() -> object_m.Object:
        cam = object_m.Object(ObjectCreator.rely_scene, "Camera")
        ObjectCreator.camera_component = components.Camera()
        cam.add_component(ObjectCreator.camera_component)
        cam.add_component(components.FreeFlyMove())
        temp = cam.components[1]
        cam.components[1] = cam.components[2]
        cam.components[2] = temp
        cam.transformation.pos = (-2, 3, 0)
        cam.transformation.rot = (-30, 45, 0)

        return cam

    @staticmethod
    def create_light() -> object_m.Object:
        light = object_m.Object(ObjectCreator.rely_scene, "Light", [])
        light.add_component(components.Light())
        light.transformation.pos = (0, 3, 0)

        return light

    @staticmethod
    def create_cube(color: str, name="") -> object_m.Object:
        cube = object_m.Object(ObjectCreator.rely_scene, name, [])
        if name == "":
            cube.name = f"cube_{cube.id}"
        cube_renderer = components.Renderer(library_m.meshes['cube'], library_m.materials[color], True)
        cube.add_component(cube_renderer)
        if library_m.materials[color].render_mode == render.RenderMode.Opaque:
            ObjectCreator.rely_scene.opaque_renderer.append(cube_renderer)
        else:
            ObjectCreator.rely_scene.transparency_renderer.append(cube_renderer)
        return cube

    @staticmethod
    def create_tetrahedron(color: str, name="", add_to_sequence_render=True) -> object_m.Object:
        tetrahedron = object_m.Object(ObjectCreator.rely_scene, name, [])
        if name == "":
            tetrahedron.name = f"tetrahedron_{tetrahedron.id}"
        tetrahedron_renderer = components.Renderer(library_m.meshes['tetrahedron'], library_m.materials[color], True)
        tetrahedron.add_component(tetrahedron_renderer)
        if add_to_sequence_render:
            if library_m.materials[color].render_mode == render.RenderMode.Opaque:
                ObjectCreator.rely_scene.opaque_renderer.append(tetrahedron_renderer)
            else:
                ObjectCreator.rely_scene.transparency_renderer.append(tetrahedron_renderer)
        return tetrahedron

    @staticmethod
    def create_octahedron(color: str, name="") -> object_m.Object:
        octahedron = object_m.Object(ObjectCreator.rely_scene, name, [])
        if name == "":
            octahedron.name = f"octahedron_{octahedron.id}"
        octahedron_renderer = components.Renderer(library_m.meshes['octahedron'], library_m.materials[color], True)
        octahedron.add_component(octahedron_renderer)
        if library_m.materials[color].render_mode == render.RenderMode.Opaque:
            ObjectCreator.rely_scene.opaque_renderer.append(octahedron_renderer)
        else:
            ObjectCreator.rely_scene.transparency_renderer.append(octahedron_renderer)
        return octahedron

    @staticmethod
    def create_point(color: glm.vec4, size=200, name=""):
        point = object_m.Object(ObjectCreator.rely_scene, name, [])
        if name == "":
            point.name = f"point_{point.id}"
        point_component = components.Point(color, size, False)
        point.add_component(point_component)
        ObjectCreator.rely_scene.opaque_renderer.append(point_component)
        return point

    @staticmethod
    def create_segment(color: glm.vec4, p1, p2, size=100, name=""):
        segment = object_m.Object(ObjectCreator.rely_scene, name, [])
        if name == "":
            segment.name = f"segment_{segment.id}"
        segment_component = components.Segment(p1, p2, color, size, False)
        segment.add_component(segment_component)

        segment.transformation.moveable = False
        ObjectCreator.rely_scene.opaque_renderer.append(segment_component)
        return segment

    @staticmethod
    def create_plane(name=""):
        plane = object_m.Object(ObjectCreator.rely_scene, name, [])
        if name == "":
            plane.name = f"plane_{plane.id}"
        renderer = components.Renderer(library_m.meshes['plane'], library_m.materials['gray'])
        plane.add_component(renderer)
        ObjectCreator.rely_scene.opaque_renderer.append(renderer)
        return plane

    @staticmethod
    def create_plane_by_3_points(p1: object_m.Object, p2: object_m.Object, p3: object_m.Object, color=glm.vec4(0.5),
                                 name=''):
        plane = object_m.Object(ObjectCreator.rely_scene, name, [])
        if name == "":
            plane.name = f"plane_{plane.id}"
        plane_component = components.Plane(color, p1, p2, p3, save_size=False)
        plane.add_component(plane_component)

        plane.transformation.moveable = False
        plane.transformation.scale = glm.vec3(10, 1, 10)
        ObjectCreator.rely_scene.transparency_renderer.append(plane_component)
        return plane

    @staticmethod
    def release():
        ObjectCreator.app = None
        ObjectCreator.camera_component = None
        ObjectCreator.rely_scene = None
