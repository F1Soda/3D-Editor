import glm
import GUI.GUI as GUI_m
import scene as scene_m
import pygame as pg
import moderngl as mgl
import Scripts.Source.Render.library as library_object_m
import Scripts.GUI.library as library_gui_m
import Scripts.Source.General.data_manager as data_manager_m
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
        self.win_size = (width, height)

        # Settings GL
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode(self.win_size, flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)

        # Mouse settings
        # pg.event.set_grab(True)
        # pg.mouse.set_visible(False)

        # Context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        # Transparency
        self.ctx.blend_func = mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA

        # Data Manager
        data_manager_m.DataManager.init()

        # Library
        library_gui_m.init(self.ctx)
        library_object_m.init(self.ctx)

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

        # GUI
        self.gui = GUI_m.GUI(self, WIN_SIZE)

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
            elif event.type == pg.VIDEORESIZE:
                self.process_window_resize(event)

    def process_window_resize(self, event):
        self.width, self.height = event.size
        self.win_size = glm.vec2(self.width, self.height)

        pg.display.set_mode((self.width, self.height), flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)

        self.gui.process_window_resize(self.win_size)
        self.scene.process_window_resize(self.win_size)
        object_picker_m.ObjectPicker.process_window_resize(self.win_size)

        self.ctx.viewport = (0, 0, self.width, self.height)

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
        self.ctx.clear(color=(0.08, 0.16, 0.18, 1))
        self.scene.apply_components()
        self.render_gizmos()

        # GUI
        self.ctx.enable(mgl.BLEND)
        self.ctx.disable(mgl.DEPTH_TEST)
        self.gui.render()
        self.ctx.disable(mgl.BLEND)
        self.ctx.enable(mgl.DEPTH_TEST)
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
