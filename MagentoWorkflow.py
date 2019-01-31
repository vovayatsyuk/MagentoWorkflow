import os
import re
import subprocess

import time
import sublime
import sublime_plugin

class MagentoWorkflow:

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

    def __init__(self, filepath=None):
        self.workdir = None
        self.filepath = None

        if filepath is None:
            return

        self.init_vars(filepath)

    def init_vars(self, filepath):
        if os.path.isdir(filepath):
            self.workdir = filepath
        elif os.path.isfile(filepath):
            self.filepath = filepath
            self.package = self.get_package_info()
            # self.workdir = self.find_workdir()

    def cmd(self, command):
        return subprocess.call(command, shell=True)

    def cleanup(self, filepath=None):
        if filepath is None:
            filepath = self.filepath
        else:
            self.init_vars(filepath)

        if self.filepath is None or self.package is None:
            return

        self.result = {
            'success': False,
            'elapsed': 0
        }

        start = time.time()
        getattr(self, 'cleanup_' + self.package['type'])(filepath)

        self.result = {
            'success': True,
            'elapsed': time.time() - start
        }

    def get_package_info(self):
        registration = self.closest_file('registration.php')
        if registration is None:
            return None

        types = {
            'module': r'[\'"]((\w+_\w+))[\'"]',
            'theme':  r'[\'"](frontend|adminhtml)/([\w-]+/[\w-]+)[\'"]',
        }

        contents = open(registration, 'r', encoding='utf-8').read()
        for package_type in types:
            match = re.search(types[package_type], contents)
            if match:
                return {
                    'type': package_type,
                    'area': match.group(1), # this value is correct for theme only
                    'module': match.group(2),
                }

        return None

    def cleanup_module(self, filepath):
        match = re.search(r'view/(\w+)/web/css/(.*)', filepath)
        if match:
            area = match.group(1)
            file = match.group(2)
            patterns = []
            for resource in self.module_resources:
                patterns.append(resource.format(**{
                    'area': area,
                    'module': self.package['module'],
                    'file': file,
                }))
            self.remove_resources(patterns)

    def cleanup_theme(self, filepath):
        print('theme')

    def remove_resources(self, patterns):
        commands = []
        for path in patterns:
            commands.append('find . -type f -regex "{}" -exec rm -rf {{}} \\;'.format(path))
        return self.cmd(' && '.join(commands));

    def find_workdir(self):
        return 'magento root folder path'

    def closest_file(self, filename):
        """ Search for file by filename, closest to the currently opened file.
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
        workflow = MagentoWorkflow(view.file_name())
        if workflow.package is None:
            return

        sublime.status_message('MagentoWorkflow is working...')

        start = time.time()
        workflow.cleanup()
        elapsed = time.time() - start;

        if workflow.result['success'] is True:
            sublime.status_message('MagentoWorkflow succeded in %.2f seconds' % workflow.result['elapsed'])
        else:
            # print('MagentoWorkflow failed to execute: "%s"' % workflow.result.command)
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
