import os
import re
import sublime_plugin

class CleanupOnFileSave(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        if self.init_vars(view) is False:
            return

        command = ' && '.join(filter(None, [
            self.module_resources(),
            self.theme_resources(),
            self.requirejs(),
            self.generated(),
            self.cache(),
        ]))

        if not command:
            return

        self.view.window().run_command('exec', { 'kill': True })
        self.view.window().run_command('exec', {
            'shell': True,
            'quiet': False,
            'cmd': [command],
            'working_dir': self.workdir,
        })

    def init_vars(self, view):
        self.view = view
        self.filepath = view.file_name()
        self.workdir = self.find_workdir()

        registration = self.find_file('registration.php')
        if registration is None:
            return False

        types = {
            'module': r'[\'"]((\w+_\w+))[\'"]',
            'theme':  r'[\'"](frontend|adminhtml)/([\w-]+/[\w-]+)[\'"]',
        }

        contents = open(registration).read()
        for package_type in types:
            match = re.search(types[package_type], contents)
            if match:
                self.type = package_type
                self.area = match.group(1)
                self.code = match.group(2)
                return

        return False

    def module_resources(self):
        if '/web/css/' not in self.filepath:
            return

        if self.type is 'module':
            match = re.search(r'view/(\w+)/web/css/(.*)', self.filepath)
            if match is None:
                return
            area = match.group(1)
            file = match.group(2)
            code = self.code
        else:
            # maybe it's a module file inside theme?
            match = re.search(r'(\w+)/web/css/(.*)', self.filepath)
            if match is None:
                return
            area = self.area
            file = match.group(2)
            code = match.group(1)

        return self.generate_remove_command([
            './var/view_preprocessed/pub/static/{}/.*/{}/css/{}'.format(area, code, file),
            './pub/static/{}/.*/{}/css/.*'.format(area, code),
        ]);

    def theme_resources(self):
        if '/web/css/' not in self.filepath:
            return

        if self.type is not 'theme':
            return

        match = re.search(r'web/css/(.*)', self.filepath)
        if match is None:
            return

        return self.generate_remove_command([
            './var/view_preprocessed/pub/static/{}/.*/css/.*styles-.*css'.format(self.area),
            './var/view_preprocessed/pub/static/{}/.*/css/.*print.*css'.format(self.area),
            './var/view_preprocessed/pub/static/{}/.*/css/{}'.format(self.area, match.group(1)),
            './pub/static/{}/.*/css/.*'.format(self.area),
        ])

    def requirejs(self):
        if '/requirejs-config.js' not in self.filepath:
            return

        if self.type is 'module':
            match = re.search(r'view/(\w+)/requirejs-config.js', self.filepath)
            if match is None:
                return
            area = match.group(1)
            code = self.code
        else:
            # it's a requirejs file inside theme
            area = self.area

        return self.generate_remove_command([
            './pub/static/{}/.*/requirejs-config.js'.format(area),
        ]);

    def generated(self):
        if '.php' not in self.filepath:
            return

        match = re.search(r'/vendor/[\w-]+/[\w-]+/(.*)', self.filepath)
        if not match:
            match = re.search(r'/app/code/[\w-]+/[\w-]+/(.*)', self.filepath)

        if not match:
            return

        file = match.group(1)

        return self.generate_remove_command([
            './generated/code/{}/{}/Interceptor.php'.format(self.code.replace('_', '/'), file.replace('.php', '')),
        ])

    def cache(self):
        rules = {
            r'/etc/.*\.xml': ['config'],
            r'/Block/.*\.php': ['block_html'],
            r'/templates/.*\.phtml': ['block_html'],
            r'/layout/.*\.xml': ['layout', 'block_html'],
            r'/i18n/.*\.csv': ['translate', 'block_html'],
            r'.*': ['full_page'],
        }

        types = set()
        for pattern in rules:
            if re.findall(pattern, self.filepath):
                for cache_type in rules[pattern]:
                    types.add(cache_type)

        return 'bin/magento cache:clean {}'.format(' '.join(types))

    def generate_remove_command(self, paths):
        commands = []
        for path in paths:
            commands.append('find . -type f -regex "{}" -exec rm -rf {{}} \\;'.format(path))
        return ' && '.join(commands);

    def find_file(self, filename):
        folders = self.filepath.split(os.sep)
        folders.pop()
        folders.append(filename)

        while len(folders) > 2:
            file = os.sep.join(folders)
            if os.path.isfile(file):
                return file
            else:
                del folders[len(folders) - 2]

    def find_workdir(self):
        index = self.find_file('index.php')
        if index:
            workdir = os.path.dirname(index)
            if os.path.isfile(os.sep.join([workdir, 'bin/magento'])):
                return workdir

        return self.view.window().extract_variables().get('folder')
