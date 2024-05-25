import re
import subprocess


class Cache:
    def __init__(self, app):
        self.app = app

    def bin_magento(self):
        return self.app.settings.get('bin_magento_command')

    def run(self, command):
        try:
            return self.app.terminal.run(command)
        except subprocess.CalledProcessError as err:
            print(err.output.decode().strip('\n\r'))
            print('[MagentoWorkflow] bin/magento is broken, trying to remove cache manually')
            return self.app.terminal.run('rm -rf var/cache')

    def flush(self):
        return self.run(self.bin_magento() + ' cache:flush')

    def clean(self, type=None):
        if type is None:
            type = self.get_types_to_clean()
            if len(type) == 0:
                return

        cmd = '{} cache:clean '.format(self.bin_magento())
        if isinstance(type, (set, list)):
            cmd += ' '.join(type)
        elif type != 'All':
            cmd += type

        return self.run(cmd)

    def get_types_to_clean(self):
        rules = {
            r'/etc/.*\.(xml|xsd)': ['config'],
            r'/Block/.*\.php': ['block_html'],
            r'/Controller/.*\.php': ['config'],
            r'/.*Layout.*\.php': ['layout'],
            r'/templates/.*\.phtml': ['block_html'],
            r'/layout/.*\.xml': ['layout', 'block_html'],
            r'/page_layout/.*\.xml': ['layout', 'block_html'],
            r'/pagebuilder/.*\.xml': ['config'],
            r'/ui_component/.*\.xml': ['config'],
            r'/i18n/.*\.csv': ['translate', 'block_html'],
            r'/menu\.xml': ['block_html'],
            r'\.(php|xml|json)': ['full_page'],
            r'/web/css/': ['full_page'],
            r'/requirejs-config\.js': ['full_page'],
            r'/.*\.html': ['full_page'],
        }

        types = set()
        for pattern in rules:
            if re.findall(pattern, self.app.filepath):
                for cache_type in rules[pattern]:
                    types.add(cache_type)

        if len(types) > 0:
            types.add('full_page')

        return types

    def type(self):
        return [
            ['Block HTML Output', 'block_html'],
            ['Configuration', 'config'],
            ['Database DDL operations', 'db_ddl'],
            ['FPC', 'full_page'],
            ['Layouts', 'layout'],
            ['Translations', 'translate'],
        ]
