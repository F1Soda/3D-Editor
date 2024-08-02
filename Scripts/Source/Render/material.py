import copy

import moderngl
import Scripts.Source.Render.shader_program as shader_program_m

import enum


class VisibleState(enum.Enum):
    Visible = 0
    Debug = 1


class MaterialProperty:
    def __init__(self, name: str, value, material, visible: VisibleState = 0):
        self.name = name
        self.visible = visible
        self.material = material
        self.value = value


class Material:
    def __init__(self, ctx: moderngl.Context, material_name: str, shader_program: shader_program_m.ShaderProgram,
                 properties):
        self.ctx = ctx
        self.name = material_name
        self.shader_program = shader_program
        self.properties = {}
        for name, value in properties:
            self.properties[name] = MaterialProperty(name, value, self)

        # Camera
        self.camera_component = None
        self.camera_transformation = None

    def __getitem__(self, item):
        return self.properties[item]

    def __setitem__(self, key, value):
        self.properties[key].value = value
        self.shader_program[key].write(value)

    def initialize(self):
        self._initialize_shader_with_base_uniforms()

    def _initialize_shader_with_base_uniforms(self):
        # Projection Matrix
        m_proj = self.shader_program.get('m_proj')
        if m_proj:
            m_proj.write(self.camera_component.m_proj)

    def _update_base_uniforms(self, transform_object):
        # Camera Position
        cam_pos = self.shader_program.get('camPos')
        if cam_pos and self.camera_transformation is not None:
            cam_pos.write(self.camera_transformation.pos)
        # View Matrix
        m_view = self.shader_program.get('m_view')
        if m_view and self.camera_transformation is not None:
            m_view.write(self.camera_component.m_view)
        # Model Matrix
        m_matrix = self.shader_program.get('m_model')
        if m_matrix:
            m_matrix.write(transform_object.m_model)

    def _update_properties_uniforms(self):
        for key, value in self.properties.items():
            self.shader_program[key].write(value.value)

    def update_projection_matrix(self, m_proj):
        if self.shader_program.get('m_proj'):
            self.shader_program.get('m_proj').write(m_proj)

    def update(self, transform_object):
        self._update_base_uniforms(transform_object)
        self._update_properties_uniforms()

    def destroy(self):
        self.ctx = None
        self.shader_program.destroy()
        self.shader_program = None
        for shader_property in self.properties:
            shader_property._material = None
            shader_property.value = None
