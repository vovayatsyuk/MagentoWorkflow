import re


class Resources:
    module_resources = [
        './var/view_preprocessed/pub/static/{area}/.*/{module}/css/{file}',
        './pub/static/{area}/.*/{module}/css/.*',
    ]

    theme_resources = [
        './var/view_preprocessed/pub/static/{area}/.*/css/.*styles-.*css',
        './var/view_preprocessed/pub/static/{area}/.*/css/.*print.*css',
        './var/view_preprocessed/pub/static/{area}/.*/css/{file}',
        './pub/static/{area}/.*/css/.*',
    ]

    requirejs_resources = [
        './pub/static/{area}/.*/requirejs-config.js',
    ]

    generated_resources = [
        './generated/code/{module}/{file}/Interceptor.php',
    ]

    def __init__(self, app):
        self.app = app

    def remove(self, patterns=None):
        if patterns is None:
            patterns = self.get_patterns()

        commands = []
        for path in patterns:
            commands.append(
                'find . -type f -regex "{}" -exec rm -rf {{}} \\;'.format(path)
            )
        self.app.terminal.run(' && '.join(commands))

    def get_patterns(self):
        patterns = []
        patterns.extend(self.get_module_patterns())
        patterns.extend(self.get_requirejs_patterns())
        patterns.extend(self.get_generated_patterns())
        return patterns

    def get_module_patterns(self):
        match = re.search(r'view/(\w+)/web/css/(.*)', self.app.filepath)
        if match is None:
            return []
        return self.render_patterns(self.module_resources, {
            'area': match.group(1),
            'module': self.app.package.module,
            'file': match.group(2),
        })

    def get_requirejs_patterns(self):
        match = re.search(r'view/(\w+)/requirejs-config.js', self.app.filepath)
        if match is None:
            return []
        return self.render_patterns(self.requirejs_resources, {
            'area': match.group(1),
            'module': self.app.package.module
        })

    def get_generated_patterns(self):
        if '.php' not in self.app.filepath:
            return []

        match = re.search(
            r'/vendor/[\w-]+/[\w-]+/(.*)\.php',
            self.app.filepath
        )
        if not match:
            match = re.search(
                r'/app/code/[\w-]+/[\w-]+/(.*)\.php',
                self.app.filepath
            )

        if not match:
            return []

        file = match.group(1)
        return self.render_patterns(self.generated_resources, {
            'module': self.app.package.module.replace('_', '/'),
            'file': file,
        })

    def render_patterns(self, patterns, options):
        rendered = []
        for pattern in patterns:
            rendered.append(pattern.format(**options))
        return rendered
