import Scripts.Source.Components.component as component_m
import Scripts.Source.Render.library as library_m
import Scripts.Experemental.frame_debugger as frame_debugger_m
import moderngl as mgl
import glm

NAME = "Secateur"
DESCRIPTION = "Objects with component section will be rendering only inside object mesh"


class Secateur(component_m.Component):
    # External initialization
    background_stencil_texture = None
    front_stencil_texture = None
    background_stencil_fbo = None
    front_stencil_fbo = None

    @staticmethod
    def init_texture(app):
        size = (int(app.win_size.x), int(app.win_size.y))
        Secateur.background_stencil_texture = app.ctx.texture(size, 1, dtype='f1')
        Secateur.background_stencil_texture.repeat_x = False
        Secateur.background_stencil_texture.repeat_y = False
        Secateur.background_stencil_texture.filter = (mgl.NEAREST, mgl.NEAREST)
        Secateur.background_stencil_texture.swizzle = 'RRR1'

        Secateur.front_stencil_texture = app.ctx.texture(size, 1, dtype='f1')
        Secateur.front_stencil_texture.repeat_x = False
        Secateur.front_stencil_texture.repeat_y = False
        Secateur.front_stencil_texture.filter = (mgl.NEAREST, mgl.NEAREST)
        Secateur.front_stencil_texture.swizzle = 'RRR1'

        Secateur.background_stencil_fbo = app.ctx.framebuffer(
            color_attachments=[Secateur.background_stencil_texture],
            depth_attachment=app.ctx.depth_texture(size)
        )

        Secateur.front_stencil_fbo = app.ctx.framebuffer(
            color_attachments=[Secateur.front_stencil_texture],
            depth_attachment=app.ctx.depth_texture(size)
        )

    def __init__(self, enable=True):
        super().__init__(NAME, DESCRIPTION, enable)

        self.renderer = None
        self.vao = None
        self.shader = library_m.shader_programs['silhouette']

    def init(self, app, rely_object):
        super().init(app, rely_object)

        self.renderer = self.rely_object.get_component_by_name("Renderer")
        if self.renderer:
            self.vao = self.renderer.get_vao(self.shader, self.renderer.mesh)
        frame_debugger_m.FrameDebugger.draw_texture(self.background_stencil_texture, glm.vec2(0.85))
        frame_debugger_m.FrameDebugger.draw_texture(self.front_stencil_texture, glm.vec2(0.85, 0.55))
        # frame_debugger_m.FrameDebugger.draw_texture(Secateur.depth_texture0, glm.vec2(0.85, 0.25), True)
        # frame_debugger_m.FrameDebugger.draw_texture(Secateur.depth_texture1, glm.vec2(0.85, 0), True)
        self.shader['m_proj'].write(self.app.scene.camera_component.m_proj)
        self.renderer.enable = False

    def apply(self):
        if self.background_stencil_fbo is None or self.background_stencil_texture is None or self.renderer is None or self.vao is None:
            return
        self.shader['m_view'].write(self.app.scene.camera_component.m_view)
        self.shader['m_model'].write(self.rely_object.transformation.m_model)
        # There don't update projection matrix!!!
        self.shader['subtract'] = False

        self.background_stencil_fbo.use()
        self.app.ctx.clear()
        self.app.ctx.cull_face = 'front'
        self.vao.render()

        self.front_stencil_fbo.use()
        self.app.ctx.clear()
        self.app.ctx.cull_face = 'back'
        self.vao.render()

        self.app.ctx.screen.use()

    def serialize(self) -> {}:
        return {
            'enable': self.enable
        }

    def delete(self):
        self.renderer = None
        self.vao.release()
        self.vao = None
        super().delete()
