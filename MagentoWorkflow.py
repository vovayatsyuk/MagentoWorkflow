import os
import re
import sublime_plugin

class CleanupOnFileSave(sublime_plugin.EventListener):
    def on_post_save(self, view):
        self.view = view
        self.filepath = view.file_name()
        self.workdir = None
        self.workdir = self.find_workdir()
        self.init_package_info()

        if not self.registration:
            return

        command = ' && '.join(filter(None, [
            self.module_resources(),
            self.theme_resources(),
            self.generated(),
            self.cache(),
        ]))

        if not command:
            return

        self.view.window().run_command('exec', { 'kill': True })
        self.view.window().run_command('exec', {
            'shell': True,
            'quiet': True,
            'cmd': [command],
            'working_dir': self.workdir,
        })

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
            r'/web/css/': 'fpc',
            r'/etc/.*\.xml': 'config fpc',
            r'/Block/.*\.php': 'block fpc',
            r'/templates/.*\.phtml': 'block fpc',
            r'/layout/.*\.xml': 'layout block fpc',
            r'/i18n/.*\.csv': 'translate block fpc',
        }

        for pattern in rules:
            if re.findall(pattern, self.filepath):
                return 'bin/magento cache:clean {}'.format(rules[pattern])

    def generate_remove_command(self, paths):
        commands = []
        for path in paths:
            commands.append('find . -type f -regex "{}" -exec rm -rf {{}} \\;'.format(path))
        return ' && '.join(commands);

    def init_package_info(self):
        self.registration = self.find_file('registration.php')
        if self.registration is None:
            return

        types = {
            'module': r'[\'"]((\w+_\w+))[\'"]',
            'theme':  r'[\'"](frontend|adminhtml)/([\w-]+/[\w-]+)[\'"]',
        }

        contents = open(self.registration).read()
        for package_type in types:
            match = re.search(types[package_type], contents)
            if match:
                self.type = package_type
                self.area = match.group(1)
                self.code = match.group(2)
                return

    def find_file(self, filename):
        if self.workdir is None:
            min_depth = 5
        else:
            min_depth = self.workdir.count('/') + 1

        folders = self.filepath.split(os.sep)
        folders.pop()
        folders.append(filename)

        while len(folders) > min_depth:
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
