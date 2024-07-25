import numpy as np
import Scripts.Source.Render.render as render
import glm

meshes = dict()
materials = dict()
shader_programs = dict()


def _init_cube(ctx):
    vertices = [(-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5),
                (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5)]

    indices = [(0, 2, 3), (0, 1, 2),
               (1, 7, 2), (1, 6, 7),
               (6, 5, 4), (4, 7, 6),
               (3, 4, 5), (3, 5, 0),
               (3, 7, 4), (3, 2, 7),
               (0, 6, 1), (0, 5, 6)]

    # tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
    # tex_coord_indices = [(0, 2, 3), (0, 1, 2),
    #                      (0, 2, 3), (0, 1, 2),
    #                      (0, 1, 2), (2, 3, 0),
    #                      (2, 3, 0), (2, 0, 1),
    #                      (0, 2, 3), (0, 1, 2),
    #                      (3, 1, 2), (3, 0, 1)]
    # normals = [(0, 0, 1) * 6,
    #            (1, 0, 0) * 6,
    #            (0, 0, -1) * 6,
    #            (-1, 0, 0) * 6,
    #            (0, 1, 0) * 6,
    #            (0, -1, 0) * 6, ]

    # normals = np.array(normals, dtype='f4').reshape(36, 3)
    mesh = render.Mesh(ctx, "cube", '3f', ['in_position'])
    mesh.vertices = vertices
    mesh.indices = indices
    return mesh


def _init_plane(ctx):
    vertices = [(-0.5, 0, -0.5), (-0.5, 0, 0.5), (0.5, 0, 0.5), (0.5, 0, -0.5)]

    indices = [(0, 1, 2), (0, 2, 3), (0, 2, 1), (0, 3, 2)]

    mesh = render.Mesh(ctx, "plane", '3f', ['in_position'])
    mesh.vertices = vertices
    mesh.indices = indices
    return mesh


def _init_unlit_material(ctx, color):
    return render.Material(ctx, "Unlit", shader_programs['unlit'], [('color', glm.vec3(color))])


def _init_test_material(ctx):
    return render.Material(ctx, "test", render.ShaderProgram(ctx, 'test'), [])


def _init_shaders(ctx):
    shader_programs['unlit'] = render.ShaderProgram(ctx, 'unlit')
    shader_programs['word_axis_gizmo'] = render.ShaderProgram(ctx, 'WordAxisGizmo')


def get_segment_vao(ctx, start, end, color=(0, 1, 0)):
    buffer_format = '3f 3f'
    data = np.array([start, end], dtype='f4')
    data = np.hstack([data, np.array([color, color], dtype='f4')])
    vbo = ctx.buffer(data)
    vao = ctx.vertex_array(shader_programs['word_axis_gizmo'].bin_program,
                           [(vbo, buffer_format, 'in_position', 'in_color')])
    return vao


def get_point_vao(ctx, pos):
    buffer_format = '3f'
    data = np.array([pos], dtype='f4')
    vbo = ctx.buffer(data)
    vao = ctx.vertex_array(shader_programs['unlit'].bin_program,
                           [(vbo, buffer_format, 'in_position')])
    return vao


def init(ctx):
    _init_shaders(ctx)

    # Meshes
    meshes['cube'] = _init_cube(ctx)
    meshes['plane'] = _init_plane(ctx)

    # Materials
    materials['red'] = _init_unlit_material(ctx, (1, 0, 0))
    materials['green'] = _init_unlit_material(ctx, (0, 1, 0))
    materials['blue'] = _init_unlit_material(ctx, (0, 0, 1))
    materials['magenta'] = _init_unlit_material(ctx, (1, 0, 1))
    materials['cyan'] = _init_unlit_material(ctx, (0, 1, 1))
    materials['gray'] = _init_unlit_material(ctx, (0.5, 0.5, 0.5))
    materials['black'] = _init_unlit_material(ctx, (0, 0, 0))
    materials['white'] = _init_unlit_material(ctx, (1, 1, 1))

