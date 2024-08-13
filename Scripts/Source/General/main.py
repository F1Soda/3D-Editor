import cProfile
import os
import pstats
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import glm
import Scripts.GUI.GUI as GUI_m
import scene as scene_m
import pygame as pg
import moderngl as mgl
import Scripts.Source.Render.library as library_object_m
import Scripts.GUI.library as library_gui_m
import Scripts.Source.General.data_manager as data_manager_m
import Scripts.Source.Render.gizmos as gizmos_m
import Scripts.Source.General.input_manager as input_manager_m
import Scripts.Source.General.object_picker as object_picker_m
import Scripts.Source.General.object_creator as object_creator_m
import sys
import Scripts.Experemental.profiler as profiler
import Scripts.Source.Components.secateur as secateur_m
import Scripts.Experemental.frame_debugger as frame_debugger_m

WIN_SIZE = (1600, 900)


class GraphicsEngine:
    win_size = glm.vec2()

    def __init__(self, width=WIN_SIZE[0], height=WIN_SIZE[1]):

        pg.init()

        # Window size
        GraphicsEngine.win_size = glm.vec2(width, height)

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
        self.ctx.enable(mgl.DEPTH_TEST | mgl.CULL_FACE)

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

        # GUI
        self.gui = GUI_m.GUI(self, WIN_SIZE)

        frame_debugger_m.FrameDebugger.init(self.gui)

        # Input Manager
        input_manager_m.InputManager.init(self)

        secateur_m.Secateur.init_buffers(self)

        # Initialization in load_scene
        self.scene = None
        self.gizmos = None

        # Load Scene
        self.load_scene('C:/Users/golik/PycharmProjects/3dEditor/Scenes/scene2.json')

        self.draw_gui = True

        pg.display.set_caption("3D Editor")

    def load_scene(self, file_path=None):
        if self.scene:
            self.scene.delete()
            object_picker_m.ObjectPicker.release()
            object_creator_m.ObjectCreator.release()
        if self.gizmos:
            self.gizmos.delete()
        self.scene = scene_m.Scene(self, self.gui)
        input_manager_m.InputManager.init(self)
        object_creator_m.ObjectCreator.rely_scene = self.scene
        object_picker_m.ObjectPicker.init(self)
        self.scene.load(file_path)
        self.gizmos = gizmos_m.Gizmos(self.ctx, self.scene)

        self.gui.update_data_in_hierarchy()

    def process_window_resize(self, event):
        self.win_size = glm.vec2(event.size)

        pg.display.set_mode((self.win_size.x, self.win_size.y), flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)

        secateur_m.Secateur.delete_buffers()
        secateur_m.Secateur.init_buffers(self)

        self.gui.process_window_resize(self.win_size)
        self.scene.process_window_resize(self.win_size)
        self.gizmos.process_window_resize(self.win_size)
        object_picker_m.ObjectPicker.process_window_resize(self.win_size)

        self.ctx.viewport = (0, 0, self.win_size.x, self.win_size.y)

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
        self.ctx.enable(mgl.BLEND)
        self.scene.render_opaque_objects()

        # Gizmos
        self.gizmos.render()

        self.scene.render_transparent_objects()
        self.ctx.enable(mgl.BLEND)
        self.ctx.disable(mgl.DEPTH_TEST)
        # GUI
        if self.draw_gui:
            self.gui.render()
        self.ctx.disable(mgl.BLEND)
        self.ctx.enable(mgl.DEPTH_TEST)

        pg.display.flip()

    def exit(self):
        pg.quit()
        self.scene.delete()
        self.gizmos.delete()
        self.gui.delete()

        secateur_m.Secateur.delete_buffers()

        object_picker_m.ObjectPicker.release()
        input_manager_m.InputManager.release()
        object_creator_m.ObjectCreator.release()
        profiler.close_streams()
        sys.exit()

    def run(self):

        while True:
            self.delta_time = self.clock.tick(120)
            self.update_time()
            self.scene.apply_components()
            self.render()

            object_picker_m.ObjectPicker.picking_pass()
            input_manager_m.InputManager.process()


if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
