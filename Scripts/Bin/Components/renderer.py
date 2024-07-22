import Scripts.Bin.General.object as object_m
import Scripts.Bin.Components.component as component_m
import Scripts.Bin.General.scene as scene_m
import Scripts.Bin.Components.light as light_m
import Scripts.Bin.Render.mesh as mesh_m
import Scripts.Bin.Render.material as material_m
import glm
import moderngl

NAME = 'Renderer'
DESCRIPTION = 'Отвечает за отрисовку'


class Renderer(component_m.Component):
    def __init__(self, ctx: moderngl.Context, rely_object: object_m.Object, mesh: mesh_m.Mesh,
                 material: material_m.Material, enable=True):
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
        self.material.shader_program['m_proj'].write(self.camera_component.m_proj)

    def update(self):
        # self.material.shader_program['camPos'].write(self.camera_transform.pos)
        self.material.shader_program['m_view'].write(self.camera_component.m_view)
        self.material.shader_program['m_model'].write(self.get_model_matrix())

        # self.material.shader_program['light.position'].write(self.light_transform.pos)
        # self.material.shader_program['light.Ia'].write(self.light_component.intensity_ambient)
        # self.material.shader_program['light.Id'].write(self.light_component.intensity_diffuse)
        # self.material.shader_program['light.Is'].write(self.light_component.intensity_specular)

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
        self.material.destroy()
        self.mesh.destroy()
        self.vao = None
        self.material = None
        self.mesh = None
