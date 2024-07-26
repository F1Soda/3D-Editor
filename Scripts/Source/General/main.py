import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import glm
import struct
import scene as scene_m
import pygame as pg
import moderngl as mgl
import Scripts.Source.Render.library as library_m
import Scripts.Source.Render.gizmos as gizmos_m
import Scripts.Source.General.index_manager as index_manager_m

WIN_SIZE = (1600, 900)


class GraphicsEngine:
    def __init__(self, width=1600, height=900):
        pg.init()
        # Window size
        self.width = width
        self.height = height
        self.WIN_SIZE = (width, height)

        # Settings GL
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)

        # Mouse settings
        # pg.event.set_grab(True)
        # pg.mouse.set_visible(False)

        # Context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        # Mouse Picking
        self.pick_fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.renderbuffer(self.WIN_SIZE)]
        )

        # Library
        library_m.init(self.ctx)

        # Clock and time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        self.scene = scene_m.Scene(self)

        # Gizmos
        self.gizmos = gizmos_m.Gizmos(self.ctx, self.scene.camera.get_component_by_name("Camera"))

    def check_events(self):
        '''
        На данный момент проверяет только выход из приложения
        :return:
        '''
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                self.scene.delete()
                sys.exit()

    def update_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def update_title(self):
        pg.display.set_caption(
            f'FPS: {round(self.clock.get_fps())} '
            f'Cam Pos(x: {round(self.scene.camera.transformation.pos.x, 1)}, '
            f'y: {round(self.scene.camera.transformation.pos.y, 1)}, '
            f'z: {round(self.scene.camera.transformation.pos.z, 1)}) '
            f'Rot(x: {round(self.scene.camera.transformation.rot.x, 1)}, '
            f'y: {round(self.scene.camera.transformation.rot.y, 1)}, '
            f'z: {round(self.scene.camera.transformation.rot.z, 1)})')

    def render(self):
        self.ctx.screen.use()
        self.ctx.clear(color=(0.08, 0.16, 0.18, 1))
        self.scene.apply_components()
        self.gizmos.update()
        self.render_gizmos()
        pg.display.flip()

    def render_gizmos(self):
        self.ctx.disable(mgl.DEPTH_TEST)
        self.gizmos.draw_word_axis()
        self.ctx.enable(mgl.DEPTH_TEST)

    def picking_pass(self):
        self.pick_fbo.use()
        self.ctx.clear(0.0, 0.0, 0.0)
        for obj in self.scene.objects:
            renderer = obj.get_component_by_name('Renderer')
            if renderer is None:
                continue
            past_color = renderer.material['color'].value
            pick_color = index_manager_m.IndexManager.get_color_by_id(obj.id)
            renderer.material['color'].value = glm.vec3(pick_color)
            renderer.apply()
            renderer.material['color'].value = past_color

    def get_object_id_at_mouse(self):
        x, y = pg.mouse.get_pos()
        y = self.height - y
        pixel = self.pick_fbo.read(attachment=0, viewport=(x, y, 1, 1), dtype='f1')

        return index_manager_m.IndexManager.get_id_by_color(self._bytes_to_normalized_tuple(pixel))

    def _bytes_to_normalized_tuple(self, byte_data):
        # Unpack the byte data into integers
        int_values = struct.unpack('BBB', byte_data)
        # Normalize the values to the range [0, 1]
        normalized_values = tuple(value / 255.0 for value in int_values)
        return normalized_values

    def run(self):
        while True:
            self.update_title()
            self.update_time()
            self.check_events()
            self.scene.update()
            self.render()
            self.picking_pass()
            if pg.mouse.get_pressed()[0]:
                print(self.get_object_id_at_mouse())
            self.delta_time = self.clock.tick(120)


if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
