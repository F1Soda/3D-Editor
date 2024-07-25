import Scripts.Source.General.object as object_m
import Scripts.Source.Components.component as component_m
import Scripts.Source.General.scene as scene_m
import Scripts.Source.Components.light as light_m
import Scripts.Source.Render.mesh as mesh_m
import Scripts.Source.Render.material as material_m
import glm
import moderngl

NAME = 'Renderer'
DESCRIPTION = 'Отвечает за отрисовку'


class Renderer(component_m.Component):
    def __init__(self, ctx: moderngl.Context, rely_object: object_m.Object, mesh: mesh_m.Mesh,
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

        # Other
        self.mesh = mesh
        self.material = material
        self.transformation = self.rely_object.transformation
        self.vao = self.get_vao(material.shader_program, mesh)
        self.material.camera_component = camera_component
        self.material.camera_transformation = camera_component.transformation
        self.ctx.line_width = 3.0
        self.ctx.point_size = 4.0
        self.material.initialize()

    def update(self):
        self.material.update(self.transformation)

    def get_model_matrix(self) -> glm.mat4x4:
        return glm.mat4() if self.transformation is None else self.transformation.m_model

    def get_vao(self, shader_program, mesh) -> moderngl.VertexArray:
        vao = self.ctx.vertex_array(shader_program.bin_program, [(mesh.vbo, mesh.data_format, *mesh.attributes)])
        return vao

    def apply(self):
        self.update()
        self.vao.render()

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
        self.material = None
        self.mesh = None
