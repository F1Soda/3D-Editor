from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from Scripts.Source.General.object import Object


class Component:
    def __init__(self, name: str, description: str, enable=True):
        self.name = name
        self.description = description
        self.rely_object = None  # type: Object | None
        self.enable = enable
        self.app = None

    def set_active(self, enable: bool):
        self.enable = enable

    def apply(self): ...

    def delete(self):
        self.rely_object = None
        self.app = None
        self.name = None
        self.description = None

    def on_change(self): ...

    def init(self, app, rely_object):
        self.app = app
        self.rely_object = rely_object

    def serialize(self) -> {}:
        ...

    def process_window_resize(self, new_size):
        ...

    def __str__(self):
        return f"Component '{self.name}', rely object: {self.rely_object}"

    def __repr__(self):
        return str(self)
