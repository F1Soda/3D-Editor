import Scripts.Bin.Components.component as component_m
import Scripts.Bin.General.main as main_m
import Scripts.Bin.General.object as object_m
import Scripts.Bin.Components.camera as camera_m
import Scripts.Bin.Components.transformation as transformation_m
import glm
import pygame as pg

NAME = "Free Fly Move"
DESCRIPTION = "Компонент для свободного передвижения камеры"

SPEED = 0.005
SHIFT_SPEED = 0.01
SENSITIVITY = 0.2


class FreeFlyMove(component_m.Component):
    def __init__(self, rely_object: object_m.Object, app: main_m.GraphicsEngine, enable=True):
        super().__init__(NAME, DESCRIPTION, rely_object, enable)
        self.app = app
        self._transformation = rely_object.transformation
        self.camera_component = rely_object.get_component_by_name('Camera')  # type: camera_m.Camera

        self.RIGHT_MOUSE_BUTTON_RELEASED = False

    def _move(self):
        keys = pg.key.get_pressed()
        velocity = (SHIFT_SPEED if keys[pg.K_LSHIFT] else SPEED) * self.app.delta_time

        if keys[pg.K_w]:
            self.transformation.pos += self.camera_component.forward * velocity
        if keys[pg.K_s]:
            self.transformation.pos -= self.camera_component.forward * velocity
        if keys[pg.K_a]:
            self.transformation.pos -= self.camera_component.right * velocity
        if keys[pg.K_d]:
            self.transformation.pos += self.camera_component.right * velocity
        if keys[pg.K_q]:
            self.transformation.pos += self.camera_component.up * velocity
        if keys[pg.K_e]:
            self.transformation.pos -= self.camera_component.up * velocity

    def _rotate(self):
        if pg.mouse.get_pressed()[2]:  # Right click
            if not self.RIGHT_MOUSE_BUTTON_RELEASED:
                self.RIGHT_MOUSE_BUTTON_RELEASED = True
                rel_x, rel_y = pg.mouse.get_rel()
            rel_x, rel_y = pg.mouse.get_rel()
            self.transformation.rot.y += rel_x * SENSITIVITY
            self.transformation.rot.x -= rel_y * SENSITIVITY
            self.transformation.rot.x = max(-89, min(89, self.transformation.rot.x))
        else:
            self.RIGHT_MOUSE_BUTTON_RELEASED = False

    def _update_camera_vectors(self):
        x, y = glm.radians(self.transformation.rot.y), glm.radians(self.transformation.rot.x)

        self.camera_component.forward.x = glm.cos(x) * glm.cos(y)
        self.camera_component.forward.y = glm.sin(y)
        self.camera_component.forward.z = glm.sin(x) * glm.cos(y)

        self.camera_component.forward = glm.normalize(self.camera_component.forward)
        self.camera_component.right = glm.normalize(glm.cross(self.camera_component.forward, glm.vec3(0, 1, 0)))
        self.camera_component.up = glm.normalize(glm.cross(self.camera_component.right, self.camera_component.forward))

    def update(self):
        self._move()
        self._rotate()
        self._update_camera_vectors()

    @property
    def transformation(self):
        if self._transformation is None:
            self._transformation = self.rely_object.get_component_by_type(transformation_m.Transformation)
        return self._transformation

    @transformation.setter
    def transformation(self, value):
        self._transformation = value

    def delete(self):
        self.app = None
        self.camera_component = None
        self.transformation = None
        self.rely_object = None
