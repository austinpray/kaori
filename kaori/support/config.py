from functools import lru_cache
import importlib.util

# TODO: get_config should probably return a standardized config class
@lru_cache(maxsize=32)
def get_config(path):
    spec = importlib.util.spec_from_file_location("config.kaori", path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    return config
