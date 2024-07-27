class ShaderProgram:
    def __init__(self, ctx, name='test'):
        self.ctx = ctx
        self.bin_program = self.get_bin_program(name)

    def __getitem__(self, item):
        return self.bin_program[item]

    def get_bin_program(self, shader_name: str):
        with open(f'Shaders/{shader_name}/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'Shaders/{shader_name}/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def get(self, key: str):
        return self.bin_program.get(key, None)

    def destroy(self):
        self.bin_program.release()
        self.ctx = None
