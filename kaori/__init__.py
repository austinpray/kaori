from pathlib import Path

from .support.config import get_config

_test_config_path = Path(__file__).parent.joinpath('../config/kaori_test.py').absolute()
test_config = get_config(str(_test_config_path))

__all__ = ['test_config']
