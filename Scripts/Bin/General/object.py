import typing
import Scripts.Bin.Components.component as component_m
import Scripts.Bin.Components.transformation as transformation_m
import Scripts.Bin.Components.renderer as renderer_m


class Object:
    def __init__(self, scene, name: str, components: typing.List[component_m.Component], parent_object=None):
        self.scene = scene
        self.name = name
        self.components: typing.List[component_m.Component] = components
        self.parent_object = parent_object
        self.child_objects = []
        self.id = self._create_id()

        # Transformation
        self.transformation = transformation_m.Transformation(self)
        components.append(self.transformation)

        self._renderer: renderer_m.Renderer = None
        self.enable = True

    def _create_id(self) -> int:
        return hash(self.name)

    def add_component(self, component) -> component_m.Component:
        self.components.append(component)
        component.rely_object = self
        component.apply()
        return component

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
            if component.enable:
                component.apply()

    def update_components(self):
        for component in self.components:
            if component.enable:
                component.update()
