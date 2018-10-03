import inspect
from inspect import Parameter

from typing import Dict, Any, Set, Callable


class DependencyMissing(RuntimeError):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.dependency = kwargs.get('dependency', None)


def build_di_args(components: Set, fn: Callable) -> Dict[str, Any]:
    args_dict = {}
    params = inspect.signature(fn).parameters

    components_dict = {component.__class__.__name__: component for component in components}

    param: Parameter
    for name, param in params.items():
        dep_name = param.annotation.__name__
        resolved = components_dict.get(dep_name)
        if not resolved:
            raise DependencyMissing(f'Do not know how to handle dependency "{dep_name}"',
                                    dependency=dep_name)
        args_dict[name] = resolved

    return args_dict
