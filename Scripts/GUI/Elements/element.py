import glm


class Element:
    def __init__(self, name, rely_element, relative_left_bottom: glm.vec2, win_size: glm.vec2,
                 relative_right_top=glm.vec2(1, 1),
                 size: glm.vec2 = None):
        self.name = name
        self.relative_left_bottom = relative_left_bottom
        self.relative_right_top = relative_right_top
        self.rely_element = rely_element

        if self.rely_element:
            self.rely_element.elements.append(self)
        self.win_size = win_size
        self.size = size

        self.left_bottom, self.right_top = None, None

        self.evaluate_abs_values()

        self.m_gui = glm.mat4()
        self.elements = []

    @property
    def aspect_ratio(self):
        return self.size.x / self.size.y

    @property
    def win_aspect_ratio(self):
        return self.win_size.x / self.win_size.y

    @property
    def aspect_vec2(self):
        return glm.vec2(1, self.aspect_ratio)

    def evaluate_abs_values(self):
        rely_element = self.rely_element
        if rely_element:
            self.left_bottom = (rely_element.left_bottom + rely_element.size * self.relative_left_bottom)
            self.right_top = (rely_element.left_bottom + rely_element.size * self.relative_right_top)
            self.size = self.right_top - self.left_bottom
        elif self.size:
            self.left_bottom = glm.vec2(0, 0)
            self.right_top = self.size

    def process_window_resize(self, new_size: glm.vec2):
        self.win_size = new_size
        if self.rely_element is None:
            self.size = new_size
        self.evaluate_abs_values()
        for element in self.elements:
            element.process_window_resize(new_size)

    def update_m_gui(self, size=None):
        vec4 = glm.vec4
        if size is None:
            size = self.size
        win_size = self.win_size
        left_bottom = self.left_bottom
        rely_element = self.rely_element
        if rely_element is None:
            rely_element = self
        c0 = vec4(size.x / win_size.x, 0, 0, 0)
        c1 = vec4(0, size.y / win_size.y, 0, 0)
        c2 = vec4(0, 0, 0, 0)
        c3 = vec4((left_bottom.x - rely_element.left_bottom.x) / win_size.x + rely_element.m_gui[3][0],
                  (left_bottom.y - rely_element.left_bottom.y) / win_size.y + rely_element.m_gui[3][1], 0, 1)

        m_gui = glm.mat4x4(c0, c1, c2, c3)
        self.m_gui = m_gui

    def add(self, element):
        self.elements.append(element)

    def render(self):
        for element in self.elements:
            element.render()

    def delete(self):
        for element in self.elements:
            element.delete()
        self.rely_element = None
        self.elements.clear()

    def handle_left_click(self, pos):
        ...

    def handle_right_click(self, pos):
        ...

    def __str__(self):
        return f"GUI. Name: {self.name}, Type: {self.__class__.__name__}"

    def __repr__(self):
        return str(self)
