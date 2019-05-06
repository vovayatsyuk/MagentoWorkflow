import yaml

from .filesystem import *


class Docker:
    def __init__(self, app):
        self.app = app
        self._config = None

    def config(self):
        if self._config is not None:
            return self._config

        file = closest('docker-compose.yml', self.app.workdir, False, 2)
        if file:
            with open(file, 'r') as stream:
                try:
                    self._config = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
        else:
            self._config = False

        return self._config

    def service_name(self, search):
        config = self.config()
        if config:
            services = config.get('services')
            try:
                return next(k for k, v in services.items() if search in k)
            except StopIteration:
                return None
        return None
