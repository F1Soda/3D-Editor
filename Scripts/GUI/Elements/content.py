import element as element_m
import block as block_m
import glm


class Content(element_m.Element):
    def __init__(self, name, rely_element, win_size: glm.vec2, color=(0, 0, 0, 0.1)):
        super().__init__(name, rely_element, win_size)

        self.background = block_m.Block(f"{name}_block", self, win_size, color)
        self.background.position.relative.right_top = glm.vec2(1)
        self.elements_size = []

    def add(self, element):
        new_size_y = self.position.absolute.size.y + element.position.absolute.size.y
        for i in range(len(self.elements)):
            size_y = self.elements_size[i].y / new_size_y

            self.elements[i].position.relative.size = glm.vec2(self.elements[i].position.relative.size.x, size_y)

        self.background.elements.append(element)
        element.rely_element = self.background
        element.position.rely_element_position = self.background.position
        element.position.absolute.left_bottom = glm.vec2(self.background.position.absolute.left_bottom.x,
                                                         self.background.position.absolute.right_top.y)

        self.position.absolute.size.x = max(self.position.absolute.size.x, element.position.absolute.size.x)
        self.position.absolute.size.y += element.position.absolute.size.y
        self.position.evaluate_values_by_absolute()
        self.background.position.evaluate_values_by_relative()

        element.position.absolute.right_top = self.background.position.absolute.right_top
        element.position.evaluate_values_by_absolute()
        self.elements_size.append(element.position.absolute.size)
        for element in self.elements:
            element.position.evaluate_values_by_relative()

    def render(self):
        self.background.render()
