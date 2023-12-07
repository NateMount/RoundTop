# [Init - Config]

from os import environ
from sys import modules
import roundtop.config.settings

APP_ENV = environ.get('APP_ENV', 'Dev')
_current = getattr(modules['roundtop.config.settings'], '{}Config'.format(APP_ENV))()

[ 
    setattr(
        modules[__name__], 
        attr, 
        environ.get(attr, getattr(_current, attr))
    ) for attr in [
        f for f in dir(_current) if not '__' in f
    ] 
]