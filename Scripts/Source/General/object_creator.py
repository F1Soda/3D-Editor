import numpy as np

import Scripts.Source.Components.components as components
import Scripts.Source.General.object as object_m
import Scripts.Source.Render.library as library_m
import Scripts.Source.Render.gizmos as gizmos_m
import copy
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
        cam = object_m.Object(ObjectCreator.rely_scene, "Camera", [])
        ObjectCreator.camera_component = components.Camera(cam, ObjectCreator.app)
        cam.add_component(ObjectCreator.camera_component)
        cam.add_component(components.FreeFlyMove(cam, ObjectCreator.app))
        cam.transformation.pos = (-2, 3, 0)
        cam.transformation.rot = (-30, 45, 0)

        return cam

    @staticmethod
    def create_light() -> object_m.Object:
        light = object_m.Object(ObjectCreator.rely_scene, "Light", [])
        light.add_component(components.Light(light))
        light.transformation.pos = (0, 3, 0)

        return light

    @staticmethod
    def create_cube(color: str, name="") -> object_m.Object:
        cube = object_m.Object(ObjectCreator.rely_scene, name, [])
        if name == "":
            cube.name = f"cube_{cube.id}"
        cube_renderer = components.Renderer(ObjectCreator.app.ctx, cube, library_m.meshes['cube'],
                                            library_m.materials[color],
                                            ObjectCreator.camera_component)
        cube.add_component(cube_renderer)
        ObjectCreator.rely_scene.opaque_renderer.append(cube_renderer)
        return cube

    @staticmethod
    def create_tetrahedron(color: str, name="") -> object_m.Object:
        tetrahedron = object_m.Object(ObjectCreator.rely_scene, name, [])
        if name == "":
            tetrahedron.name = f"tetrahedron_{tetrahedron.id}"
        tetrahedron_renderer = components.Renderer(ObjectCreator.app.ctx, tetrahedron, library_m.meshes['tetrahedron'],
                                                   library_m.materials[color],
                                                   ObjectCreator.camera_component)
        tetrahedron.add_component(tetrahedron_renderer)
        ObjectCreator.rely_scene.opaque_renderer.append(tetrahedron_renderer)
        return tetrahedron


    @staticmethod
    def create_octahedron(color: str, name="") -> object_m.Object:
        octahedron = object_m.Object(ObjectCreator.rely_scene, name, [])
        if name == "":
            octahedron.name = f"octahedron_{octahedron.id}"
        octahedron_renderer = components.Renderer(ObjectCreator.app.ctx, octahedron, library_m.meshes['octahedron'],
                                                   library_m.materials[color],
                                                   ObjectCreator.camera_component)
        octahedron.add_component(octahedron_renderer)
        ObjectCreator.rely_scene.opaque_renderer.append(octahedron_renderer)
        return octahedron


    @staticmethod
    def create_point(color: glm.vec4, size=200, name=""):
        point = object_m.Object(ObjectCreator.rely_scene, name, [])
        if name == "":
            point.name = f"point_{point.id}"
        point_component = components.Point(point, ObjectCreator.app.ctx, color,
                                           size,
                                           ObjectCreator.camera_component, False)
        point.add_component(point_component)
        ObjectCreator.rely_scene.opaque_renderer.append(point_component)
        return point

    @staticmethod
    def create_segment(color: glm.vec4, p1, p2, size=100, name=""):
        segment = object_m.Object(ObjectCreator.rely_scene, name, [])
        if name == "":
            segment.name = f"segment_{segment.id}"
        segment_component = components.Segment(segment, p1, p2, ObjectCreator.app.ctx,
                                               color,
                                               size,
                                               ObjectCreator.camera_component, False)
        segment.add_component(segment_component)

        segment.transformation.moveable = False
        ObjectCreator.rely_scene.opaque_renderer.append(segment_component)
        return segment

    @staticmethod
    def create_plane(name=""):
        plane = object_m.Object(ObjectCreator.rely_scene, name, [])
        if name == "":
            plane.name = f"plane_{plane.id}"
        renderer = components.Renderer(ObjectCreator.app.ctx, plane, library_m.meshes['plane'],
                                       library_m.materials['gray'],
                                       ObjectCreator.camera_component)
        plane.add_component(renderer)
        ObjectCreator.rely_scene.opaque_renderer.append(renderer)
        return plane

    @staticmethod
    def create_plane_by_3_points(p1, p2, p3, color=glm.vec4(0.5), name=''):
        plane = object_m.Object(ObjectCreator.rely_scene, name, [])
        if name == "":
            plane.name = f"plane_{plane.id}"
        plane_component = components.Plane(plane, ObjectCreator.app.ctx,
                                           color,
                                           p1, p2, p3,
                                           ObjectCreator.camera_component, False)
        plane.add_component(plane_component)

        plane.transformation.moveable = False
        plane.transformation.scale = glm.vec3(10, 1, 10)
        ObjectCreator.rely_scene.transparency_renderer.append(plane_component)
        return plane

    @staticmethod
    def rotation_matrix_to_euler_angles(R):
        x = np.atan2(R[1][2], R[2][2])
        y = glm.asin(R[0][2])  # np.atan2(-R[0][2], np.sqrt(R[2][1] * R[2][1] + R[2][2] * R[2][2]))
        z = np.atan2(R[0][1], R[0][0])
        return x, y, z

    @staticmethod
    def angles(n):
        z = np.atan2(n.y, n.x)
        y = np.acos(n.x / (np.sqrt(n.x * n.x + n.z * n.z)))
        x = np.asin(n.x / (np.sqrt(n.x * n.x + n.z * n.z + n.y * n.y)))
        return x, y, z

    @staticmethod
    def create_name() -> str:
        index = 0
        while True:
            yield f"object_{index}"
            index += 1
