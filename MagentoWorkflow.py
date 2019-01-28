import os
import re
import subprocess

import time
import sublime
import sublime_plugin

class MagentoWorkflow:
    def __init__(self, filepath=None):
        self.workdir = None
        self.filepath = None

        if filepath is None:
            return

        if os.path.isdir(filepath):
            self.workdir = filepath
        elif os.path.isfile(filepath):
            self.filepath = filepath
            self.workdir = self.find_workdir()

    def cmd(self, command):
        return subprocess.call(command, shell=True)

    def cleanup(self, filepath):
        # generate commands? and run with cmd method
        return

    def find_workdir(self):
        return 'magento root folder path'

    def closest_file(self, filename):
        """ Search for the closest file by its filename, relative to the current file.
        """

        folders = self.filepath.split(os.sep)
        folders.pop()
        folders.append(filename)

        while len(folders) > 2:
            file = os.sep.join(folders)
            if os.path.isfile(file):
                return file
            else:
                del folders[len(folders) - 2]

class CleanupOnFileSave(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        workflow = MagentoWorkflow() # .cleanup(view.file_name())

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

        sublime.status_message('MagentoWorkflow is working...')

        start = time.time()
        result = workflow.cmd(command)
        end = time.time()

        if result is 0:
            sublime.status_message('MagentoWorkflow succeded in %d seconds' % (end - start))
        else:
            print('MagentoWorkflow failed to execute: "%s"' % command)
            sublime.status_message('MagentoWorkflow error. See more information in console')

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

        contents = open(registration, 'r', encoding='utf-8').read()
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
