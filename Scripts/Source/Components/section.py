import Scripts.Source.Components.component as component_m
import Scripts.Source.Render.library as library_m
import Scripts.Source.Components.secateur as secateur_m
import Scripts.Source.Components.renderer as renderer_m
import moderngl as mgl

NAME = "Section"
DESCRIPTION = "Add this component to make section with objects with Secateur component"


class Section(component_m.Component):
    def __init__(self, secateur, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)

        # self._shader = library_m.shader_programs['section']
        self._material = library_m.materials['section']
        self.renderer = None
        self._vao = None
        self._subtract_vao = None
        self.secateur = secateur
        self._subtract_shader = library_m.shader_programs['silhouette']
        self._section_shader = library_m.shader_programs['section']

    def init(self, app, rely_object):
        super().init(app, rely_object)

        self.renderer = self.rely_object.get_component_by_name("Renderer")
        if self.renderer:
            self._vao = self.renderer.get_vao(self._material.shader_program, self.renderer.mesh)
        else:
            self.renderer = self.rely_object.get_component_by_name("Plane")
            if self.renderer:
                self._vao = self.renderer.get_vao(self._material.shader_program)
                self.app.scene.transparency_renderer.remove(self.renderer)
                self.app.scene.opaque_renderer.append(self.renderer)
                self._subtract_vao = self.renderer.get_vao(self._subtract_shader)
                # self.renderer.enable = False
        self._material.camera_component = self.app.scene.camera_component
        self._material.camera_transformation = self.app.scene.camera.transformation
        self._material.initialize()
        self._material['texture0'].value = secateur_m.Secateur.background_stencil_texture
        self._material['texture1'].value = secateur_m.Secateur.front_stencil_texture
        self.renderer.apply = self.renderer_apply

    def process_resize_window(self, new_win_size):
        self._material['winSize'] = new_win_size
        self._material['texture1'].value = secateur_m.Secateur.background_stencil_texture

    def renderer_apply(self):
        self.renderer.update_m_model()

        if self._vao is None or secateur_m.Secateur.background_stencil_texture is None:
            return
        self._material.update(self.rely_object.transformation, self.app.scene.light)

        self._subtract_shader['m_proj'].write(self.app.scene.camera_component.m_proj)
        self._subtract_shader['m_view'].write(self.app.scene.camera_component.m_view)
        self._subtract_shader['m_model'].write(self.rely_object.transformation.m_model)
        self._subtract_shader['subtract'] = True
        # self.secateur.stencil_fbo.depth_mask = False
        secateur_m.Secateur.background_stencil_fbo.use()
        self._subtract_vao.render()
        # self.secateur.background_stencil_fbo.depth_mask = True
        self._material['texture0'].value.use(location=0)
        self._material['texture1'].value.use(location=1)
        self._section_shader['texture0'] = 0
        self._section_shader['texture1'] = 1

        secateur_m.Secateur.front_stencil_fbo.use()
        self._subtract_vao.render()

        self.app.ctx.screen.use()
        self._vao.render()

    def serialize(self) -> {}:
        return {
            'enable': self.enable
        }

    def delete(self):
        self.renderer.apply = renderer_m.Renderer.apply
        self.renderer = None

        self._material = None
        self._vao.release()
        self._vao = None
        super().delete()
