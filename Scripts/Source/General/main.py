import glm

import scene as scene_m
import pygame as pg
import moderngl as mgl
import Scripts.Source.Render.library as library_m
import Scripts.Source.Render.gizmos as gizmos_m
import Scripts.Source.General.input_manager as input_manager_m
import Scripts.Source.General.object_picker as object_picker_m

import sys

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

        # Library
        library_m.init(self.ctx)

        # Clock and time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        self.scene = scene_m.Scene(self)

        # Gizmos
        self.gizmos = gizmos_m.Gizmos(self.ctx, self.scene.camera.get_component_by_name("Camera"))

        # Input Manager
        input_manager_m.InputManager.init(self)

        # ObjectPicker
        object_picker_m.ObjectPicker.init(self)

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
        self.render_gizmos()
        pg.display.flip()

    def render_gizmos(self):
        self.ctx.disable(mgl.DEPTH_TEST)
        self.gizmos.draw_word_axis()
        if object_picker_m.ObjectPicker.last_picked_obj_transformation:
            self.scene.draw_gizmos_transformation_axis(object_picker_m.ObjectPicker.last_picked_obj_transformation)
        self.ctx.enable(mgl.DEPTH_TEST)

    def run(self):
        while True:
            self.update_title()
            self.update_time()
            self.check_events()
            self.scene.update()
            self.render()
            object_picker_m.ObjectPicker.picking_pass()
            input_manager_m.InputManager.process()
            self.delta_time = self.clock.tick(120)


if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
