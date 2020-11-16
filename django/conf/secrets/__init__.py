from django.conf import settings
from django.utils.functional import empty, SimpleLazyObject
from django.utils.module_loading import import_string


class Secrets:
    _env = empty

    def __init__(self):
        self._setup()

    def _setup(self):
        if settings.configured and not self.configured:
            secret_backends = settings.SECRET_BACKENDS
            self._env = {}
            for backend_str in secret_backends:
                backend_cls = import_string(backend_str)
                backend = backend_cls()
                self._env.update(backend.get_envs())

    def __getitem__(self, item):
        self._setup()
        if self.configured:
            return self._env[item]

        def proxy_getitem():
            if not self.configured:
                self._setup()
            return self._env[item]

        return SimpleLazyObject(proxy_getitem)

    @property
    def configured(self):
        return self._env is not empty


secrets = Secrets()
