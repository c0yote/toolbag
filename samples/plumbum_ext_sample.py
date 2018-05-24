import os

from plumbum import local

from toolbag.plumbum_ext import virtualenv_context

# Hook applications.
virtualenv = local['virtualenv']

# Build virtualenv
virtualenv('.env')

with virtualenv_context('.env'):
    print(local['pip']('install','virtualenv'))