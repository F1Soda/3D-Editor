import typing
import Scripts.Source.Components.component as component_m
import Scripts.Source.Components.transformation as transformation_m
import Scripts.Source.Components.renderer as renderer_m
import Scripts.Source.General.index_manager as index_manager_m

GLOBAL_INDEX = 0


class Object:
    def __init__(self, scene, name: str, parent_object=None,
                 obj_id=None):
        self.scene = scene
        self.name = name
        self.components: typing.List[component_m.Component] = []
        self.parent_object = parent_object
        self.child_objects = []
        if obj_id:
            self.id = obj_id
        else:
            self.id = scene.index_manager.get_id()

        # Transformation
        self.transformation = transformation_m.Transformation()

        self.add_component(self.transformation)

        self._renderer: renderer_m.Renderer = None
        self.enable = True

    def add_component(self, component) -> component_m.Component:
        component.rely_object = self
        component.init(self.scene.app, self)
        self.components.append(component)
        component.apply()
        return component

    def process_window_resize(self, new_size):
        for component in self.components:
            component.process_window_resize(new_size)

    def get_component_by_name(self, name: str) -> component_m.Component | None:
        for component in self.components:
            if component.name == name:
                return component
        return None

    def get_component_by_type(self, type_component: type) -> component_m.Component | None:
        for component in self.components:
            if isinstance(component, type_component):
                return component
        return None

    def delete(self):
        for component in self.components:
            component.delete()

    def apply_components(self):
        for component in self.components:
            if component.enable and component.name not in ["Renderer", "Plane"]:
                component.apply()

    def serialize(self):
        return {
            'name': self.name,
            'components': {
                component.name: component.serialize() for component in self.components
            }
        }

    def __str__(self):
        return f"Object '{self.name}', id: {self.id}, pos: {self.transformation.pos.to_tuple()}"

    def __repr__(self):
        return str(self)
