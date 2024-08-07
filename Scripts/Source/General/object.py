import typing
import Scripts.Source.Components.component as component_m
import Scripts.Source.Components.transformation as transformation_m
import Scripts.Source.Components.renderer as renderer_m
import Scripts.Source.General.index_manager as index_manager_m

GLOBAL_INDEX = 0


class Object:
    def __init__(self, scene, name: str, components: typing.List[component_m.Component], parent_object=None):
        self.scene = scene
        self.name = name
        self.components: typing.List[component_m.Component] = components
        self.parent_object = parent_object
        self.child_objects = []
        self.id = index_manager_m.IndexManager.get_id()

        # Transformation
        self.transformation = transformation_m.Transformation(self)
        components.append(self.transformation)

        self._renderer: renderer_m.Renderer = None
        self.enable = True

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
            if component.enable and component.name not in ["Renderer", "Plane"]:
                component.apply()

    def update_components(self):
        for component in self.components:
            if component.enable:
                component.update()
