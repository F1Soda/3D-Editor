from vbo import VBO
from shaderprogram import ShaderProgram


class VAO:
    """
    Vertex array object
    Представляет комбинацию ShaderProgram и VBO, к которой и будет применяться шейдер
    """
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {'cube': self.get_vao(program=self.program.programs['default'], vbo=self.vbo.vbos['cube'])}

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()
