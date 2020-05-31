import inspect
from abc import ABC
from inspect import Parameter

from typing import Dict, Any, Set, Callable


class DependencyMissing(RuntimeError):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args)
        self.dependency = kwargs.get('dependency', None)


def needs_di(fn: Callable, component: object) -> bool:
    params = inspect.signature(fn).parameters

    param: Parameter
    for name, param in params.items():
        if component.__class__.__name__ == param.annotation.__name__:
            return True

    return False


def build_di_args(components: Set, fn: Callable) -> Dict[str, Any]:
    params = inspect.signature(fn).parameters

    components_dict = {}
    for component in components:
        mro = component.__class__.mro()
        for method in mro:
            if method == object or method == ABC:
                break
            components_dict[method.__name__] = component

    args_dict = {}

    param: Parameter
    for name, param in params.items():
        dep_name = param.annotation.__name__
        resolved = components_dict.get(dep_name)
        if resolved:
            args_dict[name] = resolved
            continue

        raise DependencyMissing(f'Do not know how to handle dependency "{dep_name}"',
                                dependency=dep_name)

    return args_dict
