import Scripts.Source.General.object as object_m
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
    def __init__(self, ctx: mgl.Context, rely_object: object_m.Object, mesh: mesh_m.Mesh,
                 material: material_m.Material, camera_component, enable=True):
        super().__init__(NAME, DESCRIPTION, rely_object, enable)

        self.ctx = ctx

        # Scene
        self.scene = rely_object.scene  # type: scene_m.Scene

        # Camera
        self.camera_transform = self.scene.camera.transformation
        self.camera_component = self.scene.camera.get_component_by_name('Camera')

        # Light
        self.light_component = self.scene.light.get_component_by_type(light_m.Light)
        self.light_transform = self.scene.light.transformation

        # Settings
        self.rendering_mode = RenderMode.Solid

        # Other
        self.mesh = mesh
        self._material = material
        self.picking_material = library_m.materials['object_picking']
        self.picking_material.camera_component = camera_component
        self.picking_material.camera_transformation = camera_component.transformation
        self.transformation = self.rely_object.transformation
        self.vao = self.get_vao(material.shader_program, mesh)
        self.vao_picking = self.get_vao(self.picking_material.shader_program, mesh)
        self.material.camera_component = camera_component
        self.material.camera_transformation = camera_component.transformation
        self.default_line_width = 3.0
        self.default_point_size = 4.0
        self.ctx.line_width = 3.0
        self.ctx.point_size = 4.0
        self.material.initialize()
        self.picking_material.initialize()

    def change_render_mode(self):
        self.rendering_mode = RenderMode.Wireframe if self.rendering_mode == RenderMode.Solid else RenderMode.Solid

    def update(self):
        self.material.update(self.transformation)

    def update_projection_matrix(self, m_proj):
        self.material.update_projection_matrix(m_proj)

    def get_model_matrix(self) -> glm.mat4x4:
        return glm.mat4() if self.transformation is None else self.transformation.m_model

    def get_vao(self, shader_program, mesh) -> mgl.VertexArray:
        vao = self.ctx.vertex_array(shader_program.bin_program, [(mesh.vbo, mesh.data_format, *mesh.attributes)])
        return vao

    def apply(self):
        self.update()
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
        self.picking_material.update(self.transformation)
        self.vao_picking.render()

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        self._material = value
        self.vao.release()
        self.vao = self.get_vao(self._material.shader_program, self.mesh)

    def change_material_with_saving_vao(self, material):
        self._material = material
        vao = self.vao
        self.vao = self.get_vao(self._material.shader_program, self.mesh)
        return vao

    def set_vao_and_material(self, vao, material):
        self.vao.release()
        self._material = material
        self.vao = vao

    def delete(self):
        self.rely_object = None
        self.transformation = None
        self.camera_component = None
        self.light_component = None
        self.camera_transform = None
        self.light_transform = None
        self.scene = None
        self.ctx = None
        self.vao = None
        self._material = None
        self.mesh = None
