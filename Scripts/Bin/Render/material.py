import moderngl
import Scripts.Bin.Render.shaderprogram as shader_program_m


class Material:
    def __init__(self, ctx: moderngl.Context, name: str, shader_program: shader_program_m.ShaderProgram):
        self.ctx = ctx
        self.name = name
        self.shader_program = shader_program

    def destroy(self):
        self.ctx = None
        self.shader_program.destroy()
        self.shader_program = None
