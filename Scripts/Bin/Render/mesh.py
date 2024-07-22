import typing
import moderngl
import numpy as np


class Mesh:
    def __init__(self, ctx: moderngl.Context, name: str, data_format: str, attributes: typing.List[str],
                 vertices: typing.List[int], indices: typing.List[int],
                 normals: typing.List[int], tex_coord: typing.List[int],
                 tex_coord_indices: typing.List[int]):
        self.ctx = ctx
        self.name = name
        self.data_format = data_format
        self.attributes = attributes
        self.vertices = vertices
        self.indices = indices
        self.normals = normals
        self.tex_coord = tex_coord
        self.tex_coord_indices = tex_coord_indices
        self.vbo = self.get_vbo()

    @staticmethod
    def get_data(vertices, indices) -> np.ndarray:
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def create_vertex_data(self) -> np.ndarray:
        vertex_data = self.get_data(self.vertices, self.indices)
        # tex_coord_data = self.get_data(self.tex_coord, self.tex_coord_indices)
        # normals = np.array(self.normals, dtype='f4')
        # vertex_data = np.hstack([normals, vertex_data])
        # vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data

    def get_vbo(self):
        vertex_data = self.create_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def destroy(self):
        self.ctx = None
        self.vbo.release()
