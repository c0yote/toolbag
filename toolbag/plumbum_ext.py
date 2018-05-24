import os
from contextlib import contextmanager

from plumbum import local

UNSUPPORTED_OS_ERROR_MSG = f'Context Manager \'virtualenv\' not implemented for OS \'{os.name}\'.'

def _activate_virtualenv_on_windows(virtualenv_dir):
    venv_bin_dir = os.path.join(virtualenv_dir, 'Scripts')
    patch_path = f"{venv_bin_dir};{local.env['PATH']}"
    local.env['PATH'] = patch_path
    
    patch_python = local['python']
    local.python = patch_python

def _is_windows():
    return os.name is 'nt'

@contextmanager
def virtualenv_context(virtualenv_dir):
    """ Loads virtual environment.
        
        with virtualenv_context('.env'):
            local['pip']('install','plumbum')
    """
    orig_path = local.env['PATH']
    orig_python = local.python
    
    if _is_windows():
        _activate_virtualenv_on_windows(virtualenv_dir)
    else:
        raise NotImplementedError(UNSUPPORTED_OS_ERROR_MSG)
    
    try:
        yield
    finally:
        local.env['PATH'] = orig_path
        local.python = orig_python
