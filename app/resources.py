import re


class Resources:
    css_module_resources = [
        'var/view_preprocessed/pub/static/{area}/.*/{code}/css/{file}',
        'pub/static/{area}/.*/{code}/css/.*',
    ]

    css_theme_resources = [
        'var/view_preprocessed/pub/static/{area}/.*/{locale}/css/styles.*css',
        'var/view_preprocessed/pub/static/{area}/.*/{locale}/css/print.*css',
        'var/view_preprocessed/pub/static/{area}/.*/css/{file}',
        'pub/static/{area}/.*/{locale}/css/.*',
    ]

    requirejs_resources = [
        'pub/static/{area}/.*/requirejs-config.js',
    ]

    generated_resources = [
        'generated/code/{module_folders}/{file}/Interceptor.php',
    ]

    def __init__(self, app):
        self.app = app

    def remove(self, patterns=None):
        if patterns is None:
            patterns = self.get_patterns(self.app.filepath)
        elif type(patterns) is not list:
            patterns = self.get_patterns(None, patterns)

        commands = []
        for path in patterns:
            if '.*' not in path:
                path = path.lstrip('./')
                cmd = 'rm -rf "{}"'
            elif '/.*/' in path:
                basedir, path = path.split('/.*/', 1)
                cmd = ('find ' + basedir +
                       ' -type f -regex ".*/{}" -exec rm -rf {{}} \\;')
            else:
                cmd = 'find . -type f -regex ".*{}" -exec rm -rf {{}} \\;'

            commands.append(cmd.format(path))

        if commands:
            self.app.terminal.run(' && '.join(commands))

    def get_patterns(self, filepath=None, code=None):
        placeholders = self.extract_placeholders(filepath, code)

        resources = []
        if filepath is None or '/web/css/' in filepath:
            if (placeholders['type'] == 'module' and
                    # Magento_ module with less file is a part of theme.
                    placeholders['code'].startswith('Magento_') is False):
                resources.append(self.css_module_resources)
            else:
                resources.append(self.css_theme_resources)

        if filepath is None or 'requirejs-config.js' in filepath:
            resources.append(self.requirejs_resources)

        if (placeholders['type'] == 'module' and
                (filepath is None or '.php' in filepath)):
            resources.append(self.generated_resources)

        patterns = []
        for resource in resources:
            patterns.extend(self.render_patterns(resource, placeholders))

        return patterns

    def extract_placeholders(self, filepath=None, code=None):
        placeholders = {
            'code': self.app.package.code,
            'area': self.app.package.area,
            'type': self.app.package.type,
            'file': '.*',
            'locale': '[a-z]*_[A-Z]*',
        }

        if filepath is None:
            placeholders.update({
                # don't use '[]' or '()'. @see remove method
                'area': '.*',
            })
            if code is not None:
                placeholders.update({
                    'code': code,
                    'type': 'theme' if '/' in code else 'module',
                })
        else:
            if '/web/css/' in filepath:
                # module file?
                match = re.search(r'view/(\w+)/web/css/(.*)', filepath)
                if match:
                    placeholders.update({
                        'area': match.group(1),
                        'file': match.group(2),
                        'type': 'module',
                    })
                else:
                    # module file inside a theme?
                    match = re.search(
                        self.app.package.code + r'/(\w+)/web/css/(.*)',
                        filepath
                    )
                    if match:
                        placeholders.update({
                            'code': match.group(1),
                            'file': match.group(2),
                            'type': 'module',
                        })
                    else:
                        # regular theme file
                        match = re.search(r'(\w+)/web/css/(.*)', filepath)
                        placeholders.update({
                            'file': match.group(2),
                            'type': 'theme',
                        })
            elif 'requirejs-config.js' in filepath:
                if self.app.package.type is 'module':
                    match = re.search(
                        r'view/(\w+)/requirejs-config.js',
                        filepath
                    )
                    if match:
                        placeholders.update({
                            'area': match.group(1)
                        })
            elif '.php' in filepath:
                match = re.search(
                    r'/vendor/[\w-]+/[\w-]+/(.*)\.php',
                    filepath
                )
                if not match:
                    match = re.search(
                        r'/code/[\w-]+/[\w-]+/(.*)\.php',
                        filepath
                    )
                if match:
                    file = match.group(1)
                    placeholders.update({
                        'file': file,
                    })

        if placeholders.get('area') == 'base':
            placeholders['area'] = '.*'

        placeholders['module_folders'] = placeholders['code'].replace('_', '/')

        return placeholders

    def render_patterns(self, patterns, options):
        rendered = []
        for pattern in patterns:
            rendered.append(pattern.format(**options))
        return rendered
