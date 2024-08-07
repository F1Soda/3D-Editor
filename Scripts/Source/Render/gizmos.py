import numpy as np

import Scripts.Source.Render.library as library
import moderngl as mgl
import glm
import Scripts.Source.General.index_manager as index_manager_m
import Scripts.GUI.GUI as gui_m
import Scripts.Source.General.object as object_m
import Scripts.Source.Components.components as components
import Scripts.Source.Render.library as library_m


class Gizmos:
    class Geometry:
        def __init__(self, ctx, scene, camera_component, save_size=True):
            self.id = index_manager_m.IndexManager.get_id()
            self.ctx = ctx
            self.scene = scene
            self.camera_component = camera_component
            self.save_size = True

        def draw(self):
            ...

    class SegmentByPoints:
        def __init__(self, ctx, p1, p2, color, camera_component, size=3.0, save_size=True):
            # self.id = index_manager_m.IndexManager.get_id()
            self.ctx = ctx
            self.p1 = p1
            self.p2 = p2
            self._color = glm.vec4(color)
            self._size = self.default_size = size
            self.camera_component = camera_component
            self.save_size = save_size
            self.vbo = self.ctx.buffer(self.get_vertices())
            self.shader_program = library_m.shader_programs['segment_gizmo']
            self.vao = self.ctx.vertex_array(self.shader_program.bin_program, self.vbo, 'in_position')

        def get_vertices(self):
            if self.p1 is None or self.p2 is None:
                return None
            return np.array([self.p1.transformation.pos, self.p2.transformation.pos], dtype=np.float32)

        @property
        def color(self):
            return self._color

        @color.setter
        def color(self, value):
            if isinstance(value, tuple):
                self._color = glm.vec4(value)
            else:
                self._color = value
            self.shader_program['color'].write(self._color)

        @property
        def size(self):
            return self._size

        @size.setter
        def size(self, value):
            self._size = value
            self.ctx.line_width = value

        def set_default_size(self):
            self.size = self.default_size

        def draw(self, m_model=None, m_proj=None):
            vertices = self.get_vertices()
            if vertices is None:
                return
            self.vbo.write(vertices)

            self.shader_program['color'] = self.color
            self.shader_program['m_proj'].write(m_proj if m_proj is not None else self.camera_component.m_proj)
            self.shader_program['m_view'].write(self.camera_component.get_view_matrix())
            self.shader_program['m_model'].write(m_model if m_model is not None else glm.mat4())

            if not self.save_size:
                distance = glm.distance(self.camera_component.transformation.pos,
                                        (self.p1.transformation.pos + self.p2.transformation.pos) / 2)
                scale = 1 / distance
                self.ctx.line_width = self.size * scale
            self.vao.render(mgl.LINES)

        def delete(self):
            self.ctx = None
            self.vbo.release()
            self.vbo = None
            self.vao.release()
            self.vao = None
            self.p1 = None
            self.p2 = None
            self.shader_program = None

    class WordAxisGizmo:
        def __init__(self, ctx, start, end, color, camera, size=3.0, save_size=False):
            self.id = index_manager_m.IndexManager.get_id()
            self.ctx = ctx
            self.save_size = save_size
            self.start = glm.vec3(*start)
            self._size = self.default_size = size
            self.end = glm.vec3(*end)
            self._color = glm.vec3(color)
            self.shader = library.shader_programs['word_axis_gizmo']
            self.shader['color'].write(self._color)
            self.vao = library.get_segment_vao(ctx, start, end)
            self.camera = camera

        @property
        def size(self):
            return self._size

        @size.setter
        def size(self, value):
            self._size = value
            self.ctx.line_width = value

        @property
        def color(self):
            return self._color

        @color.setter
        def color(self, value):
            if isinstance(value, tuple):
                self._color = glm.vec3(value)
            else:
                self._color = value
            self.shader['color'].write(self._color)

        def set_default_size(self):
            self.size = self.default_size

        def draw(self, m_model=None, m_proj=None, m_view=None):
            if self.shader.get('m_view'):
                self.shader.get('m_view').write(self.camera.get_view_matrix() if m_view is None else m_view)
            if self.shader.get('m_model'):
                self.shader.get('m_model').write(m_model)
            if self.shader.get('m_proj'):
                self.shader.get('m_proj').write(self.camera.m_proj if m_proj is None else m_proj)
            self.ctx.line_width = self.size
            self.shader['color'].write(self._color)
            self.vao.render(mgl.LINES)

        def delete(self):
            self.ctx = None
            self.vao.release()
            self.vao = None
            self.shader = None

    class Point:
        def __init__(self, ctx, pos: glm.vec3, color, camera, size=10.0, save_size=True):
            # self.id = index_manager_m.IndexManager.get_id()
            self.ctx = ctx
            self._pos = pos
            self.save_size = save_size
            self._size = self.default_size = size
            self._color = glm.vec4(color)
            self.shader = library.shader_programs['point_gizmo']
            self.shader['color'].write(self._color)
            self.vao = library.vaos['point']
            self.camera = camera

        @property
        def pos(self):
            return self._pos

        @pos.setter
        def pos(self, value):
            if isinstance(value, tuple):
                self._pos = glm.vec3(value)
            else:
                self._pos = value
            self.shader['position'].write(self._pos)

        @property
        def size(self):
            return self._size

        @size.setter
        def size(self, value):
            self._size = value
            self.ctx.line_width = value

        @property
        def color(self):
            return self._color

        @color.setter
        def color(self, value):
            if isinstance(value, tuple):
                self._color = glm.vec4(value)
            else:
                self._color = value
            self.shader['color'].write(self._color)

        def set_default_size(self):
            self.size = self.default_size

        def draw(self, m_proj=None, m_view=None):

            if self.shader.get('m_view'):
                self.shader.get('m_view').write(self.camera.get_view_matrix() if m_view is None else m_view)
            if self.shader.get('m_proj'):
                self.shader.get('m_proj').write(self.camera.m_proj if m_proj is None else m_proj)
            if self.save_size:
                self.ctx.point_size = self.size
            else:
                distance = glm.distance(self.camera.transformation.pos, self.pos)
                scale = 1 / distance
                self.ctx.point_size = self.size * scale
            self.shader['color'].write(self._color)
            self.shader['position'].write(self._pos)
            self.vao.render(mgl.POINTS)

        def delete(self):
            self.ctx = None
            self.camera = None
            self.shader = None
            self.vao = None

    def __init__(self, ctx: mgl.Context, scene):
        self.ctx = ctx
        self.camera = scene.camera_component
        self.scene = scene
        self.x_axis = Gizmos.WordAxisGizmo(ctx, (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), glm.vec3(1, 0, 0),
                                           self.scene.camera_component)
        self.y_axis = Gizmos.WordAxisGizmo(ctx, (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), glm.vec3(0, 1, 0),
                                           self.scene.camera_component)
        self.z_axis = Gizmos.WordAxisGizmo(ctx, (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), glm.vec3(0, 0, 1),
                                           self.scene.camera_component)

        plane = object_m.Object(scene, "Plane", [])
        renderer = components.Renderer(self.ctx, plane, library_m.meshes['plane'], library_m.materials['grid'],
                                       scene.camera_component)
        plane.add_component(renderer)
        plane.transformation.scale = glm.vec3(1000, 1, 1000)
        renderer.material['tilling'] = glm.vec2(1000)
        renderer.material['color'] = glm.vec4(1, 1, 1, 0.5)

        self.grid_plane_renderer = renderer
        self.shader = library.shader_programs['word_axis_gizmo']

        self.space = []
        length = 5
        for z in range(length):
            for y in range(length):
                for x in range(length):
                    point = Gizmos.Point(ctx, glm.vec3(x, y, z), glm.vec4(x / 10, y / 10, z / 10, 1), self.camera,
                                         size=100,
                                         save_size=False)
                    self.space.append(point)

    def draw_fun_space(self):
        for point in self.space:
            point.draw()

    def draw_center_coordinate(self):
        m_model = glm.mat4()
        m_model[3][1] = 0.5
        m_model[3][0] = 0.5
        m_model[3][2] = 0.5

        self.x_axis.draw(m_model=m_model)
        self.y_axis.draw(m_model=m_model)
        self.z_axis.draw(m_model=m_model)

    def draw_word_axis_in_right_corner(self):
        self.x_axis.draw(m_proj=self.camera.m_ortho, m_model=self.get_model_matrix_for_world_axis())
        self.y_axis.draw(m_proj=self.camera.m_ortho, m_model=self.get_model_matrix_for_world_axis())
        self.z_axis.draw(m_proj=self.camera.m_ortho, m_model=self.get_model_matrix_for_world_axis())

    def draw_plane_grid(self):
        self.grid_plane_renderer.apply()

    def get_model_matrix_for_world_axis(self):
        m_model = glm.mat4()
        near = self.camera.near
        diagonal = pow(self.ctx.screen.width * self.ctx.screen.width +
                       self.ctx.screen.height * self.ctx.screen.height, 0.5)
        size = near / diagonal * 150
        up = self.camera.up
        right = self.camera.right
        forward = self.camera.forward
        m_model = glm.translate(m_model, self.camera.transformation.pos
                                + forward * (self.camera.near + 1)
                                + right * (self.camera.right_bound * (gui_m.GUI.LEFT_INSPECTOR_CORNER - 0.5) * 2)
                                - up * (self.camera.top_bound)
                                + (up - right) * size
                                )

        m_model = glm.scale(m_model, (size, size, size))
        return m_model
