import typing
import moderngl
import numpy as np
import Scripts.Source.General.utils as utils


class Mesh:
    def __init__(self, ctx: moderngl.Context, name: str, data_format: str, attributes: typing.List):
        self.ctx = ctx
        self.name = name
        self.data_format = data_format
        self.attributes = attributes
        self.vertices = None
        self.indices = None
        self.normals = None
        self.tex_coord = None
        self.tex_coord_indices = None
        self._vbo = None

    @property
    def vbo(self):
        if self._vbo is None:
            self._vbo = self.get_vbo()
        return self._vbo

    def reconstruct_vbo(self):
        self._vbo = self.get_vbo()
        return self._vbo

    def create_vertex_data(self) -> np.ndarray:
        vertex_data = utils.get_data_elements_by_indices(self.vertices, self.indices)
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
