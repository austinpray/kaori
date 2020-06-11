import sys
import os


def maybe_instrument_debugger() -> None:
    pydevd_pycharm_egg = os.getenv('DEBUGGER_EGG')
    if not pydevd_pycharm_egg:
        return

    debugger_host = os.getenv('DEBUGGER_HOST')
    if not debugger_host:
        raise RuntimeError('not DEBUGGER_HOST configured')

    sys.path.append(pydevd_pycharm_egg)
    import pydevd_pycharm

    pydevd_pycharm.settrace(debugger_host,
                            port=4200,
                            stdoutToServer=True,
                            stderrToServer=True)