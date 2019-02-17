import os
import re
import sublime
import sublime_plugin

from subprocess import CalledProcessError
from .app.app import App


class CleanupOnFileSave(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        app = App(view.file_name())

        if app.package.type is None:
            return

        sublime.status_message('MagentoWorkflow is working...')

        try:
            app.cleanup()
            sublime.status_message(
                'MagentoWorkflow succeded in %.2f seconds'
                % app.elapsed()
            )
        except CalledProcessError as err:
            print(
                'MagentoWorkflow failed to execute: "%s"'
                % err.output
            )
            sublime.status_message(
                'MagentoWorkflow error. See more information in console'
            )

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

    def generate_remove_command(self, paths):
        commands = []
        for path in paths:
            commands.append('find . -type f -regex "{}" -exec rm -rf {{}} \\;'.format(path))
        return ' && '.join(commands);

    def find_workdir(self):
        index = self.find_file('index.php')
        if index:
            workdir = os.path.dirname(index)
            if os.path.isfile(os.sep.join([workdir, 'bin/magento'])):
                return workdir

        return self.view.window().extract_variables().get('folder')
