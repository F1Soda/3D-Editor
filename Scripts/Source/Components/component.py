from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from Scripts.Source.General.object import Object


class Component:
    def __init__(self, name: str, description: str, rely_object: Object, enable=True):
        self.name = name
        self.description = description
        self.rely_object = rely_object
        self.enable = enable

    def set_active(self, enable: bool):
        self.enable = enable

    def apply(self): ...

    def delete(self):
        rely_object = None

    def on_change(self): ...

    def update(self): ...
