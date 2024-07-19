import moderngl as mgl
import numpy as np
import glm


class BaseModel:
    def __init__(self, app, vao_name, tex_name, pos=(0,0,0), rot=(0,0,0), scale=(1,1,1)):
        self.app = app
        self.pos = pos
        self.scale = scale
        self.rot = glm.vec3([glm.radians(x) for x in rot])
        self.m_model = self.get_model_matrix()
        self.tex_name = tex_name
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()

        # position
        m_model = glm.translate(m_model, self.pos)

        # rotation
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))

        # scale
        m_model =glm.scale(m_model, self.scale)

        return m_model


    def render(self):
        self.update()
        self.vao.render()


class Cube(BaseModel):
    def __init__(self, app, vao_name='cube', tex_name='test', pos=(0,0,0), rot=(0,0,0), scale=(1,1,1)):
        super().__init__(app, vao_name, tex_name, pos, rot, scale)
        self.on_init()

    def update(self):
        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.tex_name]
        self.program['u_texture_0'] = 0
        self.texture.use()

        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.intensity_ambient)
        self.program['light.Id'].write(self.app.light.intensity_diffuse)
        self.program['light.Is'].write(self.app.light.intensity_specular)

        self.program['m_proj'].write(self.app.camera.m_proj)
        self.program['m_view'].write(self.app.camera.m_view)
        self.program['m_model'].write(self.m_model)

class Gun(BaseModel):
    def __init__(self, app, vao_name='gun', tex_name='test', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_name, pos, rot, scale)
        self.on_init()

    def update(self):
        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.tex_name]
        self.program['u_texture_0'] = 0
        self.texture.use()

        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.intensity_ambient)
        self.program['light.Id'].write(self.app.light.intensity_diffuse)
        self.program['light.Is'].write(self.app.light.intensity_specular)

        self.program['m_proj'].write(self.app.camera.m_proj)
        self.program['m_view'].write(self.app.camera.m_view)
        self.program['m_model'].write(self.m_model)