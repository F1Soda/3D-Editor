import scene as scene_m
import pygame as pg
import moderngl as mgl

import sys


class GraphicsEngine:
    def __init__(self, win_size=(900, 900)):
        pg.init()
        # Window size
        self.WIN_SIZE = win_size

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

        # Clock and time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        self.scene = scene_m.Scene(self)

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
            f'Cam Pos(x: {round(self.scene.camera.transformation.pos.x, 1)}, '
            f'y: {round(self.scene.camera.transformation.pos.y, 1)}, '
            f'z: {round(self.scene.camera.transformation.pos.z, 1)}) '
            f'Rot(x: {round(self.scene.camera.transformation.rot.x, 1)}, '
            f'y: {round(self.scene.camera.transformation.rot.y, 1)}, '
            f'z: {round(self.scene.camera.transformation.rot.z, 1)})')

    def render(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18, 1))
        self.scene.apply_components()
        pg.display.flip()

    def run(self):
        while True:
            self.update_title()
            self.update_time()
            self.check_events()
            self.scene.update()
            self.render()
            self.delta_time = self.clock.tick(60)



if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
