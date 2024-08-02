import glm
import moderngl as mgl
import Scripts.Source.General.index_manager as index_manager_m
import Scripts.Source.General.input_manager as input_manager_m
import Scripts.Source.Render.library as library_m
import utils


class ObjectPicker:
    _pick_fbo = None
    _app = None

    active_axis = None
    _last_picked_obj_id = 0
    last_picked_obj_transformation = None
    _last_picked_obj_m_model = None
    _last_picked_obj_material = None
    _last_mouse_dot = 0

    @staticmethod
    def init(app):
        ObjectPicker._app = app
        ObjectPicker._pick_fbo = app.ctx.framebuffer(
            color_attachments=[app.ctx.renderbuffer((int(app.win_size.x), int(app.win_size.y)))]
        )

        input_manager_m.InputManager.handle_left_click_event += ObjectPicker.process_left_click
        input_manager_m.InputManager.handle_left_hold_event += ObjectPicker.process_hold_left_mouse_button
        input_manager_m.InputManager.handle_left_release_event += ObjectPicker.process_release_left_mouse_button

    @staticmethod
    def process_window_resize(new_size):
        if ObjectPicker._pick_fbo:
            ObjectPicker._pick_fbo.release()
        ObjectPicker._pick_fbo = ObjectPicker._app.ctx.framebuffer(
            color_attachments=[ObjectPicker._app.ctx.renderbuffer((int(new_size.x), int(new_size.y)))]
        )

    @staticmethod
    def get_object_id_at_pos(pos: glm.vec2):
        pixel = ObjectPicker._pick_fbo.read(attachment=0, viewport=(int(pos.x), int(pos.y), 1, 1), dtype='f1')

        return index_manager_m.IndexManager.get_id_by_color(utils.bytes_to_normalized_tuple(pixel))

    @staticmethod
    def process_left_click(mouse_position):
        object_id = ObjectPicker.get_object_id_at_pos(mouse_position)
        if object_id != 0:
            gizmos_axis = ObjectPicker._app.scene.gizmo_objects.get(object_id)
            if gizmos_axis:
                ObjectPicker.process_click_transformation_gizmos(gizmos_axis, mouse_position)
            else:
                ObjectPicker.process_click_object(object_id)
            return True
        else:
            ObjectPicker.process_click_nowhere()
            return False

    @staticmethod
    def process_click_transformation_gizmos(axis, mouse_pos):
        if ObjectPicker.active_axis and ObjectPicker.active_axis != axis:
            ObjectPicker.active_axis.set_default_size()
        ObjectPicker._last_picked_obj_m_model = ObjectPicker.last_picked_obj_transformation.m_model
        ObjectPicker._last_mouse_dot = ObjectPicker.get_dot_with_axis_and_mouse_pos(axis, mouse_pos,
                                                                                    ObjectPicker._last_picked_obj_m_model)
        ObjectPicker.active_axis = axis
        ObjectPicker.active_axis.size = 10.0

    @staticmethod
    def process_click_object(object_id):
        if ObjectPicker.active_axis:
            ObjectPicker.active_axis.set_default_size()
            ObjectPicker.active_axis = None
        if object_id != ObjectPicker._last_picked_obj_id:
            if ObjectPicker._last_picked_obj_id != 0:
                renderer = ObjectPicker._app.scene.objects[ObjectPicker._last_picked_obj_id].get_component_by_name(
                    'Renderer')
                renderer.material = ObjectPicker._last_picked_obj_material
                renderer.apply()
            ObjectPicker._last_picked_obj_id = object_id
            renderer = ObjectPicker._app.scene.objects[object_id].get_component_by_name('Renderer')
            ObjectPicker._last_picked_obj_material = renderer.material
            renderer.material = library_m.materials['gray']
            ObjectPicker.last_picked_obj_transformation = renderer.transformation

    @staticmethod
    def process_click_nowhere():
        if ObjectPicker.active_axis:
            ObjectPicker.active_axis.set_default_size()
            ObjectPicker.active_axis = None
        if ObjectPicker._last_picked_obj_id != 0:
            renderer = ObjectPicker._app.scene.objects[ObjectPicker._last_picked_obj_id].get_component_by_name(
                'Renderer')
            renderer.material = ObjectPicker._last_picked_obj_material
            ObjectPicker._last_picked_obj_material = None
            ObjectPicker.last_picked_obj_transformation = None
            ObjectPicker._last_picked_obj_id = 0

    @staticmethod
    def process_release_left_mouse_button(mouse_pos):
        axis = ObjectPicker.active_axis
        if axis:
            axis.set_default_size()
            ObjectPicker.active_axis = None
            return True
        return False

    @staticmethod
    def picking_pass():
        ObjectPicker._pick_fbo.use()
        ObjectPicker._app.ctx.clear(0.0, 0.0, 0.0)
        for obj in ObjectPicker._app.scene.objects.values():
            renderer = obj.get_component_by_name('Renderer')
            if renderer is None:
                continue
            past_color = renderer._material['color'].value
            pick_color = index_manager_m.IndexManager.get_color_by_id(obj.id)
            renderer._material['color'].value = glm.vec3(pick_color)
            renderer.apply()
            renderer._material['color'].value = past_color

        if ObjectPicker._last_picked_obj_id != 0:
            for gizmo_obj in ObjectPicker._app.scene.gizmo_objects.values():
                past_color = gizmo_obj.color
                past_size = gizmo_obj.size
                gizmo_obj.size = 20
                gizmo_obj.color = index_manager_m.IndexManager.get_color_by_id(gizmo_obj.id)
                gizmo_obj.vao.render(mgl.LINES)
                gizmo_obj.color = past_color
                gizmo_obj.size = past_size

        ObjectPicker._app.ctx.screen.use()

    @staticmethod
    def get_dot_with_axis_and_mouse_pos(axis, mouse_pos, m_model):
        p0 = glm.vec4(axis.start, 1.0)
        p1 = glm.vec4(axis.end, 1.0)
        m_mvp = axis.camera.m_proj * axis.camera.m_view * m_model

        # clip space
        p0 = (m_mvp * p0)
        p1 = (m_mvp * p1)

        # ndc
        ndc_p0 = p0 / p0.w
        ndc_p1 = p1 / p1.w

        # Screen coordinates:
        screen_p0 = glm.vec2((ndc_p0.x + 1.0) * ObjectPicker._app.win_size[0],
                             (ndc_p0.y) * ObjectPicker._app.win_size[1]) * 0.5
        screen_p1 = glm.vec2((ndc_p1.x + 1.0) * ObjectPicker._app.win_size[0],
                             (ndc_p1.y) * ObjectPicker._app.win_size[1]) * 0.5

        dot = glm.dot(mouse_pos - screen_p0, glm.normalize(screen_p1 - screen_p0))
        return dot

    @staticmethod
    def process_hold_left_mouse_button(current_pos):
        axis = ObjectPicker.active_axis
        if axis is None:
            return False

        dot = ObjectPicker.get_dot_with_axis_and_mouse_pos(axis, current_pos,
                                                           ObjectPicker._last_picked_obj_m_model)
        difference = dot - ObjectPicker._last_mouse_dot
        ObjectPicker._last_mouse_dot = dot
        ObjectPicker.last_picked_obj_transformation.pos += (axis.end - axis.start) * difference / 100
        return True
