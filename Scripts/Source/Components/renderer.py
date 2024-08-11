import Scripts.Source.Components.component as component_m
import Scripts.Source.General.scene as scene_m
import Scripts.Source.Components.light as light_m
import Scripts.Source.Render.mesh as mesh_m
import Scripts.Source.Render.material as material_m
import Scripts.Source.Render.library as library_m
import glm
import moderngl as mgl
import enum

NAME = 'Renderer'
DESCRIPTION = 'Отвечает за отрисовку'


class RenderMode(enum.Enum):
    Solid = 0,
    Wireframe = 1


class Renderer(component_m.Component):

    def __init__(self, mesh: mesh_m.Mesh, material: material_m.Material, transparency=False, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)

        # Settings
        self.rendering_mode = RenderMode.Solid
        self.default_line_width = 3.0
        self.default_point_size = 4.0

        # Other
        self.mesh = mesh
        self._material = material
        self.picking_material = library_m.materials['object_picking']

        self.scene = None
        self.camera_transform = None
        self.camera_component = None
        self.transformation = None
        self.ctx = None
        self.vao = None
        self.vao_picking = None

    def init(self, app, rely_object):
        super().init(app, rely_object)
        # Scene
        self.scene = self.rely_object.scene  # type: scene_m.Scene

        self.ctx = app.ctx

        # Camera
        self.camera_transform = self.scene.camera.transformation
        self.camera_component = self.scene.camera.get_component_by_name('Camera')

        self.picking_material.camera_component = self.camera_component
        self.picking_material.camera_transformation = self.camera_component.transformation
        self.transformation = self.rely_object.transformation
        self.picking_material.initialize()

        self.material.camera_component = self.camera_component
        self.material.camera_transformation = self.camera_component.transformation
        self.material.light_component = self.light_component
        self.material.initialize()

        self.vao = self.get_vao(self._material.shader_program, self.mesh)
        self.vao_picking = self.get_vao(self.picking_material.shader_program, self.mesh)

    @property
    def light_component(self):
        return self.scene.light

    def change_render_mode(self):
        self.rendering_mode = RenderMode.Wireframe if self.rendering_mode == RenderMode.Solid else RenderMode.Solid

    def update_projection_matrix(self, m_proj):
        self.material.update_projection_matrix(m_proj)
        self.picking_material.update_projection_matrix(m_proj)

    def get_model_matrix(self) -> glm.mat4x4:
        return glm.mat4() if self.transformation is None else self.transformation.m_model

    def get_vao(self, shader_program, mesh) -> mgl.VertexArray:
        vao = self.ctx.vertex_array(shader_program.bin_program, [(mesh.vbo, mesh.data_format, *mesh.attributes)])
        return vao

    def apply(self):
        self.material.update(self.transformation, self.light_component)
        if self.rendering_mode == RenderMode.Solid:
            if self.material.render_mode == material_m.RenderMode.Opaque:
                self.vao.render()
            elif self.material.render_mode == material_m.RenderMode.Transparency:
                self.ctx.enable(mgl.BLEND)
                self.vao.render()
                self.ctx.disable(mgl.BLEND)
        else:
            self.ctx.line_width = self.default_line_width
            self.ctx.point_size = self.default_point_size
            self.vao.render(mgl.LINES)

    def render_picking_material(self):
        self.picking_material.update(self.transformation, None)
        self.vao_picking.render()

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        self._material = value
        self.vao.release()
        self.vao = self.get_vao(self._material.shader_program, self.mesh)

    def delete(self):
        self.rely_object = None
        self.transformation = None
        self.camera_component = None
        self.camera_transform = None
        self.scene = None
        self.ctx = None
        self.vao = None
        self._material = None
        self.mesh = None

    def serialize(self) -> {}:
        return {
            'mesh': self.mesh.name,
            'material': self.material.name,
            'enable': self.enable
        }
