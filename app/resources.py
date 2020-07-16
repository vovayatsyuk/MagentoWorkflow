import re


class Resources:
    css_module_resources = [
        'var/view_preprocessed/pub/static/{area}/.*/{code}/css/{file}',
        'pub/static/{area}/.*/{code}/css/.*',
        'pub/static/_cache/merged/.*',
    ]

    css_theme_resources = [
        'var/view_preprocessed/pub/static/{area}/.*/{locale}/css/styles.*css',
        'var/view_preprocessed/pub/static/{area}/.*/{locale}/css/print.*css',
        'var/view_preprocessed/pub/static/{area}/.*/css/{file}',
        'pub/static/{area}/.*/{locale}/css/.*',
        'pub/static/_cache/merged/.*',
    ]

    requirejs_resources = [
        'pub/static/{area}/.*/requirejs-config.js',
    ]

    translation_resources = [
        'pub/static/{area}/.*/js-translation.json',
    ]

    generated_resources = [
        'generated/code/{module_folders}/{file}/Interceptor.php',
    ]

    generated_metadata = [
        'generated/metadata',
    ]

    extension_attributes = [
        'generated/code/.*/.*/Api/Data/.*',
    ]

    def __init__(self, app):
        self.app = app

    def removeAll(self):
        self.remove([
            'var/view_preprocessed/pub/static/frontend',
            'var/view_preprocessed/pub/static/adminhtml',
            'pub/static/frontend',
            'pub/static/adminhtml',
            'generated/code',
            'generated/metadata',
        ])

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
            self.app.terminal.run(commands, ' & ')

    def get_patterns(self, filepath=None, code=None):
        placeholders = self.extract_placeholders(filepath, code)
        allowed_resources = self.app.settings.get('resources', [])

        resources = []

        if 'generated' in allowed_resources:
            if filepath is None or '.php' in filepath or '.xml' in filepath:
                resources.append(self.generated_metadata)

        if filepath is None or '/web/css/' in filepath:
            if (placeholders['type'] == 'module' and
                    # _module.less a part of theme.
                    (filepath is None or
                        'source/_module.less' not in filepath) and
                    # Magento_ module with less file is a part of theme.
                    placeholders['code'].startswith('Magento_') is False):

                if 'css_module' in allowed_resources:
                    resources.append(self.css_module_resources)
            else:
                if 'css_theme' in allowed_resources:
                    resources.append(self.css_theme_resources)

        if ('requirejs' in allowed_resources and
                (filepath is None or 'requirejs-config.js' in filepath)):
            resources.append(self.requirejs_resources)

        if ('translation' in allowed_resources and
                (filepath is None or '.csv' in filepath)):
            resources.append(self.translation_resources)

        if 'generated' in allowed_resources and placeholders['type'] == 'module':
            if filepath is None or '.php' in filepath:
                resources.append(self.generated_resources)
            elif 'extension_attributes.xml' in filepath:
                resources.append(self.extension_attributes)

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
                    if '/source/' in filepath:
                        # if file is inside 'source' subfolder -
                        # module inject it's styles into theme styles with
                        # _module.less file.
                        placeholders.update({
                            'area': match.group(1),
                            'file': match.group(2),
                            'type': 'theme',
                        })
                    else:
                        placeholders.update({
                            'area': match.group(1),
                            'file': match.group(2),
                            'type': 'module',
                        })
                else:
                    # module file inside a theme?
                    match = re.search(
                        r'/(\w+_\w+)/web/css/(.*)',
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
            elif '.csv' in filepath:
                placeholders.update({
                    'area': '.*',
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
