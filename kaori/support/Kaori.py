import asyncio
import inspect
from typing import Dict
import logging

from kaori.adapters import Adapter
from .di import build_di_args, DependencyMissing, needs_di


class Kaori:

    def __init__(self) -> None:
        self.adapters: Dict[str, Adapter] = {}
        self.skills = set()
        self.plugins = set()
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def can_handle(adapter: Adapter, cls) -> bool:
        # todo: the [1:2] slice is very fragile
        for mro_cls in [mro_cls.__name__ for mro_cls in inspect.getmro(cls)[1:2]]:
            for handleable in [handleable.__name__ for handleable in adapter.handles]:
                if handleable == mro_cls:
                    return True

        return False

    def get_handleable(self, adapter: Adapter) -> list:
        handleable = []
        for plugin in self.plugins:
            for name, obj in inspect.getmembers(plugin, inspect.isclass):
                if self.can_handle(adapter, obj):
                    handleable.append(obj)

        return handleable

    def get_base_components(self):
        return self.skills | {adapter for adapter in self.adapters.values()}

    def handle(self, adapter_name: str, payload: dict):
        adapter: Adapter = self.adapters.get(adapter_name)
        event = adapter.convert_payload(payload)
        handleable = self.get_handleable(adapter)

        components = {event} | self.get_base_components()
        for command in handleable:
            if needs_di(command.handle, event):
                asyncio.run(command.handle(**build_di_args(components, command.handle)))
